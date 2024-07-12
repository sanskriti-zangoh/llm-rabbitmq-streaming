from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import BaseMessage, HumanMessage, LLMResult
from langchain.schema.messages import BaseMessageChunk
from dotenv import load_dotenv, find_dotenv
import os
import getpass
import requests
from pydantic import BaseModel
from typing import List
import asyncio

class Part(BaseModel):
    text: str

class Content(BaseModel):
    parts: List[Part]

class LLMQuery(BaseModel):
    contents: List[Content]

    @classmethod
    def from_string(cls, text: str):
        return cls(contents=[Content(parts=[Part(text=text)])])
        

load_dotenv(find_dotenv())

def test1():
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GOOGLE_API_KEY"))
    response = llm.generate([[HumanMessage(content="write a romantic poem about a man")]],stream=True)
    print(response.generations[0][0].text)

def test2():
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GOOGLE_API_KEY"), callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))
    response = llm.generate([[HumanMessage(content="write a romantic poem about a man")]],stream=True)
    print(response.generations[0][0].text)
    print(len(response.generations[0]))

def test3():
    api_key = os.getenv("GOOGLE_API_KEY")
    print(f"API Key: {api_key}")  # Debug print
    llm = ChatGoogleGenerativeAI(model="models/text-bison-001", google_api_key=os.getenv("GOOGLE_API_KEY"))
    response = llm.invoke([HumanMessage(content="write a romantic poem about a man")])
    print(response)

def test4():
    # curl \
    # -H 'Content-Type: application/json' \
    # -d '{"contents":[{"parts":[{"text":"Explain how AI works"}]}]}' \
    # -X POST 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=AIzaSyB6oPl8Y83kfASqr1qWTffytT3PQyak528'
    query = LLMQuery.from_string("Hello, how are you")
    google_url = "https://generativelanguage.googleapis.com/v1beta/models"
    api_key = os.getenv("GOOGLE_API_KEY")
    model_name = "gemini-pro"
    task = "generateContent"
    response = requests.post(f"{google_url}/{model_name}:{task}?key={api_key}", json=query.model_dump(), stream=True)

async def test5():
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GOOGLE_API_KEY"))
    query = [HumanMessage(content="write a patriotic poem (Indian)")]
    async for response in llm.astream_events(query, version='v2'):
        print(response)
    # async for response in llm.astream_events(query, version='v2'):
    #     if response['event'] == ['on_chat_model_stream']:
    #         print(response)
    #     else:
    #         continue
async def test6():
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GOOGLE_API_KEY"))
    query = [HumanMessage(content="what is the most beautiful snake?")]
    async for response in llm.astream(query):
        print(response.content)

async def test7():
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GOOGLE_API_KEY"))
    query = [HumanMessage(content="Tell me about life")]
    async for response in llm.astream(query):
        print(response.content, end='', flush=True)

if __name__ == "__main__":
    asyncio.run(test7())
