#Importing all the required packages  
from fastapi import FastAPI  
import asyncio  
from fastapi.responses import StreamingResponse  
from depends.producer import RabbitMQProducer
  
from depends.handler import MyCustomHandler  
  
from dotenv import load_dotenv, find_dotenv
from threading import Thread
import os
  
#Separate package for Google GenAI  
from langchain_google_genai import ChatGoogleGenerativeAI
  
#Importing Message templates  
from langchain.schema.messages import HumanMessage, AIMessage 
  
# loading the GOOGLE_API_KEY  
load_dotenv(find_dotenv())  
  
# Creating a Streamer queue  
streamer_queue = RabbitMQProducer()
  
# Creating an object of custom handler  
my_handler = MyCustomHandler(streamer_queue)  
  
# Creating the llm object and providing the reference of the callback 
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GOOGLE_API_KEY"), callbacks=[my_handler], streaming=True)
llm_simple = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GOOGLE_API_KEY"))
llm_stream = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GOOGLE_API_KEY"), streaming = True)

async def generate_llm(query):
    message: AIMessage = llm_simple.invoke([HumanMessage(content=query)])
    return message.content

async def generate_llm_stream(query):
    messages = llm_stream.invoke([HumanMessage(content=query)]) 
    yield f"data: {messages.content}\n\n"
    
def generate(query):  
    print("generation thread started")
    llm.invoke([HumanMessage(content=query)]) 
    print("generation thread ended") 
  
  
def start_generation(query):  
    # Creating a thread with generate function as a target  
    thread = Thread(target=generate, kwargs={"query": query})  
    # Starting the thread  
    thread.start()

async def response_generator(query):  
    print("response thread started")
    # Start the generation process  
    start_generation(query)  
    print("response thread ended")
  
    # # Starting an infinite loop  
    # while True:  
    #     # Obtain the value from the streamer queue  
    #     value = streamer_queue.get()  
    #     # Check for the stop signal, which is None in our case  
    #     if value == None:  
    #         # If stop signal is found break the loop  
    #         break  
    #     # Else yield the value  
    #     yield value  
    #     # statement to signal the queue that task is done  
    #     streamer_queue.task_done()  
  
    #     # guard to make sure we are not extracting anything from   
    #     # empty queue  
    #     await asyncio.sleep(0.1)
