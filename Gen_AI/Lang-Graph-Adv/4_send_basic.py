from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send


class BankingState(TypedDict, total=False):
    customer_id: str
    amount: float
    decision: str


# Subgraph node
def check_fraud(state: BankingState):
    print("Checking fraud for:", state["customer_id"])

    if state["amount"] > 1000:
        return {"decision": "REVIEW"}

    return {"decision": "APPROVED"}


# Build subgraph
sub_builder = StateGraph(BankingState)
sub_builder.add_node("check_fraud", check_fraud)
sub_builder.add_edge(START, "check_fraud")
sub_builder.add_edge("check_fraud", END)

fraud_subgraph = sub_builder.compile()


# Parent graph node
def validate_customer(state: BankingState):
    print("Validating customer:", state["customer_id"])
    return {}


# Route using Send
def send_to_fraud(state: BankingState):
    return Send("fraud", state)


# Parent node invokes the compiled subgraph
parent_builder = StateGraph(BankingState)
parent_builder.add_node("validate", validate_customer)
parent_builder.add_node("fraud", fraud_subgraph)

parent_builder.add_edge(START, "validate")
parent_builder.add_conditional_edges(
    "validate",
    send_to_fraud,
)
parent_builder.add_edge("fraud", END)

banking_graph = parent_builder.compile()


result = banking_graph.invoke({
    "customer_id": "C101",
    "amount": 500,
})

print(result)