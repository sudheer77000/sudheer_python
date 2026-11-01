from typing import TypedDict, Annotated
import operator

from langgraph.graph import StateGraph, START, END
from langgraph.types import Send


class subState(TypedDict, total=False):
    text: str
    result: str
    count: int


class parentState(TypedDict, total=False):
    text: str
    results: Annotated[list[dict], operator.add]

def convertUpper(state: subState):
    return {
        "result": state["text"].upper()
    }


upperBuilder = StateGraph(subState)
upperBuilder.add_node("convertUpper", convertUpper)
upperBuilder.add_edge(START, "convertUpper")
upperBuilder.add_edge("convertUpper", END)

upperGraph = upperBuilder.compile()

def countWords(state: subState):
    return {
        "count": len(state["text"].split())
    }


wordBuilder = StateGraph(subState)
wordBuilder.add_node("countWords", countWords)
wordBuilder.add_edge(START, "countWords")
wordBuilder.add_edge("countWords", END)

wordGraph = wordBuilder.compile()

def countCharacters(state: subState):
    return {
        "count": len(state["text"])
    }


charBuilder = StateGraph(subState)
charBuilder.add_node("countCharacters", countCharacters)
charBuilder.add_edge(START, "countCharacters")
charBuilder.add_edge("countCharacters", END)

charGraph = charBuilder.compile()

def runUpper(state: subState):

    result = upperGraph.invoke({
        "text": state["text"]
    })

    return {
        "results": [{
            "task": "Uppercase",
            "output": result["result"]
        }]
    }


def runWordCount(state: subState):

    result = wordGraph.invoke({
        "text": state["text"]
    })

    return {
        "results": [{
            "task": "Word Count",
            "output": result["count"]
        }]
    }


def runCharacterCount(state: subState):

    result = charGraph.invoke({
        "text": state["text"]
    })

    return {
        "results": [{
            "task": "Character Count",
            "output": result["count"]
        }]
    }

def parallelProcess(state: parentState):

    return [
        Send("runUpper", {
            "text": state["text"]
        }),

        Send("runWordCount", {
            "text": state["text"]
        }),

        Send("runCharacterCount", {
            "text": state["text"]
        })
    ]

parentBuilder = StateGraph(parentState)

parentBuilder.add_node("runUpper", runUpper)
parentBuilder.add_node("runWordCount", runWordCount)
parentBuilder.add_node("runCharacterCount", runCharacterCount)

parentBuilder.add_conditional_edges(
    START,
    parallelProcess
)

parentBuilder.add_edge("runUpper", END)
parentBuilder.add_edge("runWordCount", END)
parentBuilder.add_edge("runCharacterCount", END)

parentGraph = parentBuilder.compile()

result = parentGraph.invoke({
    "text": "Welcome to LangGraph. Learning Python is fun!",
    "results": []
})

for item in result["results"]:
    print(item["task"], ":", item["output"])