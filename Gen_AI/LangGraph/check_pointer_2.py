import sqlite3

from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.checkpoint.sqlite import SqliteSaver


def chatbot(state: MessagesState):

    print("\nMessages available in Program 2:")

    for message in state["messages"]:
        print(type(message).__name__, ":", message.content)

    return {
        "messages": [
            ("assistant", "Program 2 received your message.")
        ]
    }


# Create graph
builder = StateGraph(MessagesState)

builder.add_node("chatbot", chatbot)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)


# SAME SQLite database
conn = sqlite3.connect(
    "chat_memory.db",
    check_same_thread=False
)

checkpointer = SqliteSaver(conn)

graph = builder.compile(checkpointer=checkpointer)


# SAME thread ID
config = {
    "configurable": {
        "thread_id": "test-user-1"
    }
}


# Take input from user
user_input = input("Program 2 - Enter your message: ")


result = graph.invoke(
    {
        "messages": [
            ("user", user_input)
        ]
    },
    config
)


print("\nProgram 2 result:")

for message in result["messages"]:
    print(type(message).__name__, ":", message.content)