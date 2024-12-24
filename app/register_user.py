import requests

url = "http://127.0.0.1:8000/auth/register"
data = {
    "user_name": "keerthana",
    "user_email": "jayackeerththana@gmail.com",
    "mobile_number": "1234567890",
    "password": "Apple@123"
}

response = requests.post(url, json=data)

if response.status_code == 200:
    print("User registered successfully:", response.json())
else:
    print("Error:", response.json())
