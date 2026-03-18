import requests

data = {
    "temperature": 50,
    "gas": 400,
    "pulse": 130
}

try:
    res = requests.post("http://127.0.0.1:5001/data", json=data)
    print("Status Code:", res.status_code)
    print("Response:", res.text)
except Exception as e:
    print("Error:", e)