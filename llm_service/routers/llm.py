from fastapi import APIRouter, Depends
from fastapi.responses  import StreamingResponse
from depends.llm import generate_llm, generate_llm_stream, stream_response_queue, stream_response
from depends.producer import get_producer, RabbitMQProducer
from schemas.llm import LLMQuery

router = APIRouter(prefix="/llm", tags=["llm"])

@router.post("/generate")
async def generate_endpoint(query: LLMQuery):
    # return StreamingResponse(generate_llm(query), media_type='text/event-stream')
    try:
        return {"message": await generate_llm(query.query)}
    except Exception as e:
        return {"message": str(e)}

@router.post("/stream")
async def stream_endpoint(query: LLMQuery):
    try: 
        return StreamingResponse(generate_llm_stream(query.query), media_type='text/event-stream')
    except Exception as e:
        return {"message": str(e)}
    
@router.post("/streamer")
async def streamer_endpoint(query: LLMQuery):
    try: 
        return StreamingResponse(stream_response(query.query), media_type='text/event-stream')
    except Exception as e:
        return {"message": str(e)}
    
@router.post("/streammq")
async def streammq_endpoint(query: LLMQuery, streamer_queue: RabbitMQProducer = Depends(get_producer)):
    try: 
        await stream_response_queue(query.query, streamer_queue)
        return {"message": "streaming responses to the RabbitMQ queue"}
    except Exception as e:
        return {"message": str(e)}    
