from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from typing import Any

def reverse(s: str) -> str:
    return s[::-1]

def upper(_dict: dict[str, str]) -> dict:
    return {"output":_dict["output"].upper()}

runnable1 = RunnableLambda[str, str](func=reverse)
runnable2 = RunnableLambda[dict[str,str], dict](func=upper)

chain = runnable1 | {"output": RunnablePassthrough[Any]()} | runnable2

print(f"Output: {chain.invoke('reehduS')}")