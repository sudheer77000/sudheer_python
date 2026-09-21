import os
import logging
from dotenv import load_dotenv
load_dotenv()

# 1. Enable console logging to monitor outgoing trace requests
logging.basicConfig(level=logging.INFO)

# 2. Configure LangSmith tracing and EU endpoint environment variables
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = "langgraph-learning"
os.environ["LANGCHAIN_ENDPOINT"] = "https://eu.api.smith.langchain.com"

# 3. Import LangGraph modules after environment variables are set
from typing import TypedDict
from langgraph.graph import StateGraph, END

# Define the graph state
class State(TypedDict):
    text: str

# Define a simple processing node
def uppercase_node(state: State):
    print("Executing node...")
    return {"text": state["text"].upper()}

# Build the workflow graph
workflow = StateGraph(State)
workflow.add_node("uppercase", uppercase_node)
workflow.set_entry_point("uppercase")
workflow.add_edge("uppercase", END)

# Compile the graph
app = workflow.compile()

if __name__ == "__main__":
    print("Running graph execution (tracing enabled)...")
    
    # Invoking the graph automatically creates a trace in your LangSmith project
    result = app.invoke({"text": "hello langsmith tracing"})
    
    print("Graph Output:", result)