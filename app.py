import streamlit as st
from langchain_ollama import ChatOllama
from graph import run_graph, invoke_rag

st.set_page_config(page_title="RedactaRAG", layout="wide")

st.title("RedactaRAG Chatbot")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Policy textbox
    policy = st.text_area(
        "Enter Policy:",
        placeholder="E.g., Do not mention any sensitive information...",
        height=120
    )
    
    # Model selection dropdown
    model_choice = st.selectbox(
        "Select Model:",
        options=["qwen2.5:14b", "gemma3:1b"],
        index=0
    )
    
    # Mode selection checkbox
    use_graph = st.checkbox(
        "Use RedactaRAG (policy-aware mode)",
        value=True,
        help="Enabled: Use RedactaRAG with policy filtering. Disabled: Use a standard RAG system."
    )
    
    mode_label = "run_graph (policy-aware)" if use_graph else "invoke_rag (baseline)"
    
    # Information section
    st.divider()
    st.subheader("ℹ️ About RedactaRAG")
    st.markdown("""
    **RedactaRAG** uses **information flow control** to limit policy-violating content before it reaches the frontend model.
    
    - 🔒 **RedactaRAG Mode**: Applies your policy to retrieved context, filtering sensitive information before generating responses
    - 📊 **Standard RAG Mode**: Baseline RAG system using the policy within system prompts
    
    Toggle between modes to compare how information flow control affects response generation and how different policies and prompts impact model performance.
    """)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # Display model tag for assistant messages
        if message["role"] == "assistant" and "model_type" in message:
            model_tag = "🔒 RedactaRAG" if message["model_type"] == "redactarag" else "📊 Standard RAG"
            st.caption(model_tag)
        st.markdown(message["content"])

# Chat input
if user_input := st.chat_input("Enter your question or prompt..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Generating response..."):
            try:
                # Initialize LLM with selected model
                llm = ChatOllama(model=model_choice)
                
                if use_graph:
                    # Use run_graph (requires policy)
                    if not policy.strip():
                        st.warning("⚠️ Policy is required for run_graph mode. Please enter a policy in the sidebar.")
                    else:
                        response = run_graph(user_input, policy, llm)
                        st.caption("🔒 RedactaRAG")
                        st.markdown(response)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response,
                            "model_type": "redactarag"
                        })
                else:
                    # Use baseline invoke_rag
                    response = invoke_rag(user_input, llm)
                    st.caption("📊 Standard RAG")
                    st.markdown(response)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response,
                        "model_type": "standard_rag"
                    })
            
            except Exception as e:
                st.error(f"Error generating response: {str(e)}")
