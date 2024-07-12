#Importing all the required packages  
from fastapi import FastAPI  
import asyncio  
from fastapi.responses import StreamingResponse  
from depends.producer import RabbitMQProducer
  
from depends.handler import MyCustomHandler  

import google.generativeai as genai
  
from dotenv import load_dotenv, find_dotenv
from threading import Thread
import os
  
#Separate package for Google GenAI  
from langchain_google_genai import ChatGoogleGenerativeAI
  
#Importing Message templates  
from langchain.schema.messages import HumanMessage, AIMessage 
  
# loading the GOOGLE_API_KEY  
load_dotenv(find_dotenv())  
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
  
# Creating a Streamer queue  
streamer_queue = RabbitMQProducer()
  
# Creating an object of custom handler  
my_handler = MyCustomHandler(streamer_queue)  
  
# Creating the llm object and providing the reference of the callback 
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GOOGLE_API_KEY"), callbacks=[my_handler], streaming=True)
llm_simple = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GOOGLE_API_KEY"))
llm_stream = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GOOGLE_API_KEY"), streaming = True)

google_llm = genai.GenerativeModel('gemini-1.5-flash')

async def generate_llm(query):
    message: AIMessage = llm_simple.invoke([HumanMessage(content=query)])
    return message.content

async def generate_llm_stream(query):
    message = [HumanMessage(content=query)]
    async for response in llm_simple.astream(message):
        yield response.content
    yield os.getenv("STOP_SIGNAL")

async def generate(query):  
    print("generation started")
    await llm.invoke([HumanMessage(content=query)])
    print("generation ended")

async def response_generator(query):  
    print("response thread started")
    await generate(query)  
    print("response thread ended")

async def stream_response(query: str):
    async for chunk in await google_llm.generate_content_async(query, stream=True):
        if chunk.text:
            yield chunk.text
    yield os.getenv("STOP_SIGNAL")

async def stream_response_queue(query, queue: RabbitMQProducer):  
    message = [HumanMessage(content=query)]
    async for response in llm_simple.astream(message):
        await queue.publish(queue_name=os.getenv("QUEUE_NAME"), message_content=response.content)
    await queue.publish(queue_name=os.getenv("QUEUE_NAME"), message_content=os.getenv("STOP_SIGNAL"))
