"""
BioChat Streamlit Application
A biomedical chatbot specialized for rare genetic diseases
Optimized for Streamlit Cloud deployment
"""

import streamlit as st
import asyncio
from biochat_agent import get_cloud_biochat_agent

# Configure Streamlit page
st.set_page_config(
    page_title="BioChat: Rare Disease Query Assistant",
    page_icon="🧬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .tagline {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .description {
        font-size: 1.1rem;
        color: #444;
        text-align: center;
        margin-bottom: 2rem;
        line-height: 1.6;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }
    .user-type-selector {
        margin: 2rem 0;
        text-align: center;
    }
    .query-section {
        margin: 2rem auto;
        max-width: 800px;
        text-align: center;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .disclaimer {
        background-color: #fff3e0;
        border: 1px solid #ff9800;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
        text-align: center;
    }
    .example-queries {
        background-color: #e8f5e8;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .container {
        max-width: 800px;
        margin: 0 auto;
        padding: 0 1rem;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "user_type" not in st.session_state:
        st.session_state.user_type = "Patient"
    if "agent_initialized" not in st.session_state:
        st.session_state.agent_initialized = False

def display_header():
    """Display main header and description"""
    st.markdown('<div class="main-header">🧬 BioChat</div>', unsafe_allow_html=True)
    st.markdown('<div class="tagline">Rare Disease Query Assistant</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="description">
    Get evidence-based answers from authoritative databases including PubMed, ClinicalTrials.gov, 
    OMIM, ClinVar, cBioPortal, and more. Specialized for rare genetic diseases like 
    epilepsy, neuromuscular disorders, and metabolic conditions.
    </div>
    """, unsafe_allow_html=True)

def display_user_type_selector():
    """Display user type selector"""
    st.markdown('<div class="user-type-selector">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        user_type = st.selectbox(
            "Select your role:",
            ["Patient", "Physician"],
            index=0 if st.session_state.user_type == "Patient" else 1,
            key="user_type_selector"
        )
        
        if user_type != st.session_state.user_type:
            st.session_state.user_type = user_type
            st.session_state.messages = []  # Clear chat history when user type changes
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)


def display_chat_history():
    """Display chat history"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def add_message(role: str, content: str):
    """Add a message to chat history"""
    st.session_state.messages.append({"role": role, "content": content})

async def process_user_query(query: str) -> str:
    """Process user query with the cloud BioChat agent"""
    try:
        # Get the cloud agent
        agent = get_cloud_biochat_agent()
        
        # Process the query
        response = await agent.process_query(query, st.session_state.user_type.lower())
        return response
        
    except Exception as e:
        return f"I apologize, but I encountered an error: {str(e)}. Please try again or contact support if the issue persists."

def main():
    """Main Streamlit application"""
    
    # Initialize session state
    initialize_session_state()
    
    # Main container for centered layout
    st.markdown('<div class="container">', unsafe_allow_html=True)
    
    # Display header and description
    display_header()
    
    # Display user type selector
    display_user_type_selector()
    
    
    # Clear chat button (only show if there are messages)
    if st.session_state.messages:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🗑️ Clear Chat History", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
    
    # Chat interface section
    st.markdown('<div class="query-section">', unsafe_allow_html=True)
    
    # Display chat history
    display_chat_history()
    
    # Chat input
    if prompt := st.chat_input("Ask about rare genetic diseases..."):
        # Add user message to chat history
        add_message("user", prompt)
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Process query and display response
        with st.chat_message("assistant"):
            with st.spinner("🔍 Searching biomedical databases..."):
                try:
                    # Process the query asynchronously
                    response = asyncio.run(process_user_query(prompt))
                    
                    # Display the response
                    st.markdown(response)
                    
                    # Add assistant response to chat history
                    add_message("assistant", response)
                    
                except Exception as e:
                    error_response = f"I apologize, but I encountered an error processing your query: {str(e)}. Please try again."
                    st.error(error_response)
                    add_message("assistant", error_response)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close query-section
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close container

if __name__ == "__main__":
    main()
