
try:
    from loguru import logger
except Exception as _:
    import logging
    logger = logging.getLogger()
    logger.info(f'loguru can`t be fount, now switch to logging, exception: {_}')
