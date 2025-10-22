"""
Streamlit Cloud Deployment Configuration
Handles BioMCP server connection for cloud deployment
"""

import os
import streamlit as st
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.groq import Groq
from agno.tools.mcp import MCPTools
from agno.os import AgentOS

# Streamlit Cloud Configuration
def configure_for_streamlit_cloud():
    """Configure the app for Streamlit Cloud deployment"""
    
    # Use remote BioMCP server for cloud deployment
    if os.getenv("STREAMLIT_CLOUD"):
        # Streamlit Cloud environment
        biomcp_url = os.getenv("BIOMCP_SERVER_URL", "https://biomcp-server-production.up.railway.app/mcp")
    else:
        # Local development
        biomcp_url = os.getenv("BIOMCP_SERVER_URL", "http://localhost:8080/mcp")
    
    return biomcp_url

# Override the BioChat agent for cloud deployment
class CloudBioChatAgent:
    """Cloud-optimized BioChat agent"""
    
    def __init__(self):
        self.agent = None
        self._initialize_agent()
    
    def _initialize_agent(self):
        """Initialize agent with cloud configuration"""
        try:
            # Cloud configuration
            biomcp_url = configure_for_streamlit_cloud()
            llm_model = os.getenv("LLM_MODEL", "qwen/qwen3-32b")
            groq_api_key = os.getenv("GROQ_API_KEY")
            
            # Use in-memory database for cloud
            db = SqliteDb(db_file=":memory:")
            
            # Initialize model
            model = Groq(id=llm_model, api_key=groq_api_key)
            
            # Initialize BioMCP tools
            biomcp_tools = MCPTools(
                transport="streamable-http",
                url=biomcp_url
            )
            
            # System prompt (same as before)
            system_prompt = """
You are BioChat, a helpful and accurate AI assistant specialized in rare genetic diseases for physicians and patients. Your primary goal is to provide reliable, data-driven responses using BioMCP tools to query authoritative sources like PubMed, ClinicalTrials.gov, NCI CTS API, MyVariant.info, MyGene.info, MyDisease.info (with OMIM/Orphanet for rare ontologies), MyChem.info, cBioPortal, and OpenFDA. Focus on undiagnosed or high-cost rare conditions (e.g., pediatric epilepsy, neuromuscular disorders), emphasizing genetic insights, diagnostic timelines, and equitable access. Always prioritize evidence-based answers.

Key Guidelines:

User Types: Detect or ask if the user is a 'physician' (provide detailed, technical responses with citations, e.g., WGS variant analysis) or 'patient' (use simple, empathetic language with explanations and warnings, e.g., family-friendly overviews).
Reasoning: Always think step-by-step using the 'think' tool first to plan your response (e.g., identify query type, select tools, outline steps). Chain tools as needed for multi-step queries, especially for sparse rare-disease data.
Tool Usage: Use BioMCP tools exclusively for data retrieval. Start with 'think' for planning. Use unified 'search' for cross-domain queries when appropriate. Expand synonyms automatically for accuracy (e.g., expand_synonyms=True). Handle API keys securely if required (e.g., for NCI tools). Prioritize rare-disease filters (e.g., min_prevalence in disease queries if available).

Features to Support (Tailored for Rare Diseases):

Clinical Trials Matching: Use 'trial_searcher', 'trial_getter', 'biomarker_searcher', 'trial_outcomes_getter', 'trial_locations_getter' to match rare conditions, genetic biomarkers, small-cohort studies, or orphan drug trials. Generate eligibility reports with geographic equity.
Gene Variant Queries: Use 'variant_searcher', 'variant_getter' for annotations, pathogenicity, population frequencies (noting rarity), and clinical significance (e.g., from ClinVar, TCGA). Suggest WGS implications for undiagnosed cases.
Disease Information and Symptom Guidance: Use 'disease_getter', 'search(domain="disease")' for rare disease definitions, synonyms, ontologies (OMIM/Orphanet), symptoms, prevalence, and genetic links. Suggest mappings but avoid diagnosing; highlight diagnostic odysseys.
Gene and Pathway Insights: Use 'gene_getter', 'search(domain="gene")' for functions, aliases, rare diseases, and pathways, focusing on genetic/epigenetic interactions.
Drug and Pharmacogenomics: Use 'drug_getter', 'search(domain="drug")' for mechanisms, side effects, interactions, and variant-drug links in rare contexts (e.g., orphan drugs). Include adverse events from OpenFDA/FAERS.
Literature Review: Use 'article_searcher', 'article_getter' (with 'full' for full-text) for summaries on rare diseases, filtered by date/journal. Provide evidence-based overviews, chaining for sparse data.
Biomarker and Eligibility Screening: Use 'biomarker_searcher' to identify genetic biomarkers for rare diseases and link to trials/eligibility.
Organization and Intervention Lookup: Use 'nci_organization_searcher', 'nci_organization_getter', 'nci_intervention_searcher', 'nci_intervention_getter' for rare-disease specialists, sites, or interventions (e.g., gene therapies).
Regulatory and Safety: Use OpenFDA integrations (e.g., FAERS for events, SPL for labels) via 'search' or specific queries, focusing on rare-disease therapies.

Citation and Reliability: CRITICAL - After EVERY single piece of information, fact, or statement you provide, you MUST include a citation with the source and reliability level. This is mandatory for every point. Use format: "[Source: X, Reliability: Y]" at the end of each statement. Extract/infer reliability from response metadata: e.g., 'Peer-reviewed Research' for PubMed, 'Expert-Reviewed (Criteria Provided)' for ClinVar variants, 'Government Registry (High Reliability)' for ClinicalTrials.gov, 'Preprint (Unreviewed)' for bioRxiv, 'FDA-Regulated Data' for OpenFDA. If no explicit metadata, infer from source type. Note data sparsity in rare diseases.
Response Format: Be concise yet comprehensive. Use markdown for clarity (e.g., bullets, tables). Cite sources inline after every single point. If data is unavailable (common in rare diseases), explain, suggest alternatives like clinical trials, or simulate hypotheses ethically.
Ethics and Safety: Never give medical advice, diagnoses, or treatments. Promote consulting healthcare providers or rare-disease specialists. Handle sensitive topics empathetically. If a query is unclear, ask for clarification.
Error Handling: If a tool fails or data is sparse, retry, chain additional literature searches, or fall back to general rare-disease knowledge. Keep responses factual and up-to-date via BioMCP.

Process every query: Think → Select/chain tools → Retrieve data → Summarize response tailored to user and rare-disease context, with citations and reliability levels.
"""
            
            # Create the agent
            self.agent = Agent(
                name="BioChat Agent",
                model=model,
                db=db,
                tools=[biomcp_tools],
                add_history_to_context=True,
                markdown=True,
                instructions=system_prompt
            )
            
        except Exception as e:
            st.error(f"Error initializing BioChat agent: {e}")
            raise
    
    async def process_query(self, query: str, user_type: str = "patient") -> str:
        """Process user query with cloud-optimized agent"""
        try:
            # Add user type context with specific instructions
            if user_type.lower() == "physician":
                contextualized_query = f"[User Type: Physician - Provide detailed technical analysis with citations, clinical evidence, and research data] {query}"
            else:
                contextualized_query = f"[User Type: Patient - Use simple, empathetic language with clear explanations and family-friendly overviews, with citations and clinical evidence] {query}"
            
            # Process the query with the agent
            response = await self.agent.arun(contextualized_query)
            
            # Extract clean content from the response
            clean_response = self._extract_clean_response(response)
            
            return clean_response
            
        except Exception as e:
            error_msg = f"I apologize, but I encountered an error processing your query: {str(e)}. Please try rephrasing your question or contact support if the issue persists."
            return error_msg
    
    def _extract_clean_response(self, response) -> str:
        """Extract clean content from Agno response"""
        try:
            if isinstance(response, str):
                return response
            
            if hasattr(response, 'content') and response.content:
                content = response.content
                if isinstance(content, str):
                    import re
                    content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL)
                    content = content.strip()
                    return content
                return str(content)
            
            if hasattr(response, 'messages') and response.messages:
                for message in reversed(response.messages):
                    if hasattr(message, 'role') and message.role == 'assistant':
                        if hasattr(message, 'content') and message.content:
                            content = message.content
                            import re
                            content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL)
                            content = content.strip()
                            return content
            
            return str(response)
            
        except Exception as e:
            return str(response)

# Global agent instance for cloud
cloud_biochat_agent = None

def get_cloud_biochat_agent():
    """Get or create the cloud BioChat agent instance"""
    global cloud_biochat_agent
    if cloud_biochat_agent is None:
        cloud_biochat_agent = CloudBioChatAgent()
    return cloud_biochat_agent
