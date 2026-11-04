
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
import os
from openai import OpenAI
load_dotenv()

# --------------------------------
# 1. LLM
# --------------------------------
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# --------------------------------
# 2. Simulated business data
# --------------------------------
ORDERS = {
    "1001": {
        "customer": "John",
        "status": "Shipped",
        "amount": 250
    }
}

TRACKING = {
    "1001": {
        "status": "Delayed",
        "location": "Dubai Hub",
        "expected": "Tomorrow"
    }
}

# --------------------------------
# 3. Shared State
# --------------------------------
class State(TypedDict):
    order_id: str
    order_info: str
    delivery_info: str
    support_info: str
    final_answer: str

# --------------------------------
# 4. Peer Agent 1 - Order
# --------------------------------
def order_agent(state: State):
    print("\n[Order Agent] Checking order...")

    order = ORDERS.get(state["order_id"], "Order not found")

    print("[Order Agent] Result:", order)

    return {"order_info": str(order)}

# --------------------------------
# 5. Peer Agent 2 - Delivery
# --------------------------------
def delivery_agent(state: State):
    print("\n[Delivery Agent] Checking tracking...")

    tracking = TRACKING.get(
        state["order_id"], "Tracking not found"
    )

    print("[Delivery Agent] Result:", tracking)

    return {"delivery_info": str(tracking)}

# --------------------------------
# 6. Peer Agent 3 - Support
# --------------------------------
def support_agent(state: State):
    print("\n[Support Agent] Preparing recommendation...")

    prompt = f"""
    Suggest a customer support action.

    Order: {state['order_info']}
    Delivery: {state['delivery_info']}
    """

    response = llm.invoke(prompt)

    print("[Support Agent] Recommendation generated")

    return {"support_info": response.content}

# --------------------------------
# 7. Coordinator Agent
# --------------------------------
def coordinator(state: State):
    print("\n[Coordinator] Collecting peer results...")

    prompt = f"""
    You are an e-commerce coordinator.

    Order ID: {state['order_id']}
    Order details: {state['order_info']}
    Delivery details: {state['delivery_info']}
    Support recommendation: {state['support_info']}

    Generate a clear response for the customer.
    """

    response = llm.invoke(prompt)

    print("[Coordinator] Final response generated")

    return {"final_answer": response.content}

# --------------------------------
# 8. Build LangGraph Workflow
# --------------------------------
graph = StateGraph(State)

graph.add_node("order", order_agent)
graph.add_node("delivery", delivery_agent)
graph.add_node("support", support_agent)
graph.add_node("coordinator", coordinator)

# Start parallel peer agents
graph.add_edge(START, "order")
graph.add_edge(START, "delivery")

# Wait for both peers
graph.add_edge(["order", "delivery"], "support")

# Coordinator gets combined results
graph.add_edge("support", "coordinator")
graph.add_edge("coordinator", END)

app = graph.compile()

# --------------------------------
# 9. Execute Program
# --------------------------------
if __name__ == "__main__":

    order_id = input("Enter Order ID: ")

    result = app.invoke({
        "order_id": order_id,
        "order_info": "",
        "delivery_info": "",
        "support_info": "",
        "final_answer": ""
    })

    print("\n================================")
    print("       CUSTOMER RESPONSE")
    print("================================")
    print(result["final_answer"])
