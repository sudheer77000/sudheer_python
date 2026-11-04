
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
import os
from openai import OpenAI
load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# -----------------------------------
# Simulated business database
# -----------------------------------

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


# -----------------------------------
# Shared communication state
# -----------------------------------

class State(TypedDict):
    order_id: str
    order_info: str
    delivery_info: str
    peer_message: str
    peer_reply: str
    support_info: str
    final_answer: str


# -----------------------------------
# 1. Coordinator
# -----------------------------------

def coordinator(state: State):

    print("\n[Coordinator] Assigning tasks to peers")

    return {}


# -----------------------------------
# 2. Order Agent
# -----------------------------------

def order_agent(state: State):

    print("\n[Order Agent] Checking order database")

    order = ORDERS.get(state["order_id"])

    if not order:
        return {"order_info": "Order not found"}

    print("[Order Agent] Order:", order)

    return {"order_info": str(order)}


# -----------------------------------
# 3. Delivery Agent
# -----------------------------------

def delivery_agent(state: State):

    print("\n[Delivery Agent] Checking tracking API")

    tracking = TRACKING.get(state["order_id"])

    if not tracking:
        return {"delivery_info": "Tracking not found"}

    print("[Delivery Agent] Tracking:", tracking)

    # Delivery agent needs order information
    print("\n[Delivery Agent] Sending message to Order Agent")

    return {
        "delivery_info": str(tracking),
        "peer_message": "Please confirm the order status and customer details."
    }


# -----------------------------------
# 4. Order Agent responds to peer
# -----------------------------------

def peer_response(state: State):

    print("\n[Order Agent] Received message from Delivery Agent")

    prompt = f"""
    You are the Order Agent.

    Your order information:
    {state['order_info']}

    Peer request:
    {state['peer_message']}

    Respond with the requested order details.
    """

    response = llm.invoke(prompt)

    print("[Order Agent] Sending response to Delivery Agent")

    return {"peer_reply": response.content}


# -----------------------------------
# 5. Delivery Agent uses peer response
# -----------------------------------

def delivery_update(state: State):

    print("\n[Delivery Agent] Received peer response")

    prompt = f"""
    You are the Delivery Agent.

    Tracking information:
    {state['delivery_info']}

    Order Agent response:
    {state['peer_reply']}

    Combine the information and report delivery status.
    """

    response = llm.invoke(prompt)

    return {"delivery_info": response.content}


# -----------------------------------
# 6. Support Agent
# -----------------------------------

def support_agent(state: State):

    print("\n[Support Agent] Reviewing peer findings")

    prompt = f"""
    You are the Support Agent.

    Order details:
    {state['order_info']}

    Delivery details:
    {state['delivery_info']}

    Recommend an appropriate customer support action.
    """

    response = llm.invoke(prompt)

    return {"support_info": response.content}


# -----------------------------------
# 7. Final Coordinator
# -----------------------------------

def final_coordinator(state: State):

    print("\n[Coordinator] Collecting all agent messages")

    prompt = f"""
    You are the final Coordinator.

    Order information:
    {state['order_info']}

    Delivery information:
    {state['delivery_info']}

    Peer communication:
    {state['peer_reply']}

    Support recommendation:
    {state['support_info']}

    Provide a clear final response to the customer.
    """

    response = llm.invoke(prompt)

    return {"final_answer": response.content}


# -----------------------------------
# 8. Build LangGraph
# -----------------------------------

graph = StateGraph(State)

graph.add_node("coordinator", coordinator)
graph.add_node("order", order_agent)
graph.add_node("delivery", delivery_agent)
graph.add_node("peer_response", peer_response)
graph.add_node("delivery_update", delivery_update)
graph.add_node("support", support_agent)
graph.add_node("final", final_coordinator)

# Start with coordinator
graph.add_edge(START, "coordinator")

# Coordinator delegates to peers in parallel
graph.add_edge("coordinator", "order")
graph.add_edge("coordinator", "delivery")

# Delivery agent requests information from Order Agent
graph.add_edge("delivery", "peer_response")

# Order Agent responds; Delivery Agent uses response
graph.add_edge("peer_response", "delivery_update")

# Wait for order and updated delivery findings
graph.add_edge(["order", "delivery_update"], "support")

# Support reports to coordinator
graph.add_edge("support", "final")

graph.add_edge("final", END)

app = graph.compile()


# -----------------------------------
# 9. Execute
# -----------------------------------

if __name__ == "__main__":

    order_id = input("Enter Order ID: ")

    result = app.invoke({
        "order_id": order_id,
        "order_info": "",
        "delivery_info": "",
        "peer_message": "",
        "peer_reply": "",
        "support_info": "",
        "final_answer": ""
    })

    print("\n========== FINAL CUSTOMER RESPONSE ==========")
    print(result["final_answer"])
