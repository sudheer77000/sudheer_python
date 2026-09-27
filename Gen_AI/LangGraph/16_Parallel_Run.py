import time
from typing import TypedDict

from langgraph.graph import StateGraph, START, END


# ============================================================
# 1. WEB SUBGRAPH
# ============================================================

class WebState(TypedDict):
    query: str
    web_result: str


def web_search(state: WebState):
    print("\n🌐 WEB: Started")
    
    for i in range(5):
        time.sleep(1)
        print(f"🌐 WEB: {i + 1} second")

    print("🌐 WEB: Finished")

    return {
        "web_result": f"Web result for '{state['query']}'"
    }


web_builder = StateGraph(WebState)

web_builder.add_node("search", web_search)

web_builder.add_edge(START, "search")
web_builder.add_edge("search", END)

web_graph = web_builder.compile()


# ============================================================
# 2. DB SUBGRAPH
# ============================================================

class DBState(TypedDict):
    query: str
    db_result: str


def db_search(state: DBState):
    print("\n🗄️ DB: Started")

    for i in range(5):
        time.sleep(1)
        print(f"🗄️ DB: {i + 1} second")

    print("🗄️ DB: Finished")

    return {
        "db_result": f"DB result for '{state['query']}'"
    }


db_builder = StateGraph(DBState)

db_builder.add_node("search", db_search)

db_builder.add_edge(START, "search")
db_builder.add_edge("search", END)

db_graph = db_builder.compile()


# ============================================================
# 3. PARENT GRAPH
# ============================================================

class ParentState(TypedDict):
    query: str
    web_result: str
    db_result: str


def run_web(state: ParentState):
    result = web_graph.invoke({
        "query": state["query"]
    })

    return {
        "web_result": result["web_result"]
    }


def run_db(state: ParentState):
    result = db_graph.invoke({
        "query": state["query"]
    })

    return {
        "db_result": result["db_result"]
    }


def combine(state: ParentState):
    print("\n🔄 COMBINE: Both branches finished")

    print("Web:", state["web_result"])
    print("DB :", state["db_result"])

    return state


builder = StateGraph(ParentState)

builder.add_node("web", run_web)
builder.add_node("db", run_db)
builder.add_node("combine", combine)


# ============================================================
# PARALLEL BRANCHES
# ============================================================

builder.add_edge(START, "web")
builder.add_edge(START, "db")


# combine waits for BOTH
builder.add_edge("web", "combine")
builder.add_edge("db", "combine")

builder.add_edge("combine", END)


graph = builder.compile()


# ============================================================
# RUN
# ============================================================

print("🚀 Starting graph...")

start_time = time.time()

result = graph.invoke({
    "query": "What is LangGraph?",
    "web_result": "",
    "db_result": ""
})

end_time = time.time()

print("\n✅ Graph finished")
print(f"⏱️ Total time: {end_time - start_time:.2f} seconds")