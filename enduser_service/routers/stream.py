from fastapi import APIRouter
from depends.consume import consume
from fastapi.responses import StreamingResponse
import requests
from schemas.llm import LLMQuery

router = APIRouter(prefix="/stream", tags=["stream"])

@router.post("/mq")
async def streammq_endpoint(query: LLMQuery):
    try: 
        response = requests.post("http://llm_service:5000/llm/streammq", json=query.model_dump())
        return StreamingResponse(consume(), media_type='text/event-stream')
    except Exception as e:
        return {"message": str(e)}