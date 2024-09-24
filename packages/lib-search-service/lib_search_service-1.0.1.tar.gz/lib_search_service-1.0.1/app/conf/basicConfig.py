import logging
import os
import socket

from dotenv import load_dotenv

from app.searchManager import SearchManager

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
load_dotenv()
SERVICE_URI = os.getenv("SERVICE_URI")
if SERVICE_URI is None:
    logger.warning(
        "Update SERVICE_URI to your cluster uri. Current value for SERVICE_URI={"
        "SERVICE_URI}")
    logger.info(
        "As a workaround, Going to put your hostname as SERVICE_URI")

    SERVICE_URI = socket.gethostbyname(socket.gethostname())

logger.info("SERVICE_URI={}".format(SERVICE_URI))


SERVICE_PORT = int(os.getenv("SERVICE_PORT"))
if SERVICE_PORT is None:
    logger.warning(
        "Update SERVICE_PORT to your cluster uri. Current value for SERVICE_PORT={"
        "SERVICE_PORT}")
    logger.info(
        "As a workaround, Going to put 9000 as SERVICE_PORT")

    SERVICE_PORT = 9000

logger.info("SERVICE_PORT={}".format(SERVICE_PORT))

search_manager = SearchManager()
