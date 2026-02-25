from fastapi import FastAPI
import requests

app = FastAPI()

CARD_SERVICE_URL = "https://your-card-store.onrender.com"

@app.get("/debit/{card_id}/status")
def get_status(card_id: str):
    response = requests.get(f"{CARD_SERVICE_URL}/cards/{card_id}")
    return {"status": response.json()["status"]}

@app.patch("/debit/{card_id}/status")
def update_status(card_id: str, body: dict):
    response = requests.put(
        f"{CARD_SERVICE_URL}/cards/{card_id}",
        json={"status": body["status"]}
    )
    return {"message": "Status updated"}

@app.patch("/debit/{card_id}/limits")
def update_limits(card_id: str, body: dict):
    response = requests.put(
        f"{CARD_SERVICE_URL}/cards/{card_id}",
        json=body
    )
    return {"message": "Limits updated"}