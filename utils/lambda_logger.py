import json
import logging
import os


class LambdaContextFilter(logging.Filter):

    def __init__(self, context):
        logging.Filter.__init__(self)
        self.context = context

    def filter(self, record):
        """
        Dynamically enrich the logs with information  inherited from the lambda context
        :param record:
        :return:
        """
        record.requestid = self.context.aws_request_id
        record.remainingtime = self.context.get_remaining_time_in_millis() / 1000
        return True


class LambdaLogger(object):
    """
    Class which overrides the default lambda logger
    """
    def __init__(self):
        self.logger = logging.getLogger('root')

    @staticmethod
    def setup(level, context):
        root = logging.getLogger()
        if root.handlers:
            for h in root.handlers:
                root.removeHandler(h)
        log_format = '%(asctime)s -- %(levelname)s -- %(requestid)s' \
                     '-- %(remainingtime)s -- %(message)s'
        logging.basicConfig(format=log_format, datefmt='%Y-%m-%d %H:%M:%S')
        logger = logging.getLogger('root')
        level_name = logging.getLevelName(level)
        f = LambdaContextFilter(context)
        logger.addFilter(f)
        logger.setLevel(level_name)

    def debug(self, message):
        self.logger.debug(json.dumps(message))

    def info(self, message):
        self.logger.info(json.dumps(message))

    def warning(self, message):
        self.logger.warning(json.dumps(message))

    def warn(self, message):
        self.logger.warn(json.dumps(message))

    def error(self, message):
        self.logger.error(json.dumps(message))

    def critical(self, message):
        self.logger.critical(json.dumps(message))

    def exception(self, message):
        self.logger.exception(json.dumps(message))