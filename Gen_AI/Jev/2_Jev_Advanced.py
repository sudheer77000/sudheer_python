import os
from typing import TypedDict

from typesafe_sdk import TypeSafeClient, Choice, Score, Noul
from langgraph.graph import StateGraph, START, END
import os
from dotenv import load_dotenv
load_dotenv()


# ============================================================
# 1. State
# ============================================================

class State(TypedDict):
    message: str
    department: str
    urgency: float
    severity: float
    response: str


# ============================================================
# 2. Jev Decision Node
# ============================================================

def jev_decision(state: State):

    with TypeSafeClient() as client:

        result = client.system_one(
            state=state["message"],

            questions={

                # -------- Choice --------
                "department": Choice(
                    instructions="Which department should handle this request?",
                    criteria={
                        "billing": "Payment, invoice, refund or charging issue",
                        "technical": "Technical problem, error or system issue",
                        "general": "General question or request",
                    },
                ),

                # -------- Score --------
                "severity": Score(
                    instructions="How severe is the customer's problem?",
                    criteria=[
                        "Minor issue",
                        "Moderate issue",
                        "Serious issue",
                        "Critical issue",
                    ],
                ),

                # -------- Noul --------
                "urgent": Noul(
                    instructions="Does this customer request require immediate attention?"
                ),
            },
        )

    # Read Jev results
    department = result.answers["department"].choice
    severity = result.answers["severity"].score
    urgent = result.answers["urgent"].noul

    print("Department :", department)
    print("Severity   :", severity)
    print("Urgent     :", urgent)

    return {
        "department": department,
        "severity": severity,
        "urgency": urgent,
    }


# ============================================================
# 3. Billing Node
# ============================================================

def billing_node(state: State):

    return {
        "response": (
            "Your request has been routed to the Billing team."
        )
    }


# ============================================================
# 4. Technical Node
# ============================================================

def technical_node(state: State):

    return {
        "response": (
            "Your request has been routed to the Technical Support team."
        )
    }


# ============================================================
# 5. General Node
# ============================================================

def general_node(state: State):

    return {
        "response": (
            "Your request has been routed to General Support."
        )
    }


# ============================================================
# 6. Human Escalation Node
# ============================================================

def human_node(state: State):

    return {
        "response": (
            "This request requires immediate human attention."
        )
    }


# ============================================================
# 7. LangGraph Routing Logic
# ============================================================

def route_request(state: State):

    # First priority: urgent request
    if state["urgency"] > 0.8:
        return "human"

    # Otherwise route based on department
    if state["department"] == "billing":
        return "billing"

    if state["department"] == "technical":
        return "technical"

    return "general"


# ============================================================
# 8. Build LangGraph
# ============================================================

graph = StateGraph(State)

graph.add_node("jev", jev_decision)
graph.add_node("billing", billing_node)
graph.add_node("technical", technical_node)
graph.add_node("general", general_node)
graph.add_node("human", human_node)

graph.add_edge(START, "jev")

graph.add_conditional_edges(
    "jev",
    route_request,
    {
        "billing": "billing",
        "technical": "technical",
        "general": "general",
        "human": "human",
    }
)

graph.add_edge("billing", END)
graph.add_edge("technical", END)
graph.add_edge("general", END)
graph.add_edge("human", END)

app = graph.compile()


# ============================================================
# 9. Run
# ============================================================

Question  = input("Problem Description : ")

result = app.invoke({
    "message": (Question
    ),
    "department": "",
    "urgency": 0.0,
    "severity": 0.0,
    "response": "",
})

print("\nFINAL RESPONSE:")
print(result["response"])