from langchain_core.runnables import RunnableLambda, RunnableParallel

def add_one(x: int) -> int:
    return x + 1

def mul_two(x: int) -> int:
    return x * 2

def mul_three(x: int) -> int:
    return x * 3

runnable_1 = RunnableLambda[int,int](func=add_one)
runnable_2 = RunnableLambda[int,int](func=mul_two)
runnable_3 = RunnableLambda[int,int](func=mul_three)

chain_dict = runnable_1 | RunnableParallel[int]({"mul_two":runnable_2,"mul_three":runnable_3})

print(f"Output: {chain_dict.invoke(1)}")