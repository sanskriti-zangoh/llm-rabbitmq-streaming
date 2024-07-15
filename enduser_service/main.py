from fastapi import FastAPI
from contextlib import asynccontextmanager
from depends.consumer import RabbitMQClient, consumer
from routers.stream import router as stream_router
from fastapi.middleware.cors import CORSMiddleware

from middleware.timer import TimerMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend URL if you know it
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    consumer.connect()
    yield

@app.get("/")
async def root():
    return {"message": "Welcome to the End User Service"}

app.add_middleware(TimerMiddleware)
app.include_router(stream_router)


