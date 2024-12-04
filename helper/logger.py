import logging


class Logger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(thread)d [%(name)s] %(message)s',
                                           datefmt='%Y-%m-%d %H:%M:%S')
        self.handler = logging.StreamHandler()
        self.handler.setFormatter(self.formatter)
        if not self.logger.handlers:
            self.logger.addHandler(self.handler)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        self.logger.exception(msg, *args, **kwargs)
