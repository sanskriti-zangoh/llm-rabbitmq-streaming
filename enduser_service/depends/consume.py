from depends.consumer import consumer, RabbitMQClient
import asyncio

from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

async def consume():
# Starting an infinite loop  
    while True:  
        # Obtain the value from the streamer queue  
        value = await consumer.consume(queue_name=os.getenv("QUEUE_NAME"))  
        # Check for the stop signal, which is None in our case  
        if value == None or value == os.getenv("STOP_SIGNAL"):
            break 
        # Else yield the value  
        yield value  
        print(value, end='', flush=True)
  
        # guard to make sure we are not extracting anything from   
        # empty queue  
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(consume())