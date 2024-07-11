#Importing all the required packages  
from fastapi import FastAPI  
import asyncio  
from fastapi.responses import StreamingResponse  
from depends.producer import RabbitMQProducer
  
from depends.handler import MyCustomHandler  
  
from dotenv import load_dotenv, find_dotenv
from queue import Queue  
import os
  
#Separate package for Google GenAI  
from langchain_google_genai import ChatGoogleGenerativeAI
  
#Importing Message templates  
from langchain.schema.messages import HumanMessage  
  
# loading the GOOGLE_API_KEY  
load_dotenv(find_dotenv())  
  
# Creating a Streamer queue  
streamer_queue = RabbitMQProducer()
  
# Creating an object of custom handler  
my_handler = MyCustomHandler(streamer_queue)  
  
# Creating the llm object and providing the reference of the callback 
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GOOGLE_API_KEY"), callbacks=[my_handler], streaming=True)
