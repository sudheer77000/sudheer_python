import os

# Windows workaround for cursor-sdk
if not hasattr(os, "get_blocking"):
    os.get_blocking = lambda fd: True

if not hasattr(os, "set_blocking"):
    os.set_blocking = lambda fd, blocking: None

from dotenv import load_dotenv
from cursor_sdk import Agent
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

load_dotenv()


class CursorLLM:

    def __init__(self, model):
        self.model = model

        self.api_key = os.getenv("CURSOR_API_KEY")

        if not self.api_key:
            raise RuntimeError("CURSOR_API_KEY is not set")

    def invoke(self, messages):

        prompt = self._convert_messages(messages)

        with Agent.create(
            model=self.model,
            api_key=self.api_key,
            local={"cwd": os.getcwd()}
        ) as agent:

            response = agent.send(prompt)

        return response.text()

    def _convert_messages(self, messages):

        prompt = ""

        for message in messages:

            if isinstance(message, SystemMessage):
                prompt += f"System: {message.content}\n\n"

            elif isinstance(message, HumanMessage):
                prompt += f"Human: {message.content}\n\n"

            elif isinstance(message, AIMessage):
                prompt += f"Assistant: {message.content}\n\n"

        return prompt