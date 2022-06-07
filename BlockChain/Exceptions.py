class ChainException(Exception):
    pass


class Error(ChainException):
    def __init__(self, msg: str = None, **kwargs):
        self.msg = msg
        self.kwargs = kwargs

    def __str__(self):
        return f"Message: {self.msg}, Arguments: {self.kwargs}"


class TransactionValidationError(Error):
    pass


class BlockValidationError(Error):
    pass


class BlockProcessingError(Error):
    pass


class AccountModelError(Error):
    pass

class APIError(Error):
    pass