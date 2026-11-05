
import os
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

client = OpenAI()

# ==========================================
# AI SALES CHATBOT - SINGLE PYTHON PROGRAM
# ==========================================

MODEL="gpt-5-nano"

# Sample sales data
sales_data = {
    "January": 12000,
    "February": 15000,
    "March": 18000,
    "April": 14000,
    "May": 22000,
    "June": 25000,
    "July": 20000,
    "August": 28000,
    "September": 30000,
    "October": 27000,
    "November": 35000,
    "December": 40000
}

# ==========================================
# SYSTEM INSTRUCTIONS
# ==========================================

instructions = f"""
You are an intelligent AI Sales Analysis Assistant.

Analyze the following sales dataset:

{sales_data}

You can:
1. Calculate total sales.
2. Calculate average sales.
3. Find highest and lowest sales.
4. Compare monthly sales.
5. Calculate quarterly sales.
6. Calculate growth percentages.
7. Generate sales charts.
8. Perform basic sales forecasting.
9. Explain business performance.

IMPORTANT:
- Use Python Code Interpreter for calculations.
- Do not invent sales figures.
- Clearly distinguish actual data from forecasts.
- Give answers in simple business language.
- Generate charts when requested.
"""

# ==========================================
# CHAT HISTORY
# ==========================================

previous_response_id = None


# ==========================================
# CHAT FUNCTION
# ==========================================

def sales_chat(question):

    global previous_response_id

    try:

        response = client.responses.create(

            model=MODEL,

            instructions=instructions,

            tools=[
                {
                    "type": "code_interpreter",
                    "container": {
                        "type": "auto"
                    }
                }
            ],

            input=question,

            previous_response_id=previous_response_id

            if previous_response_id else None

        )

        previous_response_id = response.id

        return response.output_text

    except Exception as e:

        return f"Error: {str(e)}"


# ==========================================
# MAIN CHAT INTERFACE
# ==========================================

def main():

    print("\n" + "=" * 55)
    print("          AI SALES ANALYSIS CHATBOT")
    print("=" * 55)

    print("\nWelcome! Ask me anything about your sales.")

    print("\nExample questions:")
    print("- What are my total sales?")
    print("- Which month had the highest sales?")
    print("- Calculate average monthly sales.")
    print("- Compare January and February.")
    print("- Show quarterly sales.")
    print("- Generate a sales chart.")
    print("- Forecast next month's sales.")

    print("\nType EXIT to close the chatbot.")

    while True:

        question = input("\nYou: ").strip()

        if question.upper() in ["EXIT", "QUIT", "BYE"]:

            print("\nThank you for using AI Sales Assistant!")
            break

        if not question:
            continue

        print("\nAI Sales Assistant: Thinking...")

        answer = sales_chat(question)

        print("\nAI Sales Assistant:")
        print(answer)


# ==========================================
# START PROGRAM
# ==========================================

if __name__ == "__main__":
    main()
