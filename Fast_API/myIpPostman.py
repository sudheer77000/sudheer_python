import requests
url = 'https://postman-echo.com/ip'
try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    ip =  data['ip']
    print(f"My public IP address is: {ip}")
except Exception as e:
    print(f"An error occurred: {e}")