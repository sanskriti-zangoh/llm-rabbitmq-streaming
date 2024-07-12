from fastapi import APIRouter
from depends.consume import consume, message_stream
from depends.consumer import RabbitMQClient, consumer
from fastapi.responses import StreamingResponse
from fastapi.exceptions import HTTPException
import requests
from schemas.llm import LLMQuery
import os

router = APIRouter(prefix="/stream", tags=["stream"])

# @router.post("/mq")
# async def streammq_endpoint(query: LLMQuery):
#     try:
#         consumer.start_consume(queue_name=os.getenv("QUEUE_NAME"))
#         return StreamingResponse(consumer._consume(), media_type="text/plain")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@router.post("/mq")
async def streammq_endpoint(query: LLMQuery):
    response = requests.post("http://llm_service:5000/llm/streammq", json=query.model_dump())
    return StreamingResponse(message_stream(), media_type="text/event-stream")