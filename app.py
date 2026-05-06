import streamlit as st
from langchain_ollama import ChatOllama
from graph import run_graph, invoke_rag

st.set_page_config(page_title="RedactaRAG", layout="wide")

# Inject CSS to fix the chat input background
st.markdown(
    """
    <style>
        /* Target the chat input container */
        [data-testid="stChatInput"] {
            background-color: #002E5D !important; /* Change to white, or your main backgroundColor */
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Can you break RedactaRAG?")
st.text("Attempt to get the RedactaRAG LLM to violate the policy on the left. Then, see how easy it is to break a base LLM!")


# Initialize chat history
if "redactarag_messages" not in st.session_state:
    st.session_state.redactarag_messages = []

if "standard_messages" not in st.session_state:
    st.session_state.standard_messages = []

def reset_memory():
    st.session_state.redactarag_messages = []
    st.session_state.standard_messages = []

# Sidebar configuration
with st.sidebar:
    left, cent, last_co = st.columns([1,4,1])
    with cent:
        st.image("monogram.png", width=200)
    st.header("⚙️ Configuration")
    
    # Policy textbox
    policy = st.text_area(
        "Enter Policy:",
        value="Do not talk about any of the linear regression assumptions.",
        placeholder="E.g., Do not mention any sensitive information...",
        height=120
    )
    
    # Model selection dropdown
    model_choice = st.selectbox(
        "Select Model:",
        options=["qwen2.5:14b", "gemma3:1b", "gemma4:31b"],
        index=0
    )

    temperature = st.slider("Model Temperature:", min_value=0.0, max_value=1.0)
    
    # # Mode selection checkbox
    # use_graph = st.checkbox(
    #     "Use RedactaRAG (policy-aware mode)",
    #     value=True,
    #     help="Enabled: Use RedactaRAG with policy filtering. Disabled: Use a standard RAG system."
    # )

    use_graph = True
    
    mode_label = "run_graph (policy-aware)" if use_graph else "invoke_rag (baseline)"

    st.button("Reset model", on_click=reset_memory)
    
    # Information section
    st.divider()
    st.subheader("ℹ️ About RedactaRAG")
    st.markdown("""
    **RedactaRAG** uses **information flow control** to limit policy-violating content before it reaches the frontend model.
    
    - 🔒 **RedactaRAG Mode**: Applies your policy to retrieved context, filtering sensitive information before generating responses
    - 📊 **System Prompt Defense**: Baseline RAG system using the policy within system prompts
    """)


col1, col2 = st.columns(2)
cols = [col1, col2]
for col in cols:
    if col is col1:
        with col:
            st.header("RedactaRAG Defense")
    if col is col2:
        with col: 
            st.header("System Prompt Defense")

chat1, chat2 = st.columns(2, vertical_alignment="bottom", border=True, gap="medium")
chats = [chat1, chat2]

## Render chat history
with chat1:
    for msg in st.session_state.redactarag_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])


with chat2:
    for msg in st.session_state.standard_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])


# New chat input
user_input = st.chat_input("Enter your prompt...")
if user_input:

    st.session_state.redactarag_messages.append({"role": "user", "content": user_input})
    st.session_state.standard_messages.append({"role": "user", "content": user_input})

    for col in chats:
        with col:
            with st.chat_message("user"):
                st.markdown(user_input)
            
            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("Generating response..."):
                    try:
                        # Initialize LLM with selected model
                        llm = ChatOllama(model=model_choice, temperature=temperature, disable_streaming=False)
                        
                        if col is chat1:
                            # Use run_graph (requires policy)
                            if not policy.strip():
                                st.warning("⚠️ Policy is required for run_graph mode. Please enter a policy in the sidebar.")
                            else:
                                response, context = run_graph(str(st.session_state.redactarag_messages), policy, llm)
                                st.caption("🔒 RedactaRAG")
                                st.markdown(response)
                                st.session_state.redactarag_messages.append({
                                    "role": "assistant",
                                    "content": response,
                                    "model_type": "redactarag"
                                })

                                # with st.expander("View the model's context:"):
                                #     st.markdown(context)
                        else:
                            # Use baseline invoke_rag
                            response, context = invoke_rag(str(st.session_state.standard_messages), llm)
                            st.caption("📊 Standard RAG")
                            st.markdown(response)
                            st.session_state.standard_messages.append({
                                "role": "assistant",
                                "content": response,
                                "model_type": "standard_rag"
                            })

                        with st.expander("View the context for this response:"):
                            st.markdown(context)
                    
                    except Exception as e:
                        st.error(f"Error generating response: {str(e)}")
