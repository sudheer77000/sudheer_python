from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate

examples = [
    {
        "review": "The UI is incredibly clunky and it crashes every time I try to save.",
        "sentiment": "Negative",
        "reason": "The user explicitly mentions usability issues ('clunky') and functional failures ('crashes')."
    },
    {
        "review": "Absolutely love the new dark mode feature! My eyes are so happy.",
        "sentiment": "Positive",
        "reason": "The user expresses strong positive emotion ('Absolutely love') and praises a specific feature."
    }
]

