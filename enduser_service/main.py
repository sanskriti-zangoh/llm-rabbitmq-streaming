from fastapi import FastAPI
from contextlib import asynccontextmanager
from depends.consumer import RabbitMQClient, consumer
from routers.stream import router as stream_router


app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    consumer.connect()
    yield

@app.get("/")
async def root():
    return {"message": "Welcome to the End User Service"}


app.include_router(stream_router)


