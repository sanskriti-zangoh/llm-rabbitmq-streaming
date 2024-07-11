from main import app
from contextlib import asynccontextmanager
from fastapi import FastAPI

from depends.llm import generate

from depends.producer import RabbitMQProducer
from depends.handler import MyCustomHandler
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv, find_dotenv
import os