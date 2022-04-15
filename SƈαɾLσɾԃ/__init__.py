from sideloader import *

class InterceptHandler(logging.Handler):
    LEVELS_MAP = {
        logging.CRITICAL: "CRITICAL",
        logging.ERROR: "ERROR",
        logging.WARNING: "WARNING",
        logging.INFO: "INFO",
        logging.DEBUG: "DEBUG"}
    def _get_level(self, record):
        return self.LEVELS_MAP.get(record.levelno, record.levelno)
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info, ansi=True, lazy=True)
        logger_opt.log(self._get_level(record), record.getMessage())
logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)
LOGGER = logging.getLogger(__name__)

from ꜰᴜɴᴄᴘᴏᴅ.handlers import (CustomCommandHandler,CustomMessageHandler,CustomRegexHandler)
tg.RegexHandler = CustomRegexHandler
tg.CommandHandler = CustomCommandHandler
tg.MessageHandler = CustomMessageHandler