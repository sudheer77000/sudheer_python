from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_ollama import ChatOllama


# ============================================================
# BANK SERVICE
# ============================================================

class BankService:

    def __init__(self):
        self.accounts = {
            "1001": {
                "name": "Sudheer",
                "balance": 50000
            },
            "1002": {
                "name": "Ravi",
                "balance": 30000
            }
        }

    # ========================================================
    # NORMAL METHOD 1
    # ========================================================

    def validate_account(self, account_id):
        print(f"[METHOD] validate_account({account_id})")

        if account_id not in self.accounts:
            raise ValueError("Account not found")

        return True

    # ========================================================
    # NORMAL METHOD 2
    # ========================================================

    def get_balance(self, account_id):
        print(f"[METHOD] get_balance({account_id})")

        self.validate_account(account_id)

        return self.accounts[account_id]["balance"]

    # ========================================================
    # NORMAL METHOD 3
    # ========================================================

    def update_balance(self, account_id, amount):
        print(
            f"[METHOD] update_balance("
            f"{account_id}, {amount})"
        )

        self.accounts[account_id]["balance"] += amount

    # ========================================================
    # NORMAL METHOD 4
    # ========================================================

    def transfer(self, from_account, to_account, amount):
        print(
            f"[METHOD] transfer("
            f"{from_account}, {to_account}, {amount})"
        )

        self.validate_account(from_account)
        self.validate_account(to_account)

        if self.accounts[from_account]["balance"] < amount:
            return "Insufficient balance"

        self.update_balance(
            from_account,
            -amount
        )

        self.update_balance(
            to_account,
            amount
        )

        return f"Successfully transferred {amount}"


# ============================================================
# CREATE BANK OBJECT
# ============================================================

bank = BankService()


# ============================================================
# TOOL 1
# ============================================================

@tool
def get_account_balance(account_id: str):
    """Get the current balance of a bank account."""

    print(f"[TOOL] get_account_balance({account_id})")

    return bank.get_balance(account_id)


# ============================================================
# TOOL 2
# ============================================================

@tool
def transfer_money(
    from_account: str,
    to_account: str,
    amount: float
):
    """Transfer money from one bank account to another."""

    print(
        f"[TOOL] transfer_money("
        f"{from_account}, "
        f"{to_account}, "
        f"{amount})"
    )

    return bank.transfer(
        from_account,
        to_account,
        amount
    )


# ============================================================
# MODEL
# ============================================================

model = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)


# ============================================================
# AGENT
# ============================================================

agent = create_agent(
    model=model,
    tools=[
        get_account_balance,
        transfer_money
    ]
)


# ============================================================
# USER QUERY
# ============================================================

print("\n===== USER QUERY =====")
Query = input("Please Enter The Query : ")

response = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": Query
        }
    ]
})


# ============================================================
# FINAL RESPONSE
# ============================================================

print("\n===== FINAL RESPONSE =====")

print(response["messages"][-1].content)