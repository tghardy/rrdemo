# RedactaRAG

A policy-aware Retrieval-Augmented Generation (RAG) system that uses **information flow control** to limit policy-violating content before it reaches the language model.

## Overview

RedactaRAG demonstrates how **information flow control** can be applied to RAG pipelines to enforce content policies. By filtering retrieved documents and context according to user-defined policies before passing them to the language model, RedactaRAG ensures that sensitive or policy-violating information is redacted before being used to generate responses.

The system includes two modes for comparison:
- **🔒 RedactaRAG Mode**: Policy-aware RAG with information flow control
- **📊 Standard RAG Mode**: Baseline RAG without policy filtering

## Key Concepts

### Information Flow Control
Information flow control is a security mechanism that tracks and restricts the flow of information through a system. In RedactaRAG, it works by:
1. Retrieving documents from a vector database
2. Applying the user's policy to filter sensitive content
3. Passing only policy-compliant context to the language model
4. Validating the final response against the policy

This approach ensures that policy-violating content never reaches the frontend model, regardless of what the model might try to generate.

## Project Structure

```
RedactaRAGDemo/
├── app.py              # Streamlit web interface
├── graph.py            # RAG pipeline and graph definitions
├── prompts.py          # LLM prompt templates
├── vectorstore.py      # Vector store initialization (optional)
├── chroma_db/          # ChromaDB vector database
├── pyproject.toml      # Project dependencies
└── README.md           # This file
```

### File Descriptions

- **app.py**: Streamlit application providing the web interface with policy configuration, model selection, and chat interface
- **graph.py**: Core logic including:
  - `invoke_rag()`: Baseline RAG function without policy filtering
  - `run_graph()`: Policy-aware RAG using LangGraph for orchestration
  - Vector database retrieval setup
- **prompts.py**: LLM prompt templates for filtering, validation, and response generation
- **chroma_db/**: ChromaDB vector store with embedded documents

## Setup Instructions

### Prerequisites
- Python 3.11+
- Ollama installed and running with models: `qwen2.5:14b`, `gemma3:1b`, `mxbai-embed-large`, or `llama2`
- uv (Python package manager)

### Installation

1. **Clone or navigate to the repository:**
   ```bash
   cd RedactaRAGDemo
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Start Ollama** (if not already running):
   ```bash
   ollama serve
   ```

   Ensure the required models are available:
   ```bash
   ollama list
   ```

4. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

   The app will open in your browser at `http://localhost:8501`

## How to Use

### 1. **Configure Settings (Sidebar)**
   - **Enter Policy**: Define what content should be filtered or redacted (e.g., "Do not mention any financial information")
   - **Select Model**: Choose between `qwen2.5:14b` or `gemma3:1b`
   - **Choose Mode**: 
     - Check to enable RedactaRAG (policy-aware with filtering)
     - Uncheck to use Standard RAG (baseline without filtering)

### 2. **Enter Questions**
   - Type your question in the chat input box
   - The app will process it based on the selected mode

### 3. **View Responses**
   - Responses are tagged with their source:
     - 🔒 **RedactaRAG**: Policy-filtered response
     - 📊 **Standard RAG**: Baseline response
   - Chat history is maintained during the session

## Understanding the Modes

### 🔒 RedactaRAG Mode (Policy-Aware)
This mode enforces information flow control:
1. Retrieves relevant documents from ChromaDB
2. **Filters context** using the policy via LLM (removes sensitive content)
3. Generates response using filtered context
4. **Validates response** against the policy
5. Rewrites if policy violations are detected

**Best for**: Enforcing strict content policies and ensuring sensitive information doesn't leak into responses.

### 📊 Standard RAG Mode (Baseline)
This mode provides baseline RAG without policy enforcement:
1. Retrieves relevant documents from ChromaDB
2. Generates response directly using the context
3. No policy filtering or validation

**Best for**: Comparing how information flow control affects response quality and understanding the baseline behavior.

## Example Usage

### Example 1: Financial Data Protection
**Policy**: "Do not mention any specific financial figures or account information"

1. Set the policy in the sidebar
2. Ask: "What should I know about my investment portfolio?"
3. **RedactaRAG** will redact sensitive financial details
4. **Standard RAG** will include all information

### Example 2: Privacy-Preserving Information
**Policy**: "Do not mention personal names, email addresses, or phone numbers"

1. Set the policy in the sidebar
2. Ask: "Who are the team members?"
3. **RedactaRAG** will redact personal identifiers
4. Compare with **Standard RAG** to see the difference

## Dependencies

- **langchain**: LLM framework and chains
- **langchain-ollama**: Ollama integration
- **langgraph**: Graph-based workflow orchestration
- **chromadb**: Vector database for retrieval
- **streamlit**: Web interface framework
- **pypdf**: PDF document handling

See `pyproject.toml` for version details.

## Architecture Flow

### RedactaRAG Pipeline
```
User Query
    ↓
Vector Database Retrieval
    ↓
Policy-Based Context Filtering (LLM)
    ↓
Filtered Context + Query
    ↓
Response Generation (LLM)
    ↓
Policy Validation (LLM)
    ↓
[If valid] → Return Response
[If invalid] → Rewrite using policy instructions
    ↓
Final Response
```

### Standard RAG Pipeline
```
User Query
    ↓
Vector Database Retrieval
    ↓
Context + Query
    ↓
Response Generation (LLM)
    ↓
Return Response
```

## Troubleshooting

### "Ollama connection refused"
- Ensure Ollama is running: `ollama serve`
- Check that models are available: `ollama list`

### "Policy is required for RedactaRAG mode"
- Enter a policy in the sidebar before asking questions in RedactaRAG mode
- Switch to Standard RAG mode if you want to test without a policy

### Slow response generation
- Check Ollama resource usage
- Try a smaller model (e.g., `gemma3:1b`)
- Ensure your system has sufficient RAM