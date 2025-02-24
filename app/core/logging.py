"""Общий модуль для подключение логера."""
from icecream import ic
from app.core.config import settings

# class Looger(IceCreamDebugger):
    
#     def logging_mode(self, mode: str):
        
logging_mode = {
    "on": "enable",
    "off": "disable"
}

logger = ic
logger.configureOutput(prefix='logging ', includeContext=True)
getattr(logger, logging_mode[settings.auth.logging_mode])()