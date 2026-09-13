import os
from dotenv import load_dotenv
from cursor_sdk import Agent
load_dotenv()

api_key = os.getenv("CURSOR_API_KEY")
if not hasattr(os, "get_blocking"):
    os.get_blocking = lambda fd: True

if not hasattr(os, "set_blocking"):
    os.set_blocking = lambda fd, blocking: None


if not api_key:
    raise RuntimeError("CURSOR_API_KEY is not set")


with Agent.create(
    model="gemini-3.7-flash",
    api_key=api_key,
    local={"cwd": os.getcwd()},
) as agent:

    response = agent.send(
        "What are the top 10 cities in UAE? in 10 words"
    )
    print(response)
    print(response.text())