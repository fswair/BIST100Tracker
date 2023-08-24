from fastapi import FastAPI, Request, Response
from utils import BIST

app = FastAPI()
bist = BIST()

@app.get("/getShares")
async def get_shares(request: Request, response: Response):
    shares = []
    for share in bist.get_shares(as_json=True):
        share.pop("__pydantic_initialised__")
        shares.append(share)
    return shares