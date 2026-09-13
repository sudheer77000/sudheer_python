import os

if not hasattr(os, "get_blocking"):
    os.get_blocking = lambda fd: True

if not hasattr(os, "set_blocking"):
    os.set_blocking = lambda fd, blocking: None

from dotenv import load_dotenv
from cursor_sdk import Cursor

load_dotenv()

api_key = os.getenv("CURSOR_API_KEY")

if not api_key:
    raise RuntimeError("CURSOR_API_KEY is not set")

models = Cursor.models.list(api_key=api_key)

print("Available models:")

for model in models:
    print(model.id)