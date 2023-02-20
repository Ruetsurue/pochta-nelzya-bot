import asyncio

AWAIT_BEFORE_REPLY_SECONDS = 1.5


def wait_before_reply(seconds=AWAIT_BEFORE_REPLY_SECONDS):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            await asyncio.sleep(seconds)
            return await func(*args, **kwargs)
        return wrapper
    return decorator
