from langchain_core.runnables import RunnableLambda, RunnableParallel

def add_ten(x: dict) -> dict:
    return {"added": x["input"] + 10}

mapper = RunnableParallel[dict](
    {
        "add_step" : RunnableLambda[dict,dict](add_ten),
        "add_step_2" : RunnableLambda[dict,dict](add_ten),
    }
)

print(f"Output: {mapper.invoke({'input':10})}")