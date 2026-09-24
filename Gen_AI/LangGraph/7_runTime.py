from dataclasses import dataclass
from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.runtime import Runtime


# -------------------------
# Runtime Context
# -------------------------
@dataclass
class Context:
    user_id: str


# -------------------------
# Graph State
# -------------------------
class State(TypedDict):
    order_id: str
    status: str


# -------------------------
# Node
# -------------------------
def check_order(state: State, runtime: Runtime[Context]):

    order_id = state["order_id"]
    user_id = runtime.context.user_id

    return {
        "order_id": order_id,
        "status": f"Order for User {user_id} is Shipped"
    }


# -------------------------
# Build Graph
# -------------------------
builder = StateGraph(
    State,
    context_schema=Context
)

builder.add_node("check_order", check_order)

builder.add_edge(START, "check_order")
builder.add_edge("check_order", END)

graph = builder.compile()


# -------------------------
# User Input
# -------------------------
user_id = input("Please Enter User ID: ")
order_id = input("Please Enter Order ID: ")


# -------------------------
# Run Graph
# -------------------------
result = graph.invoke(
    {"order_id": order_id, "status": ""},
    context=Context(user_id=user_id)
)


# -------------------------
# Output
# -------------------------
print("\nResult:")
print(result)