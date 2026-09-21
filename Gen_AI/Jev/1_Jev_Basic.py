from typing import TypedDict, Literal

from langgraph.graph import StateGraph, START, END
from typesafe_sdk import Choice, TypeSafeClient
import os
from dotenv import load_dotenv
load_dotenv()


# -------------------------
# 1. LangGraph State
# -------------------------

class State(TypedDict):
    message: str
    route: str
    response: str


# -------------------------
# 2. Jev Router
# -------------------------

def jev_router(state: State):

    client = TypeSafeClient()

    result = client.system_one(
        state=state["message"],
        questions={
            "route": Choice(
                instructions="Which team should handle this request?",
                criteria={
                    "billing": None,
                    "technical": None,
                    "sales": None,
                },
            )
        },
    )

    route = result.choices["route"].choice

    print("Jev selected:", route)

    return {
        "route": route
    }


# -------------------------
# 3. Billing Node
# -------------------------

def billing(state: State):

    return {
        "response": "Billing team will handle your request."
    }


# -------------------------
# 4. Technical Node
# -------------------------

def technical(state: State):

    return {
        "response": "Technical team will investigate the issue."
    }


# -------------------------
# 5. Sales Node
# -------------------------

def sales(state: State):

    return {
        "response": "Sales team will contact you."
    }


# -------------------------
# 6. Router Function
# -------------------------

def route_decision(state: State):

    return state["route"]


# -------------------------
# 7. Build Graph
# -------------------------

graph = StateGraph(State)

graph.add_node("jev_router", jev_router)
graph.add_node("billing", billing)
graph.add_node("technical", technical)
graph.add_node("sales", sales)

graph.add_edge(START, "jev_router")

graph.add_conditional_edges(
    "jev_router",
    route_decision,
    {
        "billing": "billing",
        "technical": "technical",
        "sales": "sales",
    }
)

graph.add_edge("billing", END)
graph.add_edge("technical", END)
graph.add_edge("sales", END)

app = graph.compile()


# -------------------------
# 8. Run
# -------------------------

Question  = input("Problem Description : ")

result = app.invoke({
    "message": Question,
    "route": "",
    "response": "",
})

print(result["response"])