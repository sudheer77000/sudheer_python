from typing import TypedDict
from langgraph.graph import StateGraph, END


# -------------------------
# Memory / State
# -------------------------

class LoginState(TypedDict):

    username: str
    password: str

    attempt: int
    login_status: str



# -------------------------
# Agent 1 - Validate Login
# -------------------------

def login_validation(state: LoginState):

    print("\nChecking Login")

    correct_password = "admin123"

    if state["password"] == correct_password:

        return {
            "login_status": "SUCCESS"
        }

    else:

        return {
            "login_status": "FAILED",
            "attempt": state["attempt"] + 1
        }



# -------------------------
# Agent 2 - Ask Retry
# -------------------------

def retry_login(state: LoginState):

    print("\nRetry Login")

    password = input(
        "Enter Password Again for User Id Sudheer : "
    )

    return {
        "password": password
    }



# -------------------------
# Routing Logic
# -------------------------

def check_login(state: LoginState):

    if state["login_status"] == "SUCCESS":

        return "success"


    elif state["attempt"] < 3:

        return "retry"


    else:

        return "failed"



# -------------------------
# Build Graph
# -------------------------

builder = StateGraph(LoginState)


builder.add_node(
    "Login",
    login_validation
)


builder.add_node(
    "Retry",
    retry_login
)


builder.set_entry_point(
    "Login"
)


builder.add_conditional_edges(
    "Login",
    check_login,
    {
        "success": END,
        "retry": "Retry",
        "failed": END
    }
)


# LOOP
builder.add_edge(
    "Retry",
    "Login"
)


graph = builder.compile()



# -------------------------
# Execute
# -------------------------

password = input("Please Enter Password for User Id Sudheer : ")

result = graph.invoke(
    {
        "username": "Sudheer",
        "password": password,
        "attempt": 0,
        "login_status": ""
    }
)


print("\n========== RESULT ==========")

print(result)