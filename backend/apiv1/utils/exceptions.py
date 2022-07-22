import logging

logger = logging.getLogger(__name__)


class RequestDataException(Exception):

    def __init__(self, errors, request_data):
        super().__init__("{}, request_data: {}".format(errors,request_data))

class ModelVerifyException(Exception):

    def __init__(self, messages, model_data):
        super().__init__("{}, model_data: {}".format(messages,model_data))