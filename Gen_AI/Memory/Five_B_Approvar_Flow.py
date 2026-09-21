import sqlite3

# Import state and graph compiler from program_1
from Five_A_MainFlow import build_graph
from langgraph.checkpoint.sqlite import SqliteSaver

if __name__ == "__main__":
    # 1. Connect to the SAME persistent database
    conn = sqlite3.connect("checkpoints.sqlite", check_same_thread=False)
    memory = SqliteSaver(conn)
    app = build_graph(memory)

    # 2. Specify the thread ID to resume
    thread_id = "ORDER_999"
    config = {"configurable": {"thread_id": thread_id}}

    print(f"--- Program 2: Human Approval Interface ---")
    print(f"Fetching state snapshot for thread: '{thread_id}'...")

    # Read existing state from database
    snapshot = app.get_state(config)

    if not snapshot.values:
        print("Error: No active workflow snapshot found for this thread ID.")
        exit()

    print("\n[Pending Request Found]")
    print(f"  Order ID : {snapshot.values.get('order_id')}")
    print(f"  Amount   : ${snapshot.values.get('amount')}")
    print(f"  Status   : {snapshot.values.get('status')}")
    print(f"  Next Step: {snapshot.next}")

    # 3. Prompt human for approval decision
    user_choice = input("\nDo you want to approve this order? (yes/no): ").strip().lower()
    is_approved = user_choice in ["yes", "y"]

    print("\n--- Resuming Workflow Execution ---")

    # 4. Inject human decision into the state snapshot
    app.update_state(config, {"approved": is_approved})

    # 5. Resume execution by passing None (picks up right at the 'review' node)
    final_output = app.invoke(None, config=config)

    print("\n--- Workflow Execution Completed ---")
    print("Final State Values:", final_output)