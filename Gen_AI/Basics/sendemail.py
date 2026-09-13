import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()
gmail = os.getenv("G_MAIL")
pwd = os.getenv("G_MAIL_APP_PWD")

def send_email(to_email: str, subject: str, body: str):
    sender_email = gmail
    app_password = pwd

    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, app_password)
        smtp.send_message(msg)

    return "Email sent successfully"


# Test
if __name__ == "__main__":
    result = send_email(
        "sudheergundra@gmail.com",
        "Test Email",
        "Hello, this email was sent using Python."
    )

    print(result)