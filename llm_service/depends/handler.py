
# save the below code in a file by name handler.py  
# Importing the necessary packages  
from langchain.callbacks.base import BaseCallbackHandler  
from langchain.schema.messages import BaseMessage  
from langchain.schema import LLMResult  
from typing import Dict, List, Any  
from depends.producer import RabbitMQProducer
from dotenv import load_dotenv, find_dotenv
import os


load_dotenv(find_dotenv())
  
# Creating the custom callback handler class  
class MyCustomHandler(BaseCallbackHandler):  
    def __init__(self, queue: RabbitMQProducer) -> None:  
        super().__init__()  
        # we will be providing the streamer queue as an input  
        self._queue = queue  
        # defining the stop signal that needs to be added to the queue in  
        # case of the last token  
        self._stop_signal = os.getenv("STOP_SIGNAL")  
        print("Custom handler Initialized")  
      
    # On the arrival of the new token, we are adding the new token in the   
    # queue  
    async def on_llm_new_token(self, token: str, **kwargs) -> None:  
        if token:
            await self._queue.publish(queue_name=os.getenv("QUEUE_NAME"), message_content=token) 
        
  
    # on the start or initialization, we just print or log a starting message  
    async def on_llm_start( self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any ) -> None:  
        """Run when LLM starts running."""  
        print("generation started")  
  
    # On receiving the last token, we add the stop signal, which determines  
    # the end of the generation  
    async def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:  
        """Run when LLM ends running."""  
        print("\n\ngeneration concluded")  
        await self._queue.publish(queue_name=os.getenv("QUEUE_NAME"), message_content=self._stop_signal)  
