from depends.consume import consume
from depends.consumer import RabbitMQClient, consumer
import asyncio
from depends.consumer import RabbitMQClient
import asyncio
import os

async def test1():
    async for value in consume():
        print(value)


async def test2():
    client = RabbitMQClient(amqp_url=os.getenv("AMQP_URL", "amqp://admin:admin@localhost:5672/"))
    await client.start_consume(queue_name=os.getenv("QUEUE_NAME"))

    async for value in client.on_message:
        print(f"Consumed message: {value}")

        # Check for the stop signal
        if value == os.getenv("STOP_SIGNAL"):
            break

    await client.close()

async def test3():
    await consumer.start_consume(queue_name=os.getenv("QUEUE_NAME"))

    try:
        await consumer.consume_task
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await consumer.close()


if __name__=="__main__":
    asyncio.run(test3())