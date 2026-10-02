from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
import time


# ============================================================
# 1. MAIN GRAPH STATE
# ============================================================

class State(TypedDict):
    """
    State shared by the overall graph.
    """

    topics: list[str]

    # Multiple workers will produce results.
    # `add` tells LangGraph to combine those results.
    results: Annotated[list[str], add]


# ============================================================
# 2. WORKER STATE
# ============================================================

class WorkerState(TypedDict):
    """
    State received by ONE worker execution.
    """

    topic: str

    # Worker can contribute its result here.
    results: Annotated[list[str], add]


# ============================================================
# 3. DISPATCHER
# ============================================================

def distribute_topics(state: State):
    """
    Take the list of topics and create one worker
    execution for each topic.
    """

    print("\n--- DISTRIBUTING TOPICS ---")

    sends = []

    for topic in state["topics"]:

        print(f"Creating worker for: {topic}")

        sends.append(
            Send(
                "research_worker",
                {
                    "topic": topic
                }
            )
        )

    return sends


# ============================================================
# 4. WORKER
# ============================================================

def research_worker(state: WorkerState):
    """
    This function represents ONE unit of work.

    It receives ONE topic.
    """

    topic = state["topic"]

    print(f"\nWorker started for: {topic}")

    # Pretend that research takes time
    time.sleep(2)

    result = f"Research completed for {topic}"

    print(f"Worker finished for: {topic}")

    return {
        "results": [result]
    }


# ============================================================
# 5. BUILD THE GRAPH
# ============================================================

builder = StateGraph(State)


# ------------------------------------------------------------
# NODE
# ------------------------------------------------------------
# Register the Python function as a graph node.
#
# Graph node name:
#     "research_worker"
#
# Python function:
#     research_worker
# ------------------------------------------------------------

builder.add_node(
    "research_worker",
    research_worker
)


# ------------------------------------------------------------
# START -> DISPATCHER
# ------------------------------------------------------------
#
# When the graph starts:
#
# START
#   |
#   v
# distribute_topics()
#
# distribute_topics() returns multiple Send objects.
# ------------------------------------------------------------

builder.add_conditional_edges(
    START,
    distribute_topics
)


# ------------------------------------------------------------
# WORKER -> END
# ------------------------------------------------------------
#
# After each worker finishes:
#
# research_worker
#       |
#       v
#      END
# ------------------------------------------------------------

builder.add_edge(
    "research_worker",
    END
)


# ============================================================
# 6. COMPILE GRAPH
# ============================================================

graph = builder.compile()


# ============================================================
# 7. RUN GRAPH
# ============================================================

initial_state = {
    "topics": [
        "AI",
        "Python",
        "LangGraph"
    ],
    "results": []
}

result = graph.invoke(initial_state)


# ============================================================
# 8. DISPLAY FINAL RESULT
# ============================================================

print("\n==============================")
print("FINAL RESULT")
print("==============================")

print(result)
