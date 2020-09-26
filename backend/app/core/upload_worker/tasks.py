import logging
from typing import Any, Dict

logger = logging.getLogger("__name__")
logger.addHandler(logging.NullHandler())


async def hello_world(ctx: Dict[str, Any]) -> str:
    logger.info("Executing job hello_world")
    return "DONE"


async def process_shape(ctx: Dict[str, Any], key: str) -> str:
    """
    Process a shape file where the binary data is at the key "key"

    :param ctx: Worker Context
    :param key: Storage Key
    :return:
    """
    pass
