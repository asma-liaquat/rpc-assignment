import requests

SERVER_URL = "https://rpc-assignment-production.up.railway.app"

def add(x, y):
    response = requests.post(f"{SERVER_URL}/add", json={'x': x, 'y': y})
    return response.json().get('result')

def multiply(x, y):
    response = requests.post(f"{SERVER_URL}/multiply", json={'x': x, 'y': y})
    return response.json().get('result')

if __name__ == "__main__":
    print("Addition of 5 and 3:", add(5, 3))
    print("Multiplication of 5 and 3:", multiply(5, 3))