import sqlite3
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver

# 1. Define the State schema
class OrderState(TypedDict):
    order_id: str
    amount: float
    approved: bool
    status: str

# 2. Define Nodes
def process_order(state: OrderState):
    print("  [Step 1] Processing order details...")
    return {"status": "Pending Human Review"}

def human_review_node(state: OrderState):
    print("  [Step 2] Processing decision in workflow...")
    if state.get("approved"):
        return {"status": "Approved by Manager"}
    return {"status": "Rejected by Manager"}

def fulfill_order(state: OrderState):
    print("  [Step 3] Fulfilling order and dispatching item...")
    return {"status": "Completed"}

def cancel_order(state: OrderState):
    print("  [Step 3] Order canceled. Sending notification...")
    return {"status": "Cancelled"}

def route_approval(state: OrderState) -> Literal["fulfill", "cancel"]:
    return "fulfill" if state.get("approved") else "cancel"

# 3. Build and Compile the Graph
def build_graph(checkpointer):
    workflow = StateGraph(OrderState)

    workflow.add_node("process", process_order)
    workflow.add_node("review", human_review_node)
    workflow.add_node("fulfill", fulfill_order)
    workflow.add_node("cancel", cancel_order)

    workflow.set_entry_point("process")
    workflow.add_edge("process", "review")
    workflow.add_conditional_edges(
        "review",
        route_approval,
        {"fulfill": "fulfill", "cancel": "cancel"}
    )
    workflow.add_edge("fulfill", END)
    workflow.add_edge("cancel", END)

    # Interrupt execution before reaching the 'review' node
    return workflow.compile(
        checkpointer=checkpointer,
        interrupt_before=["review"]
    )

# 4. Execution Routine
if __name__ == "__main__":
    # Use SQLite for persistent storage across separate process runs
    conn = sqlite3.connect("checkpoints.sqlite", check_same_thread=False)
    memory = SqliteSaver(conn)
    app = build_graph(memory)

    # Thread ID used to track this specific order transaction
    thread_id = "ORDER_999"
    config = {"configurable": {"thread_id": thread_id}}

    print(f"--- Program 1: Starting Workflow for Thread: {thread_id} ---")
    initial_input = {
        "order_id": "ORD-2026-X",
        "amount": 2500.00,
        "approved": False,
        "status": "New"
    }

    # Execute workflow until it hits the breakpoint
    app.invoke(initial_input, config=config)

    # Inspect current state after pause
    snapshot = app.get_state(config)
    print("\n--- Workflow Paused ---")
    print("Current State Values:", snapshot.values)
    print("Next Pending Step:", snapshot.next)
    print("Snapshot Checkpoint ID:", snapshot.config["configurable"]["checkpoint_id"])
    print("\n[PROGRAM 1 FINISHED] Execution saved to database. Run program 2 to approve/reject.")