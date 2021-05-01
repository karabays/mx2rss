from loguru import logger

logger.add("./data/mx2rss.log", retention="10 days")

