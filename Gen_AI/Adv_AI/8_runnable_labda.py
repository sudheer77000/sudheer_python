from langchain_core.runnables import RunnableLambda

def reverse(s: str) -> str:
    return s[::-1]

def upper(s: str) -> str:
    return s.upper()


runnable1 = RunnableLambda[str, str](func=reverse)
runnable2 = RunnableLambda[str, str](func=upper)

chain = runnable1 | runnable2

print(f"Output: {chain.invoke('reehduS')}")