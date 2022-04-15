from sideloader import *
from SƈαɾLσɾԃ import LOGGER, updater
from SKARS import ALL_MODULES

for module_name in ALL_MODULES:
    SƈαɾLσɾԃS = importlib.import_module("SKARS."+module_name)
    if not lib(SƈαɾLσɾԃS, "__mod_name__"):
        SƈαɾLσɾԃS.__mod_name__ = SƈαɾLσɾԃS.__name__
    if SƈαɾLσɾԃS.__mod_name__.lower() not in IMPORTED:
        IMPORTED[SƈαɾLσɾԃS.__mod_name__.lower()] = SƈαɾLσɾԃS
    if lib(SƈαɾLσɾԃS, "__help__") and SƈαɾLσɾԃS.__help__:
        HELPABLE[SƈαɾLσɾԃS.__mod_name__.lower()] = SƈαɾLσɾԃS
    if lib(SƈαɾLσɾԃS, "__migrate__"):
        MIGRATEABLE.append(SƈαɾLσɾԃS)
    if lib(SƈαɾLσɾԃS, "__stats__"):
        STATS.append(SƈαɾLσɾԃS)
    if lib(SƈαɾLσɾԃS, "__gdpr__"):
        GDPR.append(SƈαɾLσɾԃS)
    if lib(SƈαɾLσɾԃS, "__user_info__"):
        USER_INFO.append(SƈαɾLσɾԃS)
    if lib(SƈαɾLσɾԃS, "__import_data__"):
        DATA_IMPORT.append(SƈαɾLσɾԃS)
    if lib(SƈαɾLσɾԃS, "__export_data__"):
        DATA_EXPORT.append(SƈαɾLσɾԃS)
    if lib(SƈαɾLσɾԃS, "__chat_settings__"):
        CHAT_SETTINGS[SƈαɾLσɾԃS.__mod_name__.lower()] = SƈαɾLσɾԃS
    if lib(SƈαɾLσɾԃS, "__user_settings__"):
        USER_SETTINGS[SƈαɾLσɾԃS.__mod_name__.lower()] = SƈαɾLσɾԃS


LOGGER.info("—✨••÷[  SƈαɾLσɾԃ⚔️  ]÷••✨—")
LOGGER.info("")
LOGGER.info("🔥==================================================🔥")
LOGGER.info("⚔️ Hell Yea.. ӄʟǟա ʀօɮօȶ IS FUCKING READY.⚔️")
updater.start_polling(timeout=15, read_latency=4, drop_pending_updates=True)   
LOGGER.info("Successfully loaded modules: \n" + str(ALL_MODULES))
LOGGER.info("")
LOGGER.info("🔥==================================================🔥")
LOGGER.info("—✨••÷[  SƈαɾLσɾԃ⚔️  ]÷••✨—")
updater.idle()
updater.stop()
LOGGER.info("🔥==================================================🔥")
LOGGER.info("—✨••÷[  SƈαɾLσɾԃ⚔️  ]÷••✨—")