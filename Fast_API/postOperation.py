import requests
url = "https://postman-echo.com/post"

data = {
    "name": "Sudheer",
    "age": 37,
    "city": "Dubai"
}
response = requests.post(url,json=data)
print(response.status_code)
print(response.json())