from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import BaseMessage, HumanMessage, LLMResult
from dotenv import load_dotenv, find_dotenv
import os
import getpass

load_dotenv(find_dotenv())
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GOOGLE_API_KEY"))
response = llm.generate([[HumanMessage(content="write a romantic poem about a man")]],stream=True)
print(response.generations[0][0].text)
