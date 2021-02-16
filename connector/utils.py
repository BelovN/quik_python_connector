
def singleton(cls):
    instance = [None]

    def wrapper(*args, **kwargs):
        if instance[0] is None:
            instance[0] = cls(*args, **kwargs)
        return instance[0]

    return wrapper


def log_method(logger):
    def decorator(function):
        async def wrapper(*args, **kwargs):
            try:
                result = await function(*args, **kwargs)
                logger.info(f'{function.__name__} args={args} kwargs={kwargs} result={result}')
            except Exception as e:
                logger.error(e, exc_info=True)
                raise e
            return result
        return wrapper
    return decorator


