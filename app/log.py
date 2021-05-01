from loguru import logger

logger.add("app/mx2rss.log", retention="10 days")

