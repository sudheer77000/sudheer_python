
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
import os
from openai import OpenAI
load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

# Shared state
class AgentState(TypedDict):
    question: str
    research: str
    analysis: str
    summary: str
    final_answer: str


# Peer Agent 1
def researcher(state: AgentState):
    response = llm.invoke(
        f"Research this topic: {state['question']}"
    )
    return {"research": response.content}


# Peer Agent 2
def analyst(state: AgentState):
    response = llm.invoke(
        f"Analyze this topic: {state['question']}"
    )
    return {"analysis": response.content}


# Peer Agent 3
def writer(state: AgentState):
    response = llm.invoke(
        f"""
        Create a short summary using:
        Research: {state['research']}
        Analysis: {state['analysis']}
        """
    )
    return {"summary": response.content}


# Coordinator Agent
def coordinator(state: AgentState):
    response = llm.invoke(
        f"""
        You are the coordinator.
        Review the peer agents' work and provide
        the final answer.

        Research: {state['research']}
        Analysis: {state['analysis']}
        Summary: {state['summary']}
        """
    )
    return {"final_answer": response.content}


# Build LangGraph
graph = StateGraph(AgentState)

graph.add_node("researcher", researcher)
graph.add_node("analyst", analyst)
graph.add_node("writer", writer)
graph.add_node("coordinator", coordinator)

# Parallel peer execution
graph.add_edge(START, "researcher")
graph.add_edge(START, "analyst")

# Both peers must finish before writer runs
graph.add_edge(["researcher", "analyst"], "writer")

# Coordinator receives combined results
graph.add_edge("writer", "coordinator")

graph.add_edge("coordinator", END)

app = graph.compile()


# Run
result = app.invoke({
    "question": "How does Generative AI help businesses?",
    "research": "",
    "analysis": "",
    "summary": "",
    "final_answer": ""
})

print(result["final_answer"])
