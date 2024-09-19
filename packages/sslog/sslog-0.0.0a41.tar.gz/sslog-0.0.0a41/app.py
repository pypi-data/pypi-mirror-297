from sslog import logger, InterceptHandler

import logging


logger.trace("hello")
logger.debug("hello")
logger.info("hello")
logger.warning("hello")
logger.error("hello")
# logger.fatal("hello")

logging.basicConfig(handlers=[InterceptHandler()])

logging.debug("hello")
logging.info("hello")
logging.warning("hello")
logging.error("hello")
logging.critical("hello")
