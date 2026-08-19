from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import stripe
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


class PaymentRequest(BaseModel):
    payment_method_id: str
    amount: int


@app.get("/")
def home():
    return FileResponse("index.html")


@app.post("/create-payment")
def create_payment(request: PaymentRequest):

    payment_intent = stripe.PaymentIntent.create(
        amount=request.amount,
        currency="usd",
        payment_method=request.payment_method_id,
        confirm=True,
        automatic_payment_methods={
            "enabled": True,
            "allow_redirects": "never"
        }
    )

    return {
        "payment_id": payment_intent.id,
        "status": payment_intent.status,
        "amount": payment_intent.amount,
        "currency": payment_intent.currency
    }