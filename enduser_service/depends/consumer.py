import asyncio
from typing import AsyncGenerator
from aio_pika import connect, IncomingMessage, Connection, Channel, Queue
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class RabbitMQClient:
    def __init__(self, amqp_url: str):
        self.amqp_url = amqp_url
        self.connection: Connection = None
        self.channel: Channel = None
        self.queue: Queue = None
        self.consume_task: asyncio.Task = None

    async def connect(self):
        if not self.connection:
            self.connection = await connect(self.amqp_url)
            self.channel = await self.connection.channel()  # Create a new channel

    async def start_consume(self, queue_name: str):
        await self.connect()
        self.queue = await self.channel.declare_queue(queue_name)  # Declare the queue

        # Start consuming messages
        self.consume_task = asyncio.create_task(self._consume())

    async def _consume(self):
        try:
            async for message in self.queue:
                async with message.process():
                    decoded = message.body.decode()
                    print(f"{decoded}")

                    if decoded == os.getenv("STOP_SIGNAL"):
                        print("STOP_SIGNAL received, closing connection.")
                        await self.close()
                        break
        except Exception as e:
            print(f"An error occurred: {e}")

    async def close(self):
        if self.consume_task:
            self.consume_task.cancel()
            try:
                await self.consume_task
            except asyncio.CancelledError:
                pass
            except Exception as unexpected_exception:
                print("Unexpected exception has occurred")
                raise {
                    "exception": str(unexpected_exception)
                }
        if self.connection:
            await self.connection.close()
            self.connection = None
            self.channel = None
            self.queue = None

consumer = RabbitMQClient(amqp_url="amqp://admin:admin@localhost:5672/")
