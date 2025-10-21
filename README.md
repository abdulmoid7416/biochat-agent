# BioChat: Rare Disease Query Assistant

A specialized biomedical chatbot built with Agno and BioMCP for rare genetic disease research.

## Features

- **Specialized for Rare Diseases**: Focus on epilepsy, biotinidase deficiency, Dravet syndrome, and other rare genetic conditions
- **Dual User Interface**: Optimized responses for both physicians and patients
- **BioMCP Integration**: Access to comprehensive biomedical databases
- **Real-time Chat**: Streamlit-based conversational interface
- **Evidence-based Responses**: Citations and reliability indicators
- **Medical Disclaimers**: Built-in safety warnings

## Deployment

### BioChat App (Streamlit Cloud)
This repository contains the BioChat Streamlit application.

**Deploy to Streamlit Cloud:**
1. **Fork this repository**
2. **Go to [share.streamlit.io](https://share.streamlit.io)**
3. **Connect GitHub repository**
4. **Set environment variables:**
   - `BIOMCP_SERVER_URL`: Your BioMCP server URL
   - `GROQ_API_KEY`: Your Groq API key
   - `LLM_MODEL`: `qwen/qwen3-32b`
5. **Deploy**

### BioMCP Server (Railway)
The BioMCP server is in the `biomcp-server/` directory.

**Deploy to Railway:**
1. **Create separate repository** with `biomcp-server/` contents
2. **Go to [railway.app](https://railway.app)**
3. **Connect GitHub repository**
4. **Deploy automatically**
5. **Get Railway URL**

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

**Note**: You'll need a BioMCP server running locally or remotely.

## Architecture

### Components

1. **Streamlit App** (`app.py`)
   - User interface with chat functionality
   - User type selection (Physician/Patient)
   - Chat history persistence
   - Medical disclaimers

2. **Cloud Agent** (`biochat_agent.py`)
   - Cloud-optimized BioChat agent
   - Remote BioMCP server integration
   - In-memory database for cloud deployment

3. **BioMCP Server** (Separate repository)
   - Biomedical database access
   - MCP protocol server
   - Deployed on Railway

### Data Sources

BioChat connects to multiple biomedical databases through BioMCP:

- **PubMed/PubTator3**: Research literature
- **ClinicalTrials.gov**: Clinical trials
- **MyVariant.info**: Genetic variant data
- **MyGene.info**: Gene information
- **MyDisease.info**: Disease ontologies (OMIM/Orphanet)
- **cBioPortal**: Cancer genomics
- **OpenFDA**: Drug and device data

## Usage Examples

### For Patients
- "What are the symptoms of Dravet syndrome?"
- "Are there support groups for families with rare genetic disorders?"
- "What should I ask my doctor about genetic testing?"

### For Physicians
- "What genetic variants are associated with treatment-resistant epilepsy?"
- "Show me clinical trials for rare neuromuscular disorders"
- "What biomarkers are available for undiagnosed genetic conditions?"

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `BIOMCP_SERVER_URL` | BioMCP server endpoint | Yes |
| `GROQ_API_KEY` | Groq API key for LLM | Yes |
| `LLM_MODEL` | Language model identifier | No (default: qwen/qwen3-32b) |
| `NCI_API_KEY` | NCI API key for enhanced trials | No |

### Streamlit Cloud Secrets

Set these in your Streamlit Cloud dashboard:

```toml
BIOMCP_SERVER_URL = "https://your-biomcp-server.up.railway.app/mcp"
GROQ_API_KEY = "your_groq_api_key_here"
LLM_MODEL = "qwen/qwen3-32b"
NCI_API_KEY = "your_nci_api_key_here"
```

## Medical Disclaimer

**Important**: BioChat is designed for research and informational purposes only. It does not provide medical advice, diagnoses, or treatments. Always consult qualified healthcare professionals for medical decisions.

## License

This project is licensed under the MIT License.

## Support

For technical support or feature requests, please open an issue in the project repository.