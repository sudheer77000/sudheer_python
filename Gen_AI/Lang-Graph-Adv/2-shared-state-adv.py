
import time
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# Shared state between parent and subgraph
class OrderState(TypedDict):
    order_id: str
    item: str
    quantity: int
    status: str
    inventory_reserved: bool
    payment_status: str


# ---------- Subgraph nodes ----------

def validate_order(state: OrderState):
    print("\n[SUBGRAPH] Validating order...")
    time.sleep(1)

    if state["quantity"] <= 0:
        return {"status": "invalid"}

    return {"status": "validated"}


def reserve_inventory(state: OrderState):
    print("[SUBGRAPH] Reserving inventory...")
    time.sleep(1)

    return {
        "inventory_reserved": True,
        "status": "inventory_reserved",
    }


# Build the subgraph
sub_builder = StateGraph(OrderState)

sub_builder.add_node("validate", validate_order)
sub_builder.add_node("reserve", reserve_inventory)

sub_builder.add_edge(START, "validate")
sub_builder.add_edge("validate", "reserve")
sub_builder.add_edge("reserve", END)

order_subgraph = sub_builder.compile()


# ---------- Parent graph nodes ----------

def process_payment(state: OrderState):
    print("\n[PARENT] Processing payment...")
    time.sleep(1)

    if not state["inventory_reserved"]:
        return {
            "payment_status": "not_processed",
            "status": "failed",
        }

    return {
        "payment_status": "paid",
        "status": "completed",
    }


# Build the parent graph
parent_builder = StateGraph(OrderState)

parent_builder.add_node("order_workflow", order_subgraph)
parent_builder.add_node("payment", process_payment)

parent_builder.add_edge(START, "order_workflow")
parent_builder.add_edge("order_workflow", "payment")
parent_builder.add_edge("payment", END)

graph = parent_builder.compile()


# ---------- Real-time streaming ----------

initial_state = {
    "order_id": "ORD-101",
    "item": "Laptop",
    "quantity": 1,
    "status": "new",
    "inventory_reserved": False,
    "payment_status": "pending",
}

print("Starting order workflow...\n")

for chunk in graph.stream(
    initial_state,
    stream_mode="updates",
    subgraphs=True,
):
    namespace, updates = chunk

    location = "SUBGRAPH" if namespace else "PARENT"

    print(f"[{location}] State update: {updates}")

print("\nFinal state:")
print(graph.invoke(initial_state))
