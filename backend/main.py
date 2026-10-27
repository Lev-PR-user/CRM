from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from app.controller import URoute, RRoute
from app.controller import SERoute, ERoute
from app.controller import LRoute, SRoute
from app.controller import ORoute, TCRoute
from app.controller import CRoute, ORDERoute

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:7648"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

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
