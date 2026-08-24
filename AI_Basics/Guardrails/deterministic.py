BANNED_KEYWORDS = {
    "violence": [
        "kill", "murder", "bomb", "explosive", "grenade",
        "firearm", "weapon"
    ],
    "self_harm": [
        "suicide", "self harm", "kill myself", "end my life"
    ],
    "drugs": [
        "cocaine", "heroin", "meth", "fentanyl"
    ],
    "cybercrime": [
        "malware", "ransomware", "credential theft",
        "password cracking", "ddos"
    ],
    "fraud": [
        "money laundering", "identity theft",
        "credit card fraud", "forgery"
    ]
}


def check_guardrail(user_input):
    text = user_input.lower()

    matches = []

    for category, keywords in BANNED_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                matches.append({
                    "category": category,
                    "keyword": keyword
                })

    return matches


# Get input from user
user_input = input("Enter your question: ")

# Check guardrail
result = check_guardrail(user_input)

if result:
    print("\n❌ BLOCKED")
    print("Detected:", result)
else:
    print("\n✅ ALLOWED")