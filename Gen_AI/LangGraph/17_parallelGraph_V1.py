from langgraph.graph import StateGraph, START, END
from typing import TypedDict
import time

class Friends(TypedDict):
    init_msg: str
    Sudheer: str
    Sunil: str
    Siva: str
    Supin: str

def sudheer(state: Friends):
    print("Calling Sudheer....")
    time.sleep(5)
    return {"Sudheer":"I will join..."}

def sunil(state: Friends):
    print("Calling Sunil....")
    time.sleep(4)
    return {"Sunil":"I will join..."}

def siva(state: Friends):
    print("Calling Siva....")
    time.sleep(3)
    return {"Siva":"I will join..."}

def supin(state: Friends):
    print("Calling Supin....")
    time.sleep(2)
    return {"Supin":"I will join..."}

builder = StateGraph(Friends)

builder.add_node("sudheer", sudheer)
builder.add_node("sunil", sunil)
builder.add_node("siva", siva)
builder.add_node("supin", supin)

#builder.add_edge(START, "sudheer")
#builder.add_edge("sudheer", "sunil")
#builder.add_edge("sunil", "siva")
#builder.add_edge("siva", "supin")
#builder.add_edge("supin", END)

builder.add_edge(START, "sudheer")
builder.add_edge(START, "sunil")
builder.add_edge(START, "siva")
builder.add_edge(START, "supin")

graph = builder.compile()

question = input("Enter Question : ")
result = graph.invoke({"init_msg":question})
print(result)
