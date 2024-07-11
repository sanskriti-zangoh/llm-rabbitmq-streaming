from fastapi import APIRouter
from fastapi.responses  import StreamingResponse
from depends.llm import generate_llm, generate_llm_stream, response_generator
from schemas.llm import LLMQuery

router = APIRouter(prefix="/llm", tags=["llm"])

@router.post("/generate")
async def generate_endpoint(query: str):
    # return StreamingResponse(generate_llm(query), media_type='text/event-stream')
    try:
        return {"message": await generate_llm(query)}
    except Exception as e:
        return {"message": str(e)}

@router.post("/stream")
async def stream_endpoint(query: str):
    try: 
        return StreamingResponse(generate_llm_stream(query), media_type='text/event-stream')
    except Exception as e:
        return {"message": str(e)}

@router.post("/streammq")
async def streammq_endpoint(query: LLMQuery):
    try: 
        await response_generator(query.query)
        return {"message": "streaming responses to the RabbitMQ queue"}
    except Exception as e:
        return {"message": str(e)}
