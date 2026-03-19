import requests
try:
    res = requests.post("http://localhost:8000/api/auth/login", json={"email": "admin@company.com", "password": "Admin@1234"}, timeout=5)
    print("STATUS:", res.status_code)
    print("BODY:", res.text)
except Exception as e:
    print("ERROR:", str(e))
