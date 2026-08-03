from typing import TypedDict
from decimal import Decimal
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
    )

class RefundValidation(TypedDict):
    customerId : str
    orderId: str
    refundAmount: Decimal
    refundReason: str

    is_valid_customer: bool
    is_valid_order: bool
    is_refund_amount_valid: bool
    refund_reason_score: Decimal
    request_status: str



# Agent 1 -- Customer Validation
def customer_validation(state: RefundValidation):
    print("Agent 1 - Validating The Customer")
    valid_customers = ["C001","C002","C003","C004"]
    return {
        "is_valid_customer" : state["customerId"] in valid_customers
    }

# Agent 2 -- Customer Validation
def order_validation(state: RefundValidation):
    print("Agent 2 - Validating The Order")
    valid_orders = ["OA0012","OB0013","OB0014","OD0015"]
    return {
        "is_valid_order" : state["orderId"] in valid_orders
    }

# Agent 3 -- Refund Amount Validation
def refund_validation(state: RefundValidation):
    print("Agent 3 - Validating The Amount")
    order_amount = {
        "OA0012": Decimal(12699),
        "OB0013": Decimal(500),
        "OB0014": Decimal(46.98),
        "OD0015": Decimal(9698)
    }
    return {
        "is_refund_amount_valid" :  order_amount.get(state["orderId"]) == state["refundAmount"]
    }

# Agent 4 -- LLM Validation on Refund Reason
def refund_reason_validation(state: RefundValidation):

    print("Agent 4 - Refund Reason Validation")

    prompt = f"""

    You are a Refund Validation AI Agent.

    Your task is to analyze whether the customer's refund reason is genuine.

    Refund Reason:
    {state["refundReason"]}

    Evaluate:

    Return only the Score 1 to 100, don't provide any additional fields

    Example:

    90

    Now analyze the actual refund reason.

    """


    response = llm.invoke(prompt)


    return {
        "refund_reason_score": int(response.content)
    }


# Agent 5 -- Final Decision
def authorization_agent(state: RefundValidation):

    print("Agent 5 - Final Decision")

    if state["is_valid_customer"] and state["is_valid_order"] and state["is_refund_amount_valid"] and state["refund_reason_score"]  > 90:
        request_status = "APPROVED"
    else:
        request_status = "REJECTED"

    return {
        "request_status": request_status
    }



# Build Graph
builder = StateGraph(RefundValidation)

builder.add_node("Step-1", customer_validation)
builder.add_node("Step-2", order_validation)
builder.add_node("Step-3", refund_validation)
builder.add_node("Step-4", refund_reason_validation)
builder.add_node("Step-5", authorization_agent)

builder.set_entry_point("Step-1")
builder.add_edge("Step-1", "Step-2")
builder.add_edge("Step-2", "Step-3")
builder.add_edge("Step-3", "Step-4")
builder.add_edge("Step-4", "Step-5")
builder.add_edge("Step-5", END)

graph = builder.compile()

# -------------------------
# User Input
# -------------------------
customerId = input("Enter Customer Id : ")
orderId = input("Enter Order Id : ")
refundAmount = int(input("Enter Refund Amount : "))
refundReason = input("Enter Refund Reason : ")


# -------------------------
# Execute Graph
# -------------------------
result = graph.invoke(
    {
        "customerId": customerId,
        "orderId": orderId,
        "refundAmount": refundAmount,
        "refundReason": refundReason,
    }
)


# -------------------------
# Output
# -------------------------
print("\n========== Final Result ==========")
print(f"customerId     : {result['customerId']}")
print(f"orderId     : {result['orderId']}")
print(f"refundAmount  : {result['refundAmount']}")
print(f"refundReason : {result['refundReason']}")

print(f"is_valid_customer        : {result['is_valid_customer']}")
print(f"is_valid_order        : {result['is_valid_order']}")
print(f"is_refund_amount_valid        : {result['is_refund_amount_valid']}")
print(f"refund_reason_score        : {result['refund_reason_score']}")
print(f"request_status        : {result['request_status']}")



