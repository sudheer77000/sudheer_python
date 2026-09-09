from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.checkpoint.memory import MemorySaver


llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)


def chatbot(state: MessagesState):

    response = llm.invoke(state["messages"])

    return {
        "messages": [response]
    }


builder = StateGraph(MessagesState)

builder.add_node("chatbot", chatbot)

builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)


# Checkpointer
memory = MemorySaver()

graph = builder.compile(
    checkpointer=memory
)


# --------------------------------
# Conversation 1
# --------------------------------

result = graph.invoke(
    {
        "messages": [
            HumanMessage(content="My name is Sudheer")
        ]
    },
    config={
        "configurable": {
            "thread_id": "user-1"
        }
    }
)

print("AI:", result["messages"][-1].content)


# --------------------------------
# Conversation 2
# --------------------------------

result = graph.invoke(
    {
        "messages": [
            HumanMessage(content="What is my name?")
        ]
    },
    config={
        "configurable": {
            "thread_id": "user-1"
        }
    }
)

print("AI:", result["messages"][-1].content)