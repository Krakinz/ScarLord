from SƈαɾLσɾԃ import LOAD, LOGGER

def __list_all_modules():
    import glob
    from os.path import basename, dirname, isfile
    mod_paths = glob.glob(dirname(__file__) + "/*.py")
    all_modules = [
    basename(f)[:-3]
    for f in mod_paths
    if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")]
    if LOAD:
        to_load = LOAD
        if to_load:
            if not all(
            any(mod == module_name for module_name in all_modules)
            for mod in to_load):
                LOGGER.error("Invalid loadorder names. Quitting.")
                quit(1)
            all_modules = sorted(set(all_modules) - set(to_load))
            to_load = list(all_modules) + to_load
        else:
            to_load = all_modules
        return to_load
    return all_modules


ALL_MODULES = __list_all_modules()
LOGGER.info("🔥==================================================🔥")
__all__ = ALL_MODULES + ["ALL_MODULES"]