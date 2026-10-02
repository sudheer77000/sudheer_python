from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
import operator
from langgraph.types import Send

class WrapperState(TypedDict):
    text: str
    results: list[str]

class BranchState(TypedDict):
    text: str
    results: list[str]

class BranchInput(TypedDict):
    text: str


class BranchOutput(TypedDict):
    results: list[str]


def make_uppercase(state: BranchState):
    return {
        "results": [f"Uppercase: {state['text'].upper()}"]
    }

def count_words(state: BranchState):
    word_count = len(state["text"].split())
    return {
        "results": [f"Word count: {word_count}"]
    }

uppercase_builder = StateGraph(BranchState,input_schema=BranchInput,output_schema=BranchOutput)
uppercase_builder.add_node("make_uppercase", make_uppercase)
uppercase_builder.add_edge(START, "make_uppercase")
uppercase_builder.add_edge("make_uppercase", END)
uppercase_graph = uppercase_builder.compile()

def count_words(state: BranchState):
    word_count = len(state["text"].split())
    return {
        "results": [f"Word count: {word_count}"]
    }

word_count_builder = StateGraph(
    BranchState,
    input_schema=BranchInput,
    output_schema=BranchOutput,
)
word_count_builder.add_node("count_words", count_words)
word_count_builder.add_edge(START, "count_words")
word_count_builder.add_edge("count_words", END)
word_count_graph = word_count_builder.compile()

def run_two_graphs_in_wrapper(state: WrapperState):
    uppercase_result = uppercase_graph.invoke(
        {"text": state["text"]}
    )
    count_result = word_count_graph.invoke(
        {"text": state["text"]}
    )

    return {
        "results": (
            uppercase_result["results"]
            + count_result["results"]
        )
    }

def send_to_wrapper(state: WrapperState):
    return Send(
        "two_graph_wrapper",
        {"text": state["text"]},
    )

wrapper_builder = StateGraph(WrapperState)

wrapper_builder.add_node(
    "two_graph_wrapper",
    run_two_graphs_in_wrapper,
)

wrapper_builder.add_conditional_edges(
    START,
    send_to_wrapper,
    ["two_graph_wrapper"],
)

wrapper_builder.add_edge("two_graph_wrapper", END)

wrapper_graph = wrapper_builder.compile()

wrapper_result = wrapper_graph.invoke(
    {"text": "One Send has one destination"}
)

print(wrapper_result["results"])