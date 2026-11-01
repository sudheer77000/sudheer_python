from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
import operator
from dotenv import load_dotenv
import os
from openai import OpenAI
load_dotenv()

# Child Graph

# Initialize OpenAI client once
client = OpenAI()


# State definition
class childState(TypedDict, total=False):
    question: str
    answer: str


# OpenAI Web Search
def gptInvoke(state: childState):
    print("=================> Invoking GPT")
    response = client.responses.create(
        model="gpt-5-nano",
        tools=[
            {"type": "web_search"}
        ],
        input=state["question"]
    )

    return {
        "answer": response.output_text
    }


# Build LangGraph
childBuilder = StateGraph(childState)
childBuilder.add_node("gptInvoke", gptInvoke)
childBuilder.add_edge(START, "gptInvoke")
childBuilder.add_edge("gptInvoke", END)
childGraph = childBuilder.compile()


#result = childGraph.invoke({"question": "AED to INR price today"})
#print("\nQuestion:", result["question"])
#print("\nAnswer:", result["answer"])


# Child Graph End

class parentState(TypedDict, total=False):
    questionList: list[str]
    answerList: Annotated[list[dict], operator.add]

# Execute child graph for each question
def runChild(state: childState):
    result = childGraph.invoke({"question": state["question"]})
    return {"answerList": [{"question": state["question"],"answer": result["answer"]}]}


# Fan-out: send all questions to runChild
def parallelResearch(state: parentState):
    return [Send("runChild",{"question": question}) for question in state["questionList"]]


parentBuilder = StateGraph(parentState)

parentBuilder.add_node("runChild", runChild)
parentBuilder.add_conditional_edges( START,parallelResearch)
parentBuilder.add_edge("runChild", END)
parentGraph = parentBuilder.compile()


result = parentGraph.invoke({
    "questionList": [
        "What is capital of India?",
        "What is capital of China?",
        "What is capital of USA?",
        "What is capital of UAE?",
        "What is capital of Oman?",
    ],
    "answerList": []
})

for item in result["answerList"]:
    print("\nQuestion:", item["question"])
    print("Answer:", item["answer"])