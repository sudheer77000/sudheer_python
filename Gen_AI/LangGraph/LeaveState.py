from typing import TypedDict
from langgraph.graph import StateGraph, END


# -------------------------
# State
# -------------------------
class LeaveState(TypedDict):
    employee_id: str
    leave_days: int
    employee_valid: bool
    available_leave: int
    decision: str


# -------------------------
# Agent 1
# -------------------------
def employee_validation_agent(state: LeaveState):

    print("\nAgent 1: Employee Validation")

    valid_employees = ["E100", "E200", "E300"]

    return {
        "employee_valid": state["employee_id"] in valid_employees
    }


# -------------------------
# Agent 2
# -------------------------
def leave_balance_agent(state: LeaveState):

    print("Agent 2: Leave Balance Check")

    leave_db = {
        "E100": 20,
        "E200": 5,
        "E300": 15
    }

    return {
        "available_leave": leave_db.get(state["employee_id"], 0)
    }


# -------------------------
# Agent 3
# -------------------------
def approval_agent(state: LeaveState):

    print("Agent 3: Approval Decision")

    if state["employee_valid"] and state["leave_days"] <= state["available_leave"]:
        decision = "APPROVED"
    else:
        decision = "REJECTED"

    return {
        "decision": decision
    }


# -------------------------
# Build Graph
# -------------------------
builder = StateGraph(LeaveState)

builder.add_node("employee_validation", employee_validation_agent)
builder.add_node("leave_balance", leave_balance_agent)
builder.add_node("approval", approval_agent)

builder.set_entry_point("employee_validation")

builder.add_edge("employee_validation", "leave_balance")
builder.add_edge("leave_balance", "approval")
builder.add_edge("approval", END)

graph = builder.compile()


# -------------------------
# User Input
# -------------------------
employee_id = input("Enter Employee ID : ")
leave_days = int(input("Enter Leave Days : "))


# -------------------------
# Execute Graph
# -------------------------
result = graph.invoke(
    {
        "employee_id": employee_id,
        "leave_days": leave_days
    }
)


# -------------------------
# Output
# -------------------------
print("\n========== Final Result ==========")
print(f"Employee ID     : {result['employee_id']}")
print(f"Leave Days      : {result['leave_days']}")
print(f"Employee Valid  : {result['employee_valid']}")
print(f"Available Leave : {result['available_leave']}")
print(f"Decision        : {result['decision']}")