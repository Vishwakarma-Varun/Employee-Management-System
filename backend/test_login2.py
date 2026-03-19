import urllib.request
import json

data = json.dumps({"email": "admin@company.com", "password": "Admin@1234"}).encode("utf-8")
req = urllib.request.Request("http://localhost:8000/api/auth/login", data=data, headers={"Content-Type": "application/json"})

try:
    with urllib.request.urlopen(req, timeout=5) as res:
        print("STATUS:", res.status)
        print("BODY:", res.read().decode("utf-8"))
except urllib.error.HTTPError as e:
    print("HTTP ERROR:", e.code)
    print("ERROR BODY:", e.read().decode("utf-8"))
except Exception as e:
    print("ERROR:", str(e))
