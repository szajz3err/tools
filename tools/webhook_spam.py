import requests

def webhook_spam():
    url = input("Webhook URL: ")
    msg = input("Wiadomość do spamu: ")
    times = int(input("Ile razy spamować: "))
    for i in range(times):
        resp = requests.post(url, json={"content": msg})
        print(f"#{i+1} {resp.status_code} {resp.text}")