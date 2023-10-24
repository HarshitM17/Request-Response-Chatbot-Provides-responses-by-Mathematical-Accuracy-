import requests

url = "http://localhost:8000/ask"
data = {"question": "Hello, DOST!"}  # Replace with your actual question
response = requests.post(url, json=data)

print(response.status_code)
print(response.json())
