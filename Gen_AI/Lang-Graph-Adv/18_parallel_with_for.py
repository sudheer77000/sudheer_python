
import time
from typing import TypedDict, Annotated
from operator import add

from langgraph.graph import StateGraph, START, END


# 1. Shared State with reducer
class State(TypedDict):
    results: Annotated[list, add]


# 2. Three parallel nodes
def node_1(state):
    print("Node 1 started")
    time.sleep(10)
    print("Node 1 completed")

    return {"results": ["Result from Node 1"]}


def node_2(state):
    print("Node 2 started")
    time.sleep(10)
    print("Node 2 completed")

    return {"results": ["Result from Node 2"]}


def node_3(state):
    print("Node 3 started")
    time.sleep(10)
    print("Node 3 completed")

    return {"results": ["Result from Node 3"]}


# 3. Register nodes
nodes = {
    "node_1": node_1,
    "node_2": node_2,
    "node_3": node_3
}

graph = StateGraph(State)

for name, function in nodes.items():
    graph.add_node(name, function)


# 4. FAN-OUT: Execute all three nodes in parallel
for name in nodes:
    graph.add_edge(START, name)


# 5. FAN-IN: Wait for all three nodes
graph.add_edge(list(nodes.keys()), END)


# 6. Compile graph
app = graph.compile()


# 7. Execute graph
if __name__ == "__main__":

    start_time = time.time()

    result = app.invoke({
        "results": []
    })

    end_time = time.time()

    print("\n========== FINAL RESULTS ==========")

    for item in result["results"]:
        print(item)

    print("\nTotal execution time:",
          round(end_time - start_time, 2), "seconds")
