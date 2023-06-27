import asyncio
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    message = await fetch_message()  # Perform asynchronous operation
    return {"message": message}


async def fetch_message():
    # Simulate an asynchronous operation
    await asyncio.sleep(5)
    return "Hello, World!"
