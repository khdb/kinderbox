import logging
import os
from time import gmtime, strftime

class Logger:


    def __init__(self, name = "kinderbox"):

        #create logger with 'spam_application'
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        current_date = (strftime("%Y-%m-%d"), gmtime())
        filename = "tracking-%s.log" %current_date[0]
        fh = logging.FileHandler(os.path.join("/var/log/kinderbox/api/", filename))
        fh.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add the handlers to the logger
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        cmd = "sudo chown pi:pi %s" %fh
        os.system(cmd)

    def debug(self, message):
        self.logger.debug(message)

    def error(self, message):
        self.logger.error(message)

    def info(self, message):
        self.logger.info(message)

    def warn(self, message):
        self.logger.warn(message)

    def exception(self, message):
        self.logger.exception(message)
