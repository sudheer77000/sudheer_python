from langchain_core.tools import tool


# ------------------------------------------------
# NORMAL METHOD
# ------------------------------------------------

class CustomerService:

    def get_customer_from_db(self, customer_id):
        """Normal Python method."""
        
        customers = {
            101: {"name": "Sudheer", "city": "Dubai"},
            102: {"name": "Ravi", "city": "Hyderabad"}
        }

        return customers.get(customer_id, "Customer not found")


# Create object
customer_service = CustomerService()


# ------------------------------------------------
# TOOL 1
# ------------------------------------------------

@tool
def get_customer(customer_id: int):
    """Get customer details using customer ID."""

    # Calling the normal method internally
    return customer_service.get_customer_from_db(customer_id)


# ------------------------------------------------
# TOOL 2
# ------------------------------------------------

@tool
def calculate_discount(amount: float):
    """Calculate 10% discount for a purchase amount."""

    discount = amount * 0.10
    final_amount = amount - discount

    return {
        "discount": discount,
        "final_amount": final_amount
    }


# ------------------------------------------------
# TEST THE TOOLS
# ------------------------------------------------

cust_id = int(input("Please Enter Customer ID : "))
result1 = get_customer.invoke({"customer_id": cust_id})

print("Customer:")
print(result1)

amount = int(input("Please Enter Amount : "))
result2 = calculate_discount.invoke({"amount": amount})

print("\nDiscount:")
print(result2)