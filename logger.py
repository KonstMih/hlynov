# -*- coding: utf-8 -*-

import logging
import os

def set_logger():
    """
    Настройка логера
    """
    try:
        os.mkdir(os.getcwd() + '/log')
    finally:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        s_handler = logging.StreamHandler()
        f_handler = logging.FileHandler("./log/log_file.log")
        
        f_handler.setLevel(logging.INFO)
        s_handler.setLevel(logging.INFO)
        
        f_handler.setFormatter(format)
        s_handler.setFormatter(format)
        

        logger.addHandler(f_handler)
        logger.addHandler(s_handler)
        
        return logger
    
if __name__ == "__main__":
    log = set_logger()