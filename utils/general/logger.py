import logging
from datetime import datetime


class Logger:
    print_in_console = True

    @classmethod
    def __log(cls, lvl, message, title):
        if cls.print_in_console:
            print(f'-------> {lvl}', datetime.now().strftime('%Y-%m-%d %H:%M:%S+'), title, message, flush=True)

    @classmethod
    def info(cls, logger=None, message=None, title='', additional_data=None):
        cls.get_logger(logger).debug(message, extra={
            "title": title, "additional_data": str(additional_data)})
        cls.__log('INFO', message, title)

    @classmethod
    def debug(cls, logger=None, message=None, title='', additional_data=None):
        cls.get_logger(logger).debug(message, extra={
            "title": title, "additional_data": str(additional_data)})
        cls.__log('DEBUG', message, title)

    @classmethod
    def error(cls, logger=None, message=None, title='', additional_data=None):
        cls.get_logger(logger).error(message, extra={
            "title": title, "additional_data": str(additional_data)})
        cls.__log('ERROR', message, title)

    @classmethod
    def get_logger(cls, logger) -> logging.Logger:
        if not logger:
            return logging.getLogger()
        return logger
