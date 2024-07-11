from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from dotenv import load_dotenv, find_dotenv
import os
import getpass

load_dotenv(find_dotenv())
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GOOGLE_API_KEY"))
result = llm.invoke("Write a ballad about LangChain")
print(result.content)
