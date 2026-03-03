from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import httpx
import os
from auth import verify_token

app = FastAPI()

CARD_SERVICE_URL = os.getenv("CARD_SERVICE_URL")


class StatusUpdate(BaseModel):
    status: str


class LimitUpdate(BaseModel):
    transaction_limit: float


@app.get("/")
def root():
    return {"message": "Debit Service Running"}


@app.get("/debit/{card_id}/status")
async def get_status(card_id: str, user=Depends(verify_token)):
    async with httpx.AsyncClient() as client:

        response = await client.get(
            f"{CARD_SERVICE_URL}/cards/{card_id}",
            headers={"Authorization": auth_header})

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Card service error")

        return {"status": response.json()["status"]}


@app.patch("/debit/{card_id}/status")
async def update_status(card_id: str, body: StatusUpdate, user=Depends(verify_token)):
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{CARD_SERVICE_URL}/cards/{card_id}",
            json={"status": body.status}
        )

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Update failed")

        return {"message": "Status updated"}


@app.patch("/debit/{card_id}/limits")
async def update_limits(card_id: str, body: LimitUpdate, user=Depends(verify_token)):
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{CARD_SERVICE_URL}/cards/{card_id}",
            json={"transaction_limit": body.transaction_limit}
        )

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Limit update failed")

        return {"message": "Limits updated"}