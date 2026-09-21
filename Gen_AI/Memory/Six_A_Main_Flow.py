import sqlite3
import uuid
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver

# 1. Define the Graph State
class OrderState(TypedDict):
    order_id: str
    item: str
    quantity: int
    status: str

# 2. Define Node Functions
def review_order(state: OrderState):
    print(f"[{state['order_id']}] Step 1: Initial review completed for {state['quantity']}x {state['item']}.")
    return {"status": "Pending Approval"}

def process_approval_node(state: OrderState):
    print(f"[{state['order_id']}] Step 2: Order is holding for approval management...")
    return state

def fulfill_order(state: OrderState):
    if state["status"] == "Approved":
        print(f"[{state['order_id']}] Step 3: SUCCESS - Order fulfilled and dispatched!")
    else:
        print(f"[{state['order_id']}] Step 3: REJECTED - Order cancelled by management.")
    return state

# 3. Build and Compile the Graph Structure with SQLite and Interrupt
workflow = StateGraph(OrderState)

workflow.add_node("review", review_order)
workflow.add_node("wait_approval", process_approval_node)
workflow.add_node("fulfill", fulfill_order)

workflow.set_entry_point("review")
workflow.add_edge("review", "wait_approval")
workflow.add_edge("wait_approval", "fulfill")
workflow.add_edge("fulfill", END)

# Initialize SQLite checkpointer connected to 'orders.db'
conn = sqlite3.connect("orders.db", check_same_thread=False)
memory = SqliteSaver(conn)

# IMPORTANT: interrupt_before tells the graph to pause right before running 'fulfill'
app = workflow.compile(checkpointer=memory, interrupt_before=["fulfill"])

if __name__ == "__main__":
    print("=== MULTIPLE ORDER ENTRY PORTAL (SQLite) ===")
    print("Enter order details. Type 'done' as the item name when finished.\n")

    while True:
        item = input("Enter item name (or 'done'): ").strip()
        if item.lower() == 'done':
            break
        
        try:
            quantity = int(input("Enter quantity: ").strip())
        except ValueError:
            print("Invalid quantity. Please enter a valid integer.\n")
            continue

        thread_id = str(uuid.uuid4())
        short_id = thread_id[:8]
        config = {"configurable": {"thread_id": thread_id}}

        initial_state = {
            "order_id": short_id,
            "item": item,
            "quantity": quantity,
            "status": "Created"
        }

        print(f"\n[Submitting] Order Created -> ID: {short_id}")
        print(f"Copy this Thread ID to approve it later: {thread_id}")
        
        # Run graph; it will execute 'review' & 'wait_approval', then pause before 'fulfill'
        app.invoke(initial_state, config=config)
        print("-" * 50)