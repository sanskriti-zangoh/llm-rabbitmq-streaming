"""
Consumer for RabbitMQ.
"""

import asyncio
from typing import Optional, AsyncGenerator

from aio_pika import connect, IncomingMessage, Connection
from depends.file import write_to_file

class RabbitMQClient:
    def __init__(self, amqp_url: str):
        self.amqp_url = amqp_url
        self.connection: Connection = None
        self.consume_task: asyncio.Task = None

    async def connect(self):
        if not self.connection:
            self.connection = await connect(self.amqp_url)

    async def on_message(self, message: IncomingMessage) -> AsyncGenerator[str, None]:
        async with message.process():
            decoded = message.body.decode()
            if not decoded:
                await self.close()
            yield message.body.decode()
            # await write_to_file(message)

    async def consume(self, queue_name: str):
        await self.connect()
        channel = await self.connection.channel()
        queue = await channel.declare_queue(queue_name)
        await queue.consume(self.on_message, no_ack=False)        

    async def start_consume(self, queue_name: str):
        self.consume_task = asyncio.create_task(self.consume(queue_name))

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

consumer = RabbitMQClient(amqp_url="amqp://admin:admin@rabbitmq:5672/")