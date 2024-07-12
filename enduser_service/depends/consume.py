from depends.consumer import consumer, RabbitMQClient
import asyncio

from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

async def consume():
    await consumer.start_consume(queue_name=os.getenv("QUEUE_NAME"))

    try:
        await consumer.consume_task
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await consumer.close()

async def message_stream():
    await consumer.start_consume(queue_name=os.getenv("QUEUE_NAME"))

    async for value in consumer._consume(timeout=5):
        yield value

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(consume())