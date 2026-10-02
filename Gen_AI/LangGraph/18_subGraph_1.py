from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END

PRODUCT_CATALOG = {
    "Keyboard": {"stock": 5, "unit_price": 500.0},
    "Mouse": {"stock": 10, "unit_price": 250.0},
}

class OrderState(TypedDict):
    product: str
    quantity: int
    inventory_status: str
    total_price: float
    final_response: str

def check_inventory(state: OrderState):
    print("Checking inventory...")

    product = PRODUCT_CATALOG[state["product"]]
    is_available = product["stock"] >= state["quantity"]

    return {
        "inventory_status": (
            "Available" if is_available else "Unavailable"
        )
    }

def calculate_price(state: OrderState):
    print("Calculating price...")

    if state["inventory_status"] != "Available":
        return {"total_price": 0.0}

    unit_price = PRODUCT_CATALOG[state["product"]]["unit_price"]

    return {
        "total_price": state["quantity"] * unit_price
    }

order_subgraph_builder = StateGraph(OrderState)

order_subgraph_builder.add_node("check_inventory",check_inventory)
order_subgraph_builder.add_node("calculate_price",calculate_price)

order_subgraph_builder.add_edge(START,"check_inventory")
order_subgraph_builder.add_edge( "check_inventory","calculate_price")
order_subgraph_builder.add_edge( "calculate_price",END)

order_subgraph = order_subgraph_builder.compile()

#result = order_subgraph.invoke({"product": "Keyboard","quantity": 5 })
#print(result)

def validate_request(state: OrderState):
    print("Validating request...")

    if state["product"] not in PRODUCT_CATALOG:
        raise ValueError(f"Unknown product: {state['product']}")

    if state["quantity"] <= 0:
        raise ValueError("Quantity must be greater than zero.")

    return {}

def create_final_response(state: OrderState):
    if state["inventory_status"] == "Available":
        response = (
            f"{state['quantity']} {state['product']} ordered. "
            f"Total Price: ₹{state['total_price']:,.2f}"
        )
    else:
        response = (
            f"Order not placed. {state['quantity']} "
            f"{state['product']} are not available."
        )

    return {
        "final_response": response
    }

order_builder = StateGraph(OrderState)

order_builder.add_node("validate_request",validate_request)
order_builder.add_node("order_processing",order_subgraph)
order_builder.add_node("final_response",create_final_response)

order_builder.add_edge(START,"validate_request")
order_builder.add_edge("validate_request","order_processing")
order_builder.add_edge("order_processing","final_response")
order_builder.add_edge("final_response",END )

order_graph = order_builder.compile()

product = input("Enter The Product Name : ")
quantity = int(input("Enter total quantity : "))

def run_order_workflow():
    result = order_graph.invoke(
        {
            "product": product,
            "quantity": quantity,
        }
    )

    print(result["final_response"])

    return result

order_result = run_order_workflow()