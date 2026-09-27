from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# -------------------------
# 1. Subgraph state
# -------------------------

class ResearchState(TypedDict):
    query: str
    result: str


# -------------------------
# 2. Subgraph nodes
# -------------------------

def search(state: ResearchState):
    return {
        "result": f"Searching for: {state['query']}"
    }


def summarize(state: ResearchState):
    return {
        "result": state["result"] + " -> summarized"
    }


# -------------------------
# 3. Build subgraph
# -------------------------

research_builder = StateGraph(ResearchState)

research_builder.add_node("search", search)
research_builder.add_node("summarize", summarize)

research_builder.add_edge(START, "search")
research_builder.add_edge("search", "summarize")
research_builder.add_edge("summarize", END)

research_graph = research_builder.compile()


# -------------------------
# 4. Parent graph
# -------------------------

class ParentState(TypedDict):
    query: str
    answer: str


def prepare(state: ParentState):
    return {
        "query": state["query"]
    }


# Use the compiled subgraph as a node
def run_research(state: ParentState):
    result = research_graph.invoke({
        "query": state["query"],
        "result": ""
    })

    return {
        "answer": result["result"]
    }


parent_builder = StateGraph(ParentState)

parent_builder.add_node("prepare", prepare)
parent_builder.add_node("research", run_research)

parent_builder.add_edge(START, "prepare")
parent_builder.add_edge("prepare", "research")
parent_builder.add_edge("research", END)

parent_graph = parent_builder.compile()


# -------------------------
# 5. Run parent graph
# -------------------------

result = parent_graph.invoke({
    "query": "Explain About Indian Institute of Technology?",
    "answer": ""
})

print(result)