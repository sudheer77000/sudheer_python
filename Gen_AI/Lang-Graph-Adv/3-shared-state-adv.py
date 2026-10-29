from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# Shared state for parent and subgraph
class BankingState(TypedDict):
    customer_id: str
    account_status: str
    amount: float
    registered_location: str
    transaction_location: str
    fraud_decision: str
    transfer_status: str
    message: str

# ---------- SUBGRAPH: Step 1 ----------
def check_amount(state: BankingState):
    print("3. Checking transaction amount")

    if state["amount"] > 1000:
        return {"fraud_decision": "REVIEW"}

    return {"fraud_decision": "PENDING"}


# ---------- SUBGRAPH: Step 2 ----------
def check_location(state: BankingState):
    print("4. Checking transaction location")

    if (
        state["registered_location"].lower()
        != state["transaction_location"].lower()
    ):
        return {"fraud_decision": "REVIEW"}

    if state["fraud_decision"] == "PENDING":
        return {"fraud_decision": "APPROVED"}

    return {}


# Build fraud subgraph
fraud_builder = StateGraph(BankingState)

fraud_builder.add_node("amount_check", check_amount)
fraud_builder.add_node("location_check", check_location)

fraud_builder.add_edge(START, "amount_check")
fraud_builder.add_edge("amount_check", "location_check")
fraud_builder.add_edge("location_check", END)

fraud_subgraph = fraud_builder.compile()


# ---------- PARENT GRAPH: Step 1 ----------
def validate_customer(state: BankingState):
    print("1. Validating customer")

    if not state["customer_id"]:
        return {
            "fraud_decision": "BLOCK",
            "message": "Invalid customer"
        }

    return {"message": "Customer validated"}


# ---------- PARENT GRAPH: Step 2 ----------
def validate_account(state: BankingState):
    print("2. Validating account")

    if state["account_status"] != "ACTIVE":
        return {
            "fraud_decision": "BLOCK",
            "message": "Account is not active"
        }

    return {"message": "Account validated"}




# ---------- PARENT GRAPH: Invoke subgraph ----------
def run_fraud_check(state: BankingState):
    print("Invoking fraud subgraph")

    result = fraud_subgraph.invoke(state)

    # Return updated fields to parent state
    return {
        "fraud_decision": result["fraud_decision"]
    }


# ---------- PARENT GRAPH: Step 5 ----------
def process_transfer(state: BankingState):
    print("5. Processing transfer")

    if state["fraud_decision"] == "APPROVED":
        return {"transfer_status": "SUCCESS"}

    return {"transfer_status": "ON_HOLD"}


# ---------- PARENT GRAPH: Step 6 ----------
def send_confirmation(state: BankingState):
    print("6. Sending confirmation")

    if state["transfer_status"] == "SUCCESS":
        message = "Transfer completed"
    else:
        message = "Transfer on hold for review"

    return {"message": message}


# Build parent graph
parent_builder = StateGraph(BankingState)

parent_builder.add_node("customer_validation", validate_customer)
parent_builder.add_node("account_validation", validate_account)
parent_builder.add_node("fraud", run_fraud_check)
parent_builder.add_node("transfer", process_transfer)
parent_builder.add_node("confirmation", send_confirmation)

parent_builder.add_edge(START, "customer_validation")
parent_builder.add_edge("customer_validation", "account_validation")
parent_builder.add_edge("account_validation", "fraud")
parent_builder.add_edge("fraud", "transfer")
parent_builder.add_edge("transfer", "confirmation")
parent_builder.add_edge("confirmation", END)

banking_graph = parent_builder.compile()


# Invoke parent graph
result = banking_graph.invoke({
    "customer_id": "C101",
    "account_status": "ACTIVE",
    "amount": 500.0,
    "registered_location": "Dubai",
    "transaction_location": "Dubai",
    "fraud_decision": "PENDING",
    "transfer_status": "PENDING",
    "message": "",
})

print("\nFinal result:", result)