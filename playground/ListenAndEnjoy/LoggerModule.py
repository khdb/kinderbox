import logging

class Logger:

    def __init__(self):
        self.logger = logging.getLogger('kinderbox')
        hdlr = logging.FileHandler('/var/log/kinderbox/kinderbox.log')
        formatter = logging.Formatter ('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.WARNING)

    def debug(self, message):
        self.logger.debug(message)

    def error(self, message):
        self.logger.error(message)

    def exception(self, message):
        self.logger.exception(message)
