from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.controller import URoute, DURoute, RRoute
from app.controller import SERoute, ERoute, PERoute
from app.controller import LRoute, SRoute
from app.controller import ORoute, TCRoute
from app.controller import CRoute, PCRoute, ORDERoute

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(os.getenv("HOST"))],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

""""Публичные маршруты"""
app.include_router(DURoute)
app.include_router(PCRoute)
app.include_router(PERoute)

"""Защищенные маршруты"""
app.include_router(URoute)
app.include_router(RRoute)
app.include_router(SERoute)
app.include_router(ERoute)
app.include_router(LRoute)
app.include_router(SRoute)
app.include_router(ORoute)
app.include_router(TCRoute)
app.include_router(CRoute)
app.include_router(ORDERoute)


@app.get("/")
async def root():
    return {"messege": "Приложкние запущено"}
