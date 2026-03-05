import requests
BASE_URL="http://localhost:8000"


response=requests.post(
    f"{BASE_URL}/users",
    json={"email":"charlie@example.com","username":"charlie"}
)

print(f"Create: {response.status_code}")
print(response.json())
user_id=response.json()["id"]

# # READ all users
response=requests.get(f"{BASE_URL}/users")
print(f"\n READ ALL: {response.status_code}")
print(response.json())

# # READ single
# response=requests.get(f"{BASE_URL}/users/{user_id}")
# print(f"\nREAD ONE: {response.status_code}")
# print(response.json())

# #Update user
# response=requests.put(
#     f"{BASE_URL}/users/{user_id}",
#     json={"email":"charlie.new@example.com"}
# )
# print(f"\nUPDATE: {response.status_code}")
# print(response.json())

# #DELETE USER
# response=requests.delete(f"{BASE_URL}/users/{user_id}")
# print(f"\nDELETE: {response.status_code}")