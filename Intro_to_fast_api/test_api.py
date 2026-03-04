import requests

response=requests.get("http://0.0.0.0:8000/ping")
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

response=requests.get("http://0.0.0.0:8000/hello/Ada?greeting=lo",verify=False)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")