import requests

url = "https://postman-echo.com/basic-auth"

username = "postman"
password = "password"

response = requests.get(
    url,
    auth=(username, password)
)

print(response.status_code)
print(response.json())