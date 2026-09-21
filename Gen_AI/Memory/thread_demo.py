"""
Tutorial 4: Thread ID Demo
Shows how different thread_ids create separate, independent conversations.
"""

#from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.memory import MemorySaver
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os
load_dotenv()

# Initialize an OpenAI model seamlessly
llm = init_chat_model("gpt-5-nano", model_provider="openai", temperature=0.7)


#llm = ChatAnthropic(model="claude-sonnet-4-20250514")
#llm = ChatAnthropic(model="claude-sonnet-4-20250514")


def agent(state: MessagesState) -> MessagesState:
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


graph = StateGraph(MessagesState)
graph.add_node("agent", agent)
graph.add_edge(START, "agent")
graph.add_edge("agent", END)

checkpointer = MemorySaver()
agent_app = graph.compile(checkpointer=checkpointer)


if __name__ == "__main__":
    print("=" * 60)
    print("  Thread ID Demo — separate conversations")
    print("=" * 60)

    # Thread 1: Talk about Python
    thread1 = {"configurable": {"thread_id": "Q1-Thread"}}
    print("\n--- Thread 1:  ---")
    Q1 = input("Thread 1 , Question 1 Please : ")
    print("You: "+Q1)
    result = agent_app.invoke(
        {"messages": [("human", Q1)]},
        config=thread1
    )
    print(f"Agent: {result['messages'][-1].content}")

    # Thread 2: Talk about cooking
    thread2 = {"configurable": {"thread_id": "Q2-Thread"}}
    print("\n--- Thread 2:  ---")
    Q2 = input("Thread 2 , Question 1 Please : ")
    print("You: "+Q2)
    result = agent_app.invoke(
        {"messages": [("human",Q2)]},
        config=thread2
    )
    print(f"Agent: {result['messages'][-1].content}")

    # Back to Thread 1: Ask a generic follow-up
    print("\n--- Thread 1 (continued):")
    Q3 = input("Thread 1 , Question 2 Please : ")
    print("You: "+Q3)
    result = agent_app.invoke(
        {"messages": [("human", Q3)]},
        config=thread1
    )
    print(f"Agent: {result['messages'][-1].content}")

    # Back to Thread 2: Same exact question — different context
    print("\n--- Thread 2 (continued):  ---")
    Q4 = input("Thread 2 , Question 2 Please : ")
    print("You: "+Q4)
    result = agent_app.invoke(
        {"messages": [("human", Q4)]},
        config=thread2
    )
    print(f"Agent: {result['messages'][-1].content}")

    print()
    print("Same question, different answers — each thread remembers its own context.")