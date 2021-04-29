from loguru import logger

logger.add("app.log", retention="10 days")

