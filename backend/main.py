from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.controller import ACRoute, AORoute, ASRoute, ALRoute, AERoute, ASERoute, ATCRoute
from app.controller import MAORoute, MAERoute, MATCRoute, MASERoute, MACRoute

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
app.include_router(PSRoute)


"""Админ маршруты"""
app.include_router(ACRoute)
app.include_router(AORoute)
app.include_router(ASRoute)
app.include_router(ALRoute)
app.include_router(AERoute)
app.include_router(ASERoute)
app.include_router(ATCRoute)

""""Менеджер маршруты"""
app.include_router(MAORoute)
app.include_router(MAERoute)
app.include_router(MATCRoute)
app.include_router(MASERoute)
app.include_router(MACRoute)


@app.get("/")
async def root():
    return {"messege": "Приложкние запущено"}
