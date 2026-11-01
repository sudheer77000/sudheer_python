from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class subState(TypedDict, total=False):
    text: str
    result: str
    count: int


class parentState(TypedDict, total=False):
    text: str
    upperText: str
    wordCount: int
    characterCount: int

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

def executeUpper(state: parentState):

    result = upperGraph.invoke({
        "text": state["text"]
    })

    return {
        "upperText": result["result"]
    }


def executeWordCount(state: parentState):

    result = wordGraph.invoke({
        "text": state["text"]
    })

    return {
        "wordCount": result["count"]
    }


def executeCharacterCount(state: parentState):

    result = charGraph.invoke({
        "text": state["text"]
    })

    return {
        "characterCount": result["count"]
    }


parentBuilder = StateGraph(parentState)

parentBuilder.add_node("executeUpper", executeUpper)
parentBuilder.add_node("executeWordCount", executeWordCount)
parentBuilder.add_node("executeCharacterCount", executeCharacterCount)

parentBuilder.add_edge(START, "executeUpper")
parentBuilder.add_edge("executeUpper", "executeWordCount")
parentBuilder.add_edge("executeWordCount", "executeCharacterCount")
parentBuilder.add_edge("executeCharacterCount", END)

parentGraph = parentBuilder.compile()

result = parentGraph.invoke({
    "text": "Welcome to LangGraph. Learning Python is fun!"
})

print("Uppercase:", result["upperText"])
print("Word Count:", result["wordCount"])
print("Character Count:", result["characterCount"])