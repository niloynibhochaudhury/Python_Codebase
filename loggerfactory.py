# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.3
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

import logging
import sys


# ### Generic Logger Factory
# https://medium.com/geekculture/create-a-reusable-logger-factory-for-python-projects-419ad408665d

class LoggerFactory(object):

    _LOG = None

    @staticmethod
    def __create_logger(log_file,  log_level):
        """
        A private method that interacts with the python
        logging module
        """
        # set the logging format
        log_format = "%(asctime)s:%(levelname)s:%(message)s"
        
        # Initialize the class variable with logger object
        LoggerFactory._LOG = logging.getLogger(log_file)
        logging.basicConfig(level=logging.INFO, format=log_format, datefmt="%Y-%m-%d %H:%M:%S")
        
        # set the logging level based on the user selection
        if log_level == "INFO":
            LoggerFactory._LOG.setLevel(logging.INFO)
        elif log_level == "ERROR":
            LoggerFactory._LOG.setLevel(logging.ERROR)
        elif log_level == "DEBUG":
            LoggerFactory._LOG.setLevel(logging.DEBUG)
        return LoggerFactory._LOG

    @staticmethod
    def get_logger(log_file, log_level):
        """
        A static method called by other modules to initialize logger in
        their own module
        """
        logger = LoggerFactory.__create_logger(log_file, log_level)
        
        # return the logger object
        return logger



from loggerfactory import LoggerFactory

from IPython.core.display import HTML
HTML('<a href="http://example.com">link</a>')

from IPython.core.display import Markdown
Markdown('#### This will be an H4 title')

# ### Logging in NB
# https://towardsdatascience.com/how-to-setup-logging-for-your-python-notebooks-in-under-2-minutes-2a7ac88d723d



# +
import logging
import logging.config

logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "default": {
            "format": "{levelname} {asctime} | {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": sys.stdout,
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console"],
    },
})
# -

# ### Rich logging output in Jupyter IPython Notebook
# https://stackoverflow.com/questions/68807282/rich-logging-output-in-jupyter-ipython-notebook

# +
from IPython.display import display, HTML

class DisplayHandler(logging.Handler):
    def emit(self, record):
        message = self.format(record)
        # display(message)



# -

class HTMLFormatter(logging.Formatter):
    level_colors = {
        logging.DEBUG: 'lightblue',
        logging.INFO: 'dodgerblue',
        logging.WARNING: 'goldenrod',
        logging.ERROR: 'crimson',
        logging.CRITICAL: 'firebrick'
    }
    
    def __init__(self):
        super().__init__(
            '<span style="font-weight: bold; color: green">{asctime}</span> '
            '[<span style="font-weight: bold; color: {levelcolor}">{levelname}</span>] '
            '{message}',
            style='{'
        )
    
    def format(self, record):
        record.levelcolor = self.level_colors.get(record.levelno, 'black')
        return HTML(super().format(record))



log = logging.getLogger()
handler = DisplayHandler()
handler.setFormatter(HTMLFormatter())
log.addHandler(handler)
log.setLevel(logging.DEBUG)

logging.debug("DE-BUGGING")

logging.warning("WARNING")

logging.error("ERROR")


