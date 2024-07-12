from pydantic import BaseModel

class LLMQuery(BaseModel):
    query: str