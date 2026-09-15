from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

# ---------------------------------------
# 1. Create LLM
# ---------------------------------------

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)


# ---------------------------------------
# 2. Create Chat Prompt
# ---------------------------------------

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful AI assistant."
    ),

    # Dynamic conversation history
    MessagesPlaceholder(
        variable_name="history"
    ),

    # Current user question
    (
        "human",
        "{question}"
    )
])


# ---------------------------------------
# 3. Create LCEL Chain
# ---------------------------------------

chain = prompt | llm | StrOutputParser()


# ---------------------------------------
# 4. Conversation History
# ---------------------------------------

history = []


# ---------------------------------------
# 5. Command Prompt Chat Loop
# ---------------------------------------

print("====================================")
print("      LangChain CLI Chatbot")
print("====================================")
print("Type 'exit' to stop.\n")


while True:

    # Read input from command prompt
    question = input("You: ")

    # Exit
    if question.lower() == "exit":
        print("Goodbye!")
        break

    # -----------------------------------
    # Send question + history to chain
    # -----------------------------------

    response = chain.invoke({
        "history": history,
        "question": question
    })

    # -----------------------------------
    # Display AI response
    # -----------------------------------

    print("AI:", response)
    print()

    # -----------------------------------
    # Add conversation to history
    # -----------------------------------

    history.append(
        HumanMessage(content=question)
    )

    history.append(
        AIMessage(content=response)
    )