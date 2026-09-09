import sqlite3

from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.checkpoint.sqlite import SqliteSaver


def chatbot(state: MessagesState):

    print("\nMessages available in Program 1:")

    for message in state["messages"]:
        print(type(message).__name__, ":", message.content)

    return {
        "messages": [
            ("assistant", "Program 1 received your message.")
        ]
    }


# Create graph
builder = StateGraph(MessagesState)

builder.add_node("chatbot", chatbot)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)


# SQLite database
conn = sqlite3.connect(
    "chat_memory.db",
    check_same_thread=False
)

checkpointer = SqliteSaver(conn)

graph = builder.compile(checkpointer=checkpointer)


# Same thread ID
config = {
    "configurable": {
        "thread_id": "test-user-1"
    }
}


# Take input from user
user_input = input("Program 1 - Enter your message: ")


result = graph.invoke(
    {
        "messages": [
            ("user", user_input)
        ]
    },
    config
)


print("\nProgram 1 result:")

for message in result["messages"]:
    print(type(message).__name__, ":", message.content)