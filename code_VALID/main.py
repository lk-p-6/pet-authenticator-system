import requests

apiUrl = "http://127.0.0.1:8000/verify"

print("Enter to secure system")

def code_validation(code):
    return code.isdigit() and len(code) == 6

while True:
    user_code = input("Enter the code: ")
    if not code_validation(user_code):
        print("Invalid format! Try again!")
        continue
    data_payload = {"code": user_code}

    try:
        r = requests.post(apiUrl, json=data_payload, timeout=3)
    except requests.exceptions.RequestException:
        print("Server responses with an error! Try again later or contact with the tech support.")
        continue

    if r.status_code >= 500:
        print("Server error. Try again later or contact with the tech support.")
        continue

    if r.status_code != 200:
        print("Request rejected. Try again.")
        continue

    try:
        response = r.json()
    except ValueError:
        print("Server error. Try again later or contact with the tech support")
        continue

    if response.get("isCorrect") is True:
        print("Access is granted!")
        break
    else:
        print("Access is not granted! Try again!")
    

print("Proccess ended")