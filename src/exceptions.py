class Error(Exception):
    def __init__(self, message: str, *args: object) -> None:
        self.message = message
        super().__init__(message, *args)

class InvalidAuthTokenError(Error):
    pass

class APIServerError(Error):
    pass

class VendorNotFoundError(Error):
    pass

class NotPermittedError(Error):
    pass

class InvalidCreateLogRequest(Error):
    pass

class UrlNotFound(Error):
    pass

class ObjectNotFound(Error):
    pass
