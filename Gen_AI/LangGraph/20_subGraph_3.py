from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
import operator
from langgraph.types import Send

class BranchInput(TypedDict):
    text: str


class BranchOutput(TypedDict):
    results: list[str]


class BranchState(TypedDict):
    text: str
    results: list[str]


class MultiGraphState(TypedDict):
    text: str
    results: Annotated[list[str], operator.add]
    final_answer: str

def make_uppercase(state: BranchState):
    return {
        "results": [f"Uppercase: {state['text'].upper()}"]
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

def send_to_different_subgraphs(state: MultiGraphState):
    return [
        Send(
            "uppercase_graph",
            {"text": state["text"]},
        ),
        Send(
            "word_count_graph",
            {"text": state["text"]},
        ),
    ]

def combine_branch_results(state: MultiGraphState):
    return {
        "final_answer": " | ".join(state["results"])
    }

multi_graph_builder = StateGraph(MultiGraphState)

multi_graph_builder.add_node(
    "uppercase_graph",
    uppercase_graph,
)

multi_graph_builder.add_node(
    "word_count_graph",
    word_count_graph,
)

multi_graph_builder.add_node(
    "combine",
    combine_branch_results,
)

multi_graph_builder.add_conditional_edges(
    START,
    send_to_different_subgraphs,
    ["uppercase_graph", "word_count_graph"],
)

multi_graph_builder.add_edge("uppercase_graph", "combine")
multi_graph_builder.add_edge("word_count_graph", "combine")
multi_graph_builder.add_edge("combine", END)
multi_subgraph_parent = multi_graph_builder.compile()

multi_subgraph_result = multi_subgraph_parent.invoke(
    {
        "text": "Navya Sudheer Ishitha",
        "results": [],
        "final_answer": "",
    }
)

print(multi_subgraph_result["final_answer"])