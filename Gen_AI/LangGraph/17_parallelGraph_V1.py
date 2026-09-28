from langgraph.graph import StateGraph, START, END
from typing import TypedDict
import time

## Sub Graph Start
class BookTickets(TypedDict):
    Initiate: str
    Name: int
    Source: str
    Destination: str

def name(state: BookTickets):
    #print("Name.....")
    return {"Name": state['Initiate']}

def source(state: BookTickets):
    #print("Source....")
    return {"Source":"Hyderabad"}

def destination(state: BookTickets):
    #print("Destination....")
    return {"Destination":"Goa"}

sub_builder = StateGraph(BookTickets)

sub_builder.add_node("name", name)
sub_builder.add_node("source", source)
sub_builder.add_node("destination", destination)

sub_builder.add_edge(START, "name")
sub_builder.add_edge("name", "source")
sub_builder.add_edge("source", "destination")
sub_builder.add_edge("destination", END)

sub_graph = sub_builder.compile()
#sub_result = sub_graph.invoke({"Initiate":"Sudheer"})
#print(sub_result)

## Sub Graph END

class Friends(TypedDict):
    init_msg: str
    Sudheer: str
    Sunil: str
    Siva: str
    Supin: str

def sudheer(state: Friends):
    print("Calling Sudheer....")
    time.sleep(1)
    sub_result = sub_graph.invoke({"Initiate":"Sudheer"})
    print(sub_result)
    return {"Sudheer":"I will join..."}

def sunil(state: Friends):
    print("Calling Sunil....")
    time.sleep(1)
    sub_result = sub_graph.invoke({"Initiate":"Sunil"})
    print(sub_result)
    return {"Sunil":"I will join..."}

def siva(state: Friends):
    print("Calling Siva....")
    time.sleep(1)
    sub_result = sub_graph.invoke({"Initiate":"Siva"})
    print(sub_result)
    return {"Siva":"I will join..."}

def supin(state: Friends):
    print("Calling Supin....")
    time.sleep(1)
    sub_result = sub_graph.invoke({"Initiate":"Supin"})
    print(sub_result)
    return {"Supin":"I will join..."}

builder = StateGraph(Friends)

builder.add_node("sudheer", sudheer)
builder.add_node("sunil", sunil)
builder.add_node("siva", siva)
builder.add_node("supin", supin)

builder.add_edge(START, "sudheer")
builder.add_edge("sudheer", "sunil")
builder.add_edge("sunil", "siva")
builder.add_edge("siva", "supin")
builder.add_edge("supin", END)

#builder.add_edge(START, "sudheer")
#builder.add_edge(START, "sunil")
#builder.add_edge(START, "siva")
#builder.add_edge(START, "supin")

graph = builder.compile()

question = input("Enter Question : ")
result = graph.invoke({"init_msg":question})
print("##" * 75)
print(result)
