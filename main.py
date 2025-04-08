from fastapi import FastAPI
from app.routes import auth_route
from dotenv import load_dotenv
app = FastAPI()
load_dotenv()

app.include_router(auth_route.router, prefix="/api", tags=["Users"])

