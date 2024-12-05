from loguru import logger

# Configuration des logs
logger.add("application.log", rotation="1 MB", retention="7 days", level="INFO")
