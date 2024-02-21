from config import get_config
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from pathlib import Path


__logger = logging.getLogger('experiment')
__log_init = False
    
    
def get_logger():
    global __log_init
    global __logger
    
    if not __log_init:
        __log_init = True
        
        log_levels = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR
        }
        _ = get_config()
        log_level = logging.DEBUG
        if "log_level" in _:
            if _["log_level"] in log_levels:
                log_level = log_levels[_["log_level"]]            
            __logger = _init_logging(_.get("log_path"), log_level)
        
    return __logger


def _init_logging(log_path:str, log_level):
    formatter = logging.Formatter(
        '%(levelname)1.1s %(asctime)s %(module)15s:%(lineno)03d %(funcName)15s) %(message)s',
        datefmt='%H:%M:%S')
    
    Path(os.path.dirname(log_path)).mkdir(parents=True, exist_ok=True)
    file_handler = TimedRotatingFileHandler(log_path, when="d")
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    
    global __logger
    __logger.addHandler(console_handler)
    __logger.addHandler(file_handler)    
    __logger.setLevel(log_level)

    return __logger

