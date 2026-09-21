from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

# 1. Define the State schema
class OrderState(TypedDict):
    order_id: str
    amount: float
    approved: bool
    status: str

# 2. Define Node Functions
def process_order(state: OrderState):
    print("  [Node] Processing order calculations...")
    return {"status": "Pending Review"}

def human_review_node(state: OrderState):
    """
    This node runs after the human makes a decision.
    State['approved'] will be set by the human prior to resuming.
    """
    print("  [Node] Running human review node logic...")
    if state.get("approved"):
        return {"status": "Approved"}
    else:
        return {"status": "Rejected"}

def fulfill_order(state: OrderState):
    print("  [Node] Fulfilling order and sending confirmation...")
    return {"status": "Completed"}

def cancel_order(state: OrderState):
    print("  [Node] Canceling order and notifying customer...")
    return {"status": "Cancelled"}

# 3. Define Conditional Router
def route_approval(state: OrderState) -> Literal["fulfill", "cancel"]:
    if state.get("approved"):
        return "fulfill"
    return "cancel"

# 4. Build the Graph
workflow = StateGraph(OrderState)

workflow.add_node("process", process_order)
workflow.add_node("review", human_review_node)
workflow.add_node("fulfill", fulfill_order)
workflow.add_node("cancel", cancel_order)

workflow.set_entry_point("process")
workflow.add_edge("process", "review")

# Conditional path after review node completes
workflow.add_conditional_edges(
    "review",
    route_approval,
    {
        "fulfill": "fulfill",
        "cancel": "cancel"
    }
)

workflow.add_edge("fulfill", END)
workflow.add_edge("cancel", END)

# 5. Compile with Checkpointer and Breakpoint
memory = MemorySaver()

# Interrupt BEFORE running the 'review' node
app = workflow.compile(
    checkpointer=memory,
    interrupt_before=["review"]
)

# Configuration with a unique thread_id
config = {"configurable": {"thread_id": "order_tx_999"}}

# =====================================================================
# STEP 1: Start Execution (Will stop at the breakpoint)
# =====================================================================
print("--- 1. Starting Execution ---")
initial_input = {"order_id": "ORD-1234", "amount": 1500.00, "approved": False, "status": "New"}

# Executing the workflow
app.invoke(initial_input, config=config)

# =====================================================================
# STEP 2: Inspect State Snapshot during Pause
# =====================================================================
print("\n--- 2. Inspecting State Snapshot (Paused) ---")
snapshot = app.get_state(config)

print(f"Current Values: {snapshot.values}")
print(f"Next Pending Node (.next): {snapshot.next}")
print(f"Checkpoint ID: {snapshot.config['configurable']['checkpoint_id']}")

# Verify that execution is indeed paused at 'review'
if "review" in snapshot.next:
    print("\n>> Flow paused successfully before 'review' node. Awaiting human decision.")

# =====================================================================
# STEP 3A: Option A - Human APPROVES the Request
# =====================================================================
def simulate_human_approval():
    print("\n--- 3A. Human Decision: APPROVE ---")
    
    # Update state snapshot to mark as approved
    app.update_state(config, {"approved": True})
    
    # Resume execution by passing None as input
    final_result = app.invoke(None, config=config)
    print("Final State Output:", final_result)


# =====================================================================
# STEP 3B: Option B - Human REJECTS the Request
# =====================================================================
def simulate_human_rejection():
    print("\n--- 3B. Human Decision: REJECT ---")
    
    # Update state snapshot to mark as rejected
    app.update_state(config, {"approved": False})
    
    # Resume execution by passing None as input
    final_result = app.invoke(None, config=config)
    print("Final State Output:", final_result)

# Toggle between approval or rejection demo:
simulate_human_approval()
# simulate_human_rejection()