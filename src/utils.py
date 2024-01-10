IS_BUSY = False


def execute_if_not_busy(func):
    async def wrapper(*args, **kwargs):
        global IS_BUSY
        if not IS_BUSY:

            IS_BUSY = True
            result = await func(*args, **kwargs)
            IS_BUSY = False

            return result
    return wrapper
