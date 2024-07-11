import aiofiles
from aio_pika import IncomingMessage

async def write_to_file( message: IncomingMessage, file_path: str = 'data/messages.txt'):
    async with aiofiles.open(file_path, mode='a') as file:
                # Write the message to the file
                await file.write(f'{message.body.decode()}\n')
                # Flush the file to ensure it is written immediately
                await file.flush()