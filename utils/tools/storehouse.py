import yaml
import json
import logging
from pydantic import BaseModel
from logging.config import dictConfig


class Item_Login(BaseModel):
    account: str
    password: str
    token: str


class Storehouse():
    def __init__(self):
        with open('./utils/config/config.yaml', 'r') as file:
            self.config = yaml.safe_load(file)
        with open('./utils/config/label_format_schema.json', 'r') as file:
            self.label_format_schema = json.load(file)
            
        self.version = self.config['version']
        
        logging_dictConfig = {
            "version": 1,
            "disable_existing_loggers": False,  
            "formatters": {             
                "default": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",  
                    "level": "DEBUG",
                    "formatter": "default",
                },
                "log_file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": "INFO",
                    "formatter": "default",          
                    "filename": self.config['path_home']['log_path'],       # "./logs/backend.log"  
                    "maxBytes": 20*1024*1024,        
                    "backupCount": 10,               
                    "encoding": "utf8",              
                },
            },
            "root": {
                "level": "DEBUG",                    
                "handlers": ["console", "log_file"],
            },
        }
        self.logger = logging.getLogger(__name__)
        dictConfig(logging_dictConfig) 
        self.logger.info(f"Init the logger")
        


