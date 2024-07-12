import asyncio
from typing import AsyncGenerator
from aio_pika import connect, IncomingMessage, Connection, Channel, Queue
from aio_pika.exceptions import ConnectionClosed
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class RabbitMQClient:
    def __init__(self, amqp_url: str):
        self.amqp_url = amqp_url
        self.connection: Connection = None
        self.channel: Channel = None
        self.queue: Queue = None

    async def connect(self):
        if not self.connection:
            self.connection = await connect(self.amqp_url)
            self.channel = await self.connection.channel()  # Create a new channel

    async def start_consume(self, queue_name: str):
        await self.connect()
        self.queue = await self.channel.declare_queue(queue_name)  # Declare the queue

    async def _consume(self, timeout: int = 5) -> AsyncGenerator[str, None]:
        try:
            while True:
                try:
                    message: IncomingMessage = await asyncio.wait_for(self.queue.get(), timeout)
                    async with message.process():
                        decoded = message.body.decode()
                        yield decoded

                        if decoded == os.getenv("STOP_SIGNAL"):
                            yield "STOP_SIGNAL received, closing connection."
                            # await message.ack()
                            # break
                except asyncio.TimeoutError:
                    print("No messages received. Closing connection.")
                    break
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            await self.close()

    async def close(self):
        if self.connection:
            try:
                await self.connection.close()
            except ConnectionClosed:
                pass
            self.connection = None
            self.channel = None
            self.queue = None

consumer = RabbitMQClient(amqp_url="amqp://admin:admin@rabbitmq:5672/")
