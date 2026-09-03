from typing_extensions import TypedDict
import random
from typing import Literal
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    graph_info : str

def start_play(state:State):
        print("Start Play Node has been called...")
        return{"graph_info":state["graph_info"] + " I am planning to play"}
def cricket(state:State):
        print("Cricket Node has been called...")
        return{"graph_info":state["graph_info"] + " Cricket"}
def badminton(state:State):
        print("Badminton Node has been called...")
        return{"graph_info":state["graph_info"] + " Badminton"}

def random_play(state: State) -> Literal['cricket','badminton']:
       rand = random.randint(1, 10)
       print(rand)
       if rand > 5:
              return "cricket"
       else:
              return "badminton"

# Build The Graph
graph = StateGraph(State)

graph.add_node("start_play",start_play)
graph.add_node("cricket",cricket)
graph.add_node("badminton",badminton)

graph.add_edge(START,"start_play")
graph.add_conditional_edges("start_play",random_play)
graph.add_edge("cricket",END)
graph.add_edge("badminton",END)

graph_builder = graph.compile()


# Invoke the graph
result = graph_builder.invoke(
    {"graph_info": "My name is Sudheer"}
)

print("Final Result:")
print(result)
       
    

