from langchain_core.runnables import RunnableBranch


branch = RunnableBranch(
    (lambda x: x > 10, lambda x: f"{x} is greater than 10"),
    (lambda x: x > 5, lambda x: f"{x} is greater than 5"),
    lambda x: f"{x} is 5 or less"
)


print(branch.invoke(15))
print(branch.invoke(8))
print(branch.invoke(3))