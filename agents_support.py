"""
Customer Support Agent System
Senior Support Representative + Quality Assurance Agent
Includes web scraping and searching tools
Python 3.9+ compatible, direct Ollama API calls
"""

import requests
import json
from typing import Dict, List
from config import get_model_config, get_model_info

# ============================================================================
# TOOLS
# ============================================================================


class ScrapeWebsiteTool:
    """Tool to scrape website content and extract text"""

    def __init__(self):
        self.name = "scrape_website"
        self.description = "Scrapes a website URL and extracts text content for analysis"

    def execute(self, url: str) -> str:
        """
        Scrape website and return text content

        Args:
            url: The URL to scrape

        Returns:
            Extracted text content from the website
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = requests.get(url, timeout=10, headers=headers)
            response.raise_for_status()

            # Simple HTML cleaning - remove common tags
            import re

            # Remove script and style elements
            text = re.sub(r"<script[^>]*>.*?</script>", "", response.text, flags=re.DOTALL)
            text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL)

            # Remove HTML tags
            text = re.sub(r"<[^>]+>", " ", text)

            # Clean up whitespace
            text = re.sub(r"\s+", " ", text).strip()

            # Limit to first 4000 characters for better processing
            return text[:4000]

        except requests.exceptions.ConnectionError:
            return f"❌ Could not connect to {url}. Please check the URL."
        except requests.exceptions.Timeout:
            return f"⏱️  Timeout connecting to {url}. The website took too long to respond."
        except Exception as e:
            return f"❌ Error scraping {url}: {str(e)}"

    def __str__(self):
        return f"Tool: {self.name} - {self.description}"


class WebsiteSearchTool:
    """Tool to search and extract relevant information from website content"""

    def __init__(self):
        self.name = "website_search"
        self.description = "Searches website content for specific information and extracts relevant sections"

    def execute(self, query: str, url: str, scrape_tool: ScrapeWebsiteTool = None) -> str:
        """
        Search website for specific query

        Args:
            query: The search query/question
            url: The URL to search
            scrape_tool: ScrapeWebsiteTool instance

        Returns:
            Relevant information from the website
        """
        if scrape_tool is None:
            scrape_tool = ScrapeWebsiteTool()

        # Scrape the website
        content = scrape_tool.execute(url)

        if content.startswith("❌") or content.startswith("⏱️"):
            return content

        # Simple search - find sentences containing query terms
        sentences = content.split(". ")
        query_terms = query.lower().split()

        relevant_sections = []
        for sentence in sentences:
            if any(term in sentence.lower() for term in query_terms):
                relevant_sections.append(sentence.strip())

        if relevant_sections:
            return ". ".join(relevant_sections[:5])  # Return top 5 relevant sections
        else:
            return f"❌ No relevant information found about '{query}' in {url}"

    def __str__(self):
        return f"Tool: {self.name} - {self.description}"


# ============================================================================
# AGENTS
# ============================================================================


class SimpleAgent:
    """Base agent using direct Ollama API"""

    def __init__(self, role: str, goal: str, backstory: str):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.config = get_model_config()
        self.model = self.config["model"]
        self.ollama_url = "http://localhost:11434"
        self.verbose = self.config["verbose"]

    def print_header(self, text: str):
        """Print formatted header"""
        if self.verbose > 0:
            print(f"\n{'='*70}")
            print(f"  {text}")
            print(f"{'='*70}\n")

    def print_step(self, text: str):
        """Print a step indicator"""
        if self.verbose > 0:
            print(f"📍 {text}")

    def print_response(self, label: str, text: str):
        """Print response with ellipsis if too long"""
        if self.verbose > 0:
            display = text if len(text) < 300 else text[:300] + "..."
            print(f"{label}")
            print(display)

    def call_ollama(self, prompt: str) -> str:
        """Call Ollama API with the prompt"""
        try:
            if self.verbose > 1:
                print(f"  📝 Sending to Ollama ({self.model})...")

            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "temperature": self.config["temperature"],
                    "stream": False,
                },
                timeout=300,
            )

            if response.status_code == 200:
                result = response.json()
                return result.get("response", "")
            else:
                raise Exception(f"Ollama error: {response.status_code}")

        except requests.exceptions.ConnectionError:
            raise Exception(
                f"❌ Cannot connect to Ollama at {self.ollama_url}\n"
                "Make sure Ollama is running: ollama serve"
            )
        except requests.exceptions.Timeout:
            raise Exception("⏱️  Ollama request timed out (model might be slow)")
        except Exception as e:
            raise Exception(f"Error calling Ollama: {str(e)}")


class CustomerSupportAgent(SimpleAgent):
    """Senior support representative - friendly, helpful, doesn't delegate"""

    def __init__(self):
        super().__init__(
            role="Senior Customer Support Representative",
            goal="Provide friendly, helpful, and accurate support to customers without delegating",
            backstory="""You are a senior customer support representative with 10+ years of experience.
You are friendly, empathetic, and genuinely helpful. You take ownership of every customer inquiry
and provide thorough, accurate support. You never delegate tasks - you handle everything directly.
You have deep product knowledge and can answer complex questions.""",
        )
        self.scrape_tool = ScrapeWebsiteTool()
        self.search_tool = WebsiteSearchTool()
        self.memory = {}  # Store interaction context

    def process_inquiry(self, customer_inquiry: str, reference_url: str = None) -> str:
        """
        Process customer inquiry and provide support

        Args:
            customer_inquiry: The customer's question or issue
            reference_url: Optional URL to reference for information

        Returns:
            Support response
        """
        self.print_header(f"👤 SUPPORT AGENT: Processing Customer Inquiry")

        # Store in memory
        self.memory["inquiry"] = customer_inquiry
        if reference_url:
            self.memory["reference_url"] = reference_url

        self.print_step(f"Analyzing inquiry: {customer_inquiry[:100]}...")

        # If reference URL provided, search it for information
        context = ""
        if reference_url:
            self.print_step(f"Searching reference documentation...")
            context = self.search_tool.execute(customer_inquiry, reference_url)
            if self.verbose > 0:
                print(f"  📚 Found reference: {context[:150]}...")

        # Create support response prompt
        prompt = f"""You are a {self.backstory}

Customer Inquiry: {customer_inquiry}

{"Reference Information: " + context if context else "No reference provided"}

Provide a friendly, helpful, and professional response that:
1. Addresses the customer's inquiry directly
2. Shows empathy and understanding
3. Provides actionable solutions or information
4. Offers next steps if needed
5. Maintains a warm, professional tone

Important: You are a senior representative. Handle this inquiry with full ownership and expertise."""

        if self.verbose > 1:
            print(f"  💭 Generating support response...")

        result = self.call_ollama(prompt)
        self.memory["response"] = result

        if self.verbose > 0:
            self.print_response("💬 Support Response:\n", result)

        return result


class SupportQAAgent(SimpleAgent):
    """Quality Assurance Agent - validates responses and enables memory"""

    def __init__(self):
        super().__init__(
            role="Support Quality Assurance Agent",
            goal="Validate support responses for accuracy, quality, and fact-checking",
            backstory="""You are a quality assurance specialist for customer support.
Your role is to fact-check support responses, validate accuracy, and ensure best practices.
You have access to web search and scraping tools to verify information.
You maintain conversation memory to track quality metrics over time.""",
        )
        self.search_tool = WebsiteSearchTool()
        self.scrape_tool = ScrapeWebsiteTool()
        self.memory = {
            "interactions": [],
            "quality_scores": [],
            "common_issues": {},
        }

    def validate_response(
        self, customer_inquiry: str, support_response: str, reference_url: str = None
    ) -> Dict[str, any]:
        """
        Validate support response for quality and accuracy

        Args:
            customer_inquiry: Original customer question
            support_response: Support agent's response
            reference_url: URL to validate facts against

        Returns:
            Validation report with scores and recommendations
        """
        self.print_header(f"✅ QA AGENT: Validating Support Response")

        self.print_step("Checking response quality...")

        # Verify with reference if provided
        verification_result = ""
        if reference_url:
            self.print_step(f"Fact-checking against documentation...")
            verification_result = self.search_tool.execute(customer_inquiry, reference_url)
            if self.verbose > 0:
                print(f"  ✓ Verification data retrieved")

        # Create validation prompt
        prompt = f"""You are a {self.backstory}

Customer Inquiry: {customer_inquiry}

Support Response: {support_response}

{"Reference Information: " + verification_result if verification_result else ""}

Please validate this support response by:

1. ACCURACY (0-10): Is the information factually correct?
2. COMPLETENESS (0-10): Does it fully address the inquiry?
3. CLARITY (0-10): Is the response clear and understandable?
4. TONE (0-10): Is it professional and empathetic?
5. HELPFULNESS (0-10): Will this help the customer?
6. ACTIONABILITY (0-10): Are next steps clear?

Provide:
- Individual scores for each criteria
- Overall quality score (average)
- Key strengths
- Areas for improvement
- Recommendations for enhancement

Format your response as a structured validation report."""

        if self.verbose > 1:
            print(f"  📊 Analyzing response quality...")

        result = self.call_ollama(prompt)

        # Store in memory
        self.memory["interactions"].append(
            {
                "inquiry": customer_inquiry,
                "support_response": support_response[:200],
                "validation": result[:200],
            }
        )

        if self.verbose > 0:
            self.print_response("📋 Validation Report:\n", result)

        return {"validation": result, "inquiry": customer_inquiry, "reference": reference_url}

    def get_memory_summary(self) -> str:
        """Return memory summary"""
        return json.dumps(self.memory, indent=2)


# ============================================================================
# CREW
# ============================================================================


class SupportCrew:
    """Manages the support workflow with inquiry resolution and QA validation"""

    def __init__(self):
        self.support_agent = CustomerSupportAgent()
        self.qa_agent = SupportQAAgent()
        self.config = get_model_config()

    def execute(
        self, customer_inquiry: str, reference_url: str = None
    ) -> Dict[str, any]:
        """
        Execute the complete support workflow

        Args:
            customer_inquiry: The customer's question or issue
            reference_url: Optional URL to reference for information

        Returns:
            Complete support resolution with QA validation
        """
        print(f"\n{'='*70}")
        print(f"  🎯 Customer Support Resolution Workflow")
        print(f"{'='*70}")
        print(f"\n👥 Inquiry: {customer_inquiry}")
        if reference_url:
            print(f"📚 Reference: {reference_url}")
        print(f"🤖 Model: {get_model_info()}")
        print(f"📊 Verbose: {self.config['verbose']}")

        try:
            # Step 1: Support Agent processes inquiry
            print(f"\n{'='*70}")
            print(f"  📍 STEP 1️⃣  - SUPPORT INQUIRY RESOLUTION")
            print(f"{'='*70}")
            support_response = self.support_agent.process_inquiry(
                customer_inquiry, reference_url
            )

            # Step 2: QA Agent validates response
            print(f"\n{'='*70}")
            print(f"  📍 STEP 2️⃣  - QUALITY ASSURANCE VALIDATION")
            print(f"{'='*70}")
            qa_validation = self.qa_agent.validate_response(
                customer_inquiry, support_response, reference_url
            )

            # Results
            results = {
                "inquiry": customer_inquiry,
                "support_response": support_response,
                "qa_validation": qa_validation["validation"],
                "reference_url": reference_url,
                "support_memory": self.support_agent.memory,
                "qa_memory": self.qa_agent.memory,
            }

            print(f"\n{'='*70}")
            print(f"  ✅ WORKFLOW COMPLETED SUCCESSFULLY")
            print(f"{'='*70}\n")

            return results

        except Exception as e:
            print(f"\n{'='*70}")
            print(f"  ❌ WORKFLOW FAILED")
            print(f"{'='*70}")
            print(f"\n❌ Error: {str(e)}\n")
            raise


def create_support_crew() -> SupportCrew:
    """Factory function to create a support crew"""
    return SupportCrew()


# ============================================================================
# EXAMPLE USAGE / TESTING
# ============================================================================

if __name__ == "__main__":
    print("\n🎯 Customer Support Agent System - Testing\n")

    # Test inquiry
    inquiry = "How do I enable two-factor authentication for my account?"

    # Use Microsoft security documentation as reference
    # https://learn.microsoft.com/en-us/defender/defender-endpoint/manage-atp-post-breach-mfa
    reference_url = "https://learn.microsoft.com/en-us/defender"

    print(f"📝 Test Inquiry: {inquiry}")
    print(f"📚 Reference: {reference_url}")

    crew = create_support_crew()
    results = crew.execute(inquiry, reference_url)

    print("\n" + "=" * 70)
    print("📊 RESULTS SUMMARY")
    print("=" * 70)
    print(f"✅ Support Response:   {len(results['support_response'])} characters")
    print(f"✅ QA Validation:      {len(results['qa_validation'])} characters")
    print(
        f"✅ Support Memory:     {len(str(results['support_memory']))} characters"
    )
    print(f"✅ QA Memory:          {len(str(results['qa_memory']))} characters")
