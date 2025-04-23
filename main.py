from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

FAKE_TOKEN = "secrettoken123"

def fake_decode_token(token):
    if token != FAKE_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"username": "demo"}

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == "demo" and form_data.password == "secret":
        return {"access_token": FAKE_TOKEN, "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Incorrect credentials")

@app.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return {"message": f"Hello {user['username']}, this is protected content"}
