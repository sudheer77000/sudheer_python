from typing import TypedDict
from decimal import Decimal
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
from langchain_groq import ChatGroq
load_dotenv()

llm = ChatOllama(model="qwen2.5:3b",temperature=0)
#llm = ChatGroq(model="llama-3.1-8b-instant",temperature= 0,max_tokens=1000)

class RefundValidation(TypedDict):
    customerId : str
    orderId: str
    refundAmount: Decimal
    refundReason: str

    is_valid_customer: bool
    is_valid_order: bool
    is_refund_amount_valid: bool
    refund_reason_score: Decimal
    human_decision: str
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

    If refund description is irrelavent to the product, provide score as 0

    """


    response = llm.invoke(prompt)


    return {
        "refund_reason_score": int(response.content)
    }

# Agent 5 -- Human Review
def human_review_agent(state: RefundValidation):

    print("\n========================================")
    print(" HUMAN REVIEW REQUIRED")
    print("========================================")

    print(f"Customer ID        : {state['customerId']}")
    print(f"Order ID           : {state['orderId']}")
    print(f"Refund Amount      : {state['refundAmount']}")
    print(f"Refund Reason      : {state['refundReason']}")
    print(f"LLM Score          : {state['refund_reason_score']}")

    decision = input(
        "\nApprove Refund? (YES/NO): "
    ).strip().upper()

    return {
        "human_decision": decision
    }

def route_after_llm(state: RefundValidation):

    score = state["refund_reason_score"]

    if score >= 75:
        return "approve"

    elif score >= 40:
        return "human_review"

    else:
        return "reject"

# Agent 6 -- Final Decision
# Agent 6 -- Final Decision
def authorization_agent(state: RefundValidation):

    print("Agent 6 - Final Decision")

    if not (
        state["is_valid_customer"]
        and state["is_valid_order"]
        and state["is_refund_amount_valid"]
    ):
        return {
            "request_status": "REJECTED"
        }

    if state["refund_reason_score"] >= 75:

        return {
            "request_status": "APPROVED"
        }

    if state.get("human_decision") == "YES":

        return {
            "request_status": "APPROVED"
        }

    return {
        "request_status": "REJECTED"
    }



# Build Graph
builder = StateGraph(RefundValidation)

builder.add_node("Step-1", customer_validation)
builder.add_node("Step-2", order_validation)
builder.add_node("Step-3", refund_validation)
builder.add_node("Step-4", refund_reason_validation)
builder.add_node("Step-5", human_review_agent)
builder.add_node("Step-6", authorization_agent)

builder.set_entry_point("Step-1")

builder.add_edge("Step-1", "Step-2")
builder.add_edge("Step-2", "Step-3")
builder.add_edge("Step-3", "Step-4")

builder.add_conditional_edges(
    "Step-4",
    route_after_llm,
    {
        "approve": "Step-6",
        "human_review": "Step-5",
        "reject": "Step-6"
    }
)

builder.add_edge("Step-5", "Step-6")
builder.add_edge("Step-6", END)

graph = builder.compile()

# -------------------------
# User Input
# -------------------------
customerId = input("Enter Customer Id : ")
orderId = input("Enter Order Id : ")
refundAmount = Decimal(input("Enter Refund Amount : "))
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



