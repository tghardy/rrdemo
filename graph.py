from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import Chroma
from langgraph.graph import StateGraph, START, END
from prompts import filterer_prompt, validation_prompt, frontend_prompt
from typing_extensions import TypedDict


## Initialize DB

def get_retriever():
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")

    db = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )

    return db.as_retriever(search_kwargs={"k":3})

db = get_retriever()


## Define State class

class State(TypedDict):
    question: str
    context: str
    llm: ChatOllama
    response: str
    policy: str
    clean_response: str
    instructions: str

graph = StateGraph(State)

def get_context(state):

    docs = db.invoke(state["question"])

    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = filterer_prompt(state["policy"], context)
    state["context"] = state["llm"].invoke(prompt).content

    return state


def response(state):
    prompt = frontend_prompt(state["context"], state["question"])
    state["response"] = state["llm"].invoke(prompt).content
    print("Initial response:", state["response"])
    return state


def evaluate(state):
    prompt = validation_prompt(state['response'], state["policy"])
    response = state["llm"].invoke(prompt)
    state["instructions"] = response.content

    return state

def decide_node(state):
    if 'good' in state["instructions"].strip().lower():
        return "print_response"
    else:
        return "rewrite"
    
def rewrite(state):
    prompt = f'Rewrite this TEXT according to these INSTRUCTIONS: {state["instructions"]} \n\n TEXT: {state["response"]}'
    state["response"] = state["llm"].invoke(prompt).content
    return state

def print_response(state):
    print(state["response"])
    return state

graph.add_node("filter_context", get_context)
graph.add_node("response", response)
graph.add_node("evaluate", evaluate)
graph.add_node("rewrite", rewrite)
graph.add_node("print_response", print_response)


graph.add_edge(START, "filter_context")
graph.add_edge("filter_context", "response")
graph.add_edge("response", "evaluate")
graph.add_conditional_edges(
    "evaluate",
    decide_node,
    {
        "print_response": "print_response",
        "rewrite": "rewrite"
    }
)

graph.add_edge("rewrite", "evaluate")
graph.add_edge("print_response", END)


GRAPH = graph.compile()


def run_graph(prompt, policy, llm):
    print("Running graph...")
    s = State(
        question=prompt,
        context="",
        llm=llm,
        response="",
        policy=policy,
        clean_response="",
        instructions=""
    )
    GRAPH.invoke(s)


run_graph("How does linear regression work?", policy="Do not mention gradient descent.", llm=ChatOllama(model="lfm2.5-thinking"))