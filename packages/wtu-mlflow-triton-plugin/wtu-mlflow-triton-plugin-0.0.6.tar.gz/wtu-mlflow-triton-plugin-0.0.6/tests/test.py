import requests

response = requests.post(
    "https://kitech-triton.wimcorp.dev/v2/repository/index", allow_redirects=True
)
if response.status_code == 200:
    print(response.json())
else:
    print(f"오류 발생: {response.status_code}")
