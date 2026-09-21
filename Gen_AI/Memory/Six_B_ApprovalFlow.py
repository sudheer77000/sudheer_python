# Import the shared state, compiled app, and database connection from Program 1
from Six_A_Main_Flow import app, OrderState

if __name__ == "__main__":
    print("=== APPROVAL WORKFLOW PORTAL (SQLite - Imported) ===")
    print("Process multiple orders by providing their Thread IDs.\n")

    while True:
        thread_id = input("Enter Thread ID to review (or type 'exit' to quit): ").strip()
        if thread_id.lower() == 'exit':
            break

        config = {"configurable": {"thread_id": thread_id}}
        
        # Fetch current state snapshot from the shared database
        snapshot = app.get_state(config)
        
        if not snapshot.values:
            print(f"No order found for Thread ID: {thread_id}\n")
            continue

        order_data = snapshot.values
        short_id = order_data.get('order_id')

        print(f"\n--- Reviewing Order [{short_id}] ---")
        print(f"Item: {order_data.get('item')} | Quantity: {order_data.get('quantity')}")
        print(f"Current Status: {order_data.get('status')}")
        
        approval_input = input(f"Approve order {short_id}? (y/n): ").strip().lower()

        if approval_input == 'y':
            app.update_state(config, {"status": "Approved"})
            print(f"[{short_id}] Status updated to APPROVED.")
        else:
            app.update_state(config, {"status": "Rejected"})
            print(f"[{short_id}] Status updated to REJECTED.")

        print(f"Resuming workflow for {short_id} end-to-end...")
        
        # Resuming execution runs the remaining nodes ('fulfill') to END
        app.invoke(None, config=config)
        print("=" * 50 + "\n")