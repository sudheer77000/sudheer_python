from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
import operator
from langgraph.types import Send

load_dotenv()

model = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0,
)

class ParentState(TypedDict):
    topics: list[str]
    research_results: Annotated[
        list[str],
        operator.add,
    ]
    final_answer: str

class ResearchWorkerInput(TypedDict):
    topic: str

class ResearchState(TypedDict):
    topic: str
    research: str
    summary: str

def research_topic(state: ResearchState):
    topic = state["topic"]
    print(f"[SUBGRAPH] Researching: {topic}")

    response = model.invoke(
        f"""
Explain this Generative AI topic: {topic}

Include:
1. A definition
2. Important concepts
3. One practical use case

Keep the explanation concise.
"""
    )

    return {
        "research": response.content
    }


def summarize_topic(state: ResearchState):
    print(f"[SUBGRAPH] Summarizing: {state['topic']}")

    response = model.invoke(
        f"""
Create a concise summary of this research.

Topic: {state['topic']}

Research:
{state['research']}
"""
    )

    return {
        "summary": response.content
    }

research_builder = StateGraph(ResearchState)

research_builder.add_node("research_topic",research_topic) 
research_builder.add_node("summarize_topic",summarize_topic)  

research_builder.add_edge(START,"research_topic")  
research_builder.add_edge("research_topic","summarize_topic")
research_builder.add_edge("summarize_topic",END)

research_subgraph = research_builder.compile()

#result = research_subgraph.invoke({"topic":"Doller to India Rupee" })
#print(result)

def prepare_topics(state: ParentState):
    print("Topics received:")

    for topic in state["topics"]:
        print(f"- {topic}")

    return {}

def research_worker(state: ResearchWorkerInput):
    topic = state["topic"]
    print(f"[WORKER] Starting: {topic}")

    subgraph_result = research_subgraph.invoke(
        {
            "topic": topic,
            "research": "",
            "summary": "",
        }
    )

    return {
        "research_results": [
            f"## {topic}\n\n{subgraph_result['summary']}"
        ]
    }

def distribute_topics(state: ParentState):
    return [
        Send("research_worker", {"topic": topic})
        for topic in state["topics"]
    ]

def combine_results(state: ParentState):
    combined_research = "\n\n".join(
        state["research_results"]
    )

    response = model.invoke(
        f"""
Combine these research summaries into one clear explanation.
Keep each topic under its own heading.

{combined_research}
"""
    )

    return {
        "final_answer": response.content
    }

research_parent_builder = StateGraph(ParentState)

research_parent_builder.add_node(
    "prepare_topics",
    prepare_topics,
)

research_parent_builder.add_node(
    "research_worker",
    research_worker,
)

research_parent_builder.add_node(
    "combine_results",
    combine_results,
)

research_parent_builder.add_edge(
    START,
    "prepare_topics",
)

research_parent_builder.add_conditional_edges(
    source="prepare_topics",
    path=distribute_topics,
    path_map=["research_worker"],
)

research_parent_builder.add_edge(
    "research_worker",
    "combine_results",
)

research_parent_builder.add_edge(
    "combine_results",
    END,
)

research_graph = research_parent_builder.compile()

# def run_parallel_research_workflow():
#     result = research_graph.invoke(
#         {
#             "topics": [
#                 "Retrieval-Augmented Generation",
#                 "AI Agents",
#                 "Memory Management",
#             ],
#             "research_results": [],
#         }
#     )

#     print("\nFINAL ANSWER\n")
#     print(result["final_answer"])

#     return result

# research_result = run_parallel_research_workflow()
# print(research_result)

def run_parallel_research_workflow():
    result = research_graph.invoke(
        {
            "topics": [
                "american dollar",
                "Indian Rupees",
                "kuwait Dinar",
            ],
            "research_results": [],
        }
    )

    print("\nFINAL ANSWER\n")
    print(result["final_answer"])

    return result

research_result = run_parallel_research_workflow()
print(research_result)