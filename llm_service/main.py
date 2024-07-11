from fastapi import FastAPI
from routers.llm import router as llm_router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the LLM Service"}

app.include_router(llm_router)