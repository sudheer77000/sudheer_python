
import os
import json
import urllib.request
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# ==========================================
# CONFIGURATION
# ==========================================
load_dotenv()


API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise ValueError("Please set your OPENAI_API_KEY environment variable.")

MODEL = os.getenv("OPENAI_MODEL", "gpt-5-nano")

client = OpenAI(api_key=API_KEY)

DOWNLOAD_FOLDER = Path("sales_downloads")
DOWNLOAD_FOLDER.mkdir(exist_ok=True)

# ==========================================
# SALES DATA
# ==========================================

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
# AI INSTRUCTIONS
# ==========================================

instructions = f"""
You are an intelligent AI Sales Analysis Assistant.

SALES DATA:
{json.dumps(sales_data)}

Your responsibilities:

1. Calculate total sales.
2. Calculate average sales.
3. Find highest and lowest sales.
4. Compare monthly sales.
5. Calculate quarterly sales.
6. Calculate growth percentages.
7. Generate sales charts.
8. Create Excel reports.
9. Generate PDF reports.
10. Perform basic sales forecasting.

IMPORTANT FILE GENERATION RULES:

When the user requests a chart:
- Use the Python Code Interpreter.
- Generate a real chart using matplotlib.
- Save it inside /mnt/data.
- Use a descriptive filename, such as sales_chart.png.

When the user requests Excel:
- Generate a real Excel file.
- Save it inside /mnt/data.

When the user requests PDF:
- Generate a real PDF file.
- Save it inside /mnt/data.

Do not merely describe or pretend to generate files.
Actually create the files using Python.

Explain results in simple business language.
Never invent sales figures.
Clearly distinguish forecasts from actual sales.
"""

# ==========================================
# DOWNLOAD GENERATED FILES
# ==========================================

def download_files(response):

    data = response.model_dump()

    container_id = None
    generated_files = []

    # Find container ID and generated file annotations

    for item in data.get("output", []):

        if item.get("type") == "code_interpreter_call":
            container_id = item.get("container_id")

        if item.get("type") == "message":

            for content in item.get("content", []):

                for annotation in content.get("annotations", []):

                    if annotation.get("type") == "container_file_citation":

                        container_id = (
                            annotation.get("container_id")
                            or container_id
                        )

                        file_id = annotation.get("file_id")
                        filename = annotation.get("filename")

                        if file_id and filename:
                            generated_files.append(
                                (file_id, filename)
                            )

    # Remove duplicate file references

    generated_files = list(dict.fromkeys(generated_files))

    if not generated_files:
        print("\nNo downloadable files were returned.")
        return

    if not container_id:
        print("\nContainer ID not found.")
        return

    # Download each generated file

    for file_id, filename in generated_files:

        safe_filename = Path(filename).name
        save_path = DOWNLOAD_FOLDER / safe_filename

        url = (
            f"https://api.openai.com/v1/containers/"
            f"{container_id}/files/{file_id}/content"
        )

        request = urllib.request.Request(
            url,
            headers={
                "Authorization": f"Bearer {API_KEY}"
            }
        )

        try:

            with urllib.request.urlopen(request) as result:

                file_content = result.read()

            with open(save_path, "wb") as output_file:
                output_file.write(file_content)

            print("\n" + "=" * 45)
            print("FILE DOWNLOADED SUCCESSFULLY")
            print("=" * 45)
            print("Filename:", safe_filename)
            print("Saved at:", save_path.resolve())

        except Exception as error:

            print("\nFile download failed:", error)


# ==========================================
# CHAT FUNCTION
# ==========================================

previous_response_id = None


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

        # Display AI response

        print("\nAI Sales Assistant:")
        print(response.output_text)

        # Automatically download generated files

        download_files(response)

    except Exception as error:

        print("\nAPI Error:", error)


# ==========================================
# MAIN CHAT INTERFACE
# ==========================================

def main():

    print("\n" + "=" * 55)
    print("          AI SALES ANALYSIS CHATBOT")
    print("=" * 55)

    print("\nWelcome! Ask questions about your sales.")

    print("\nExample questions:")

    print("1. What are my total sales?")
    print("2. Which month performed best?")
    print("3. Calculate average sales.")
    print("4. Compare January and February.")
    print("5. Show quarterly sales.")
    print("6. Generate a sales chart.")
    print("7. Create an Excel sales report.")
    print("8. Generate a PDF report.")
    print("9. Forecast next month's sales.")

    print("\nGenerated files will be saved in:")
    print(DOWNLOAD_FOLDER.resolve())

    print("\nType EXIT to close.")

    while True:

        question = input("\nYou: ").strip()

        if question.lower() in ["exit", "quit", "bye"]:

            print("\nThank you for using AI Sales Assistant!")
            break

        if not question:
            continue

        print("\nAnalyzing your request...")

        sales_chat(question)


# ==========================================
# START PROGRAM
# ==========================================

if __name__ == "__main__":
    main()
