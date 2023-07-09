from fastapi import HTTPException
from loguru import logger


async def fetch_message():
    # Simulate an asynchronous operation
    # await asyncio.sleep(5)
    logger.info("fetch_message!")
    raise HTTPException(status_code=400, detail="Bad Request")
    # raise Exception("Something went wrong!")
    return "Hello, World!"


async def fetch_message500():
    # Simulate an asynchronous operation
    # await asyncio.sleep(5)
    logger.info("fetch_message500!")
    # raise HTTPException(status_code=400, detail="Bad Request")
    raise Exception("Something went wrong!")
    # raise HTTPException(status_code=500, detail="SORRY!")
    # raise UnicornException(name="test!")

    return "Hello, World!"
