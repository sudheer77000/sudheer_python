from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)
from langchain_core.messages import HumanMessage, AIMessage
from langchain_ollama import ChatOllama


prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Please respond in 5 to 10 words"),
    MessagesPlaceholder(
        variable_name="chat_history"
    ),

    ("human", "{question}")
])


llm = ChatOllama(
    model="qwen2.5:3b"
)

chain = prompt | llm


# Initially empty
chat_history = []


while True:

    # Read user input
    question = input("\nSudheer: ")

    if question.lower() == "exit":
        break

    # Invoke chain with current chat history
    response = chain.invoke({
        "chat_history": chat_history,
        "question": question
    })
    print("**************************")
    print(chat_history)
    print("**************************")
    print("AI:", response.content)

    # Dynamically add current conversation
    chat_history.append(
        HumanMessage(content=question)
    )

    chat_history.append(
        AIMessage(content=response.content)
    )