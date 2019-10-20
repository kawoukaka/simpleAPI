from werkzeug.exceptions import UnprocessableEntity, NotFound


class UserAlreadyExistsError(UnprocessableEntity):
    """
    Custom UserAlreadyExistsError class to be thrown when local error occurs.
    """
    def __init__(self, message, status=402, payload=None):
        self.message = message
        self.status = status
        self.payload = payload


class OrganizationAlreadyExistsError(UnprocessableEntity):
    """
    Custom OrganizationAlreadyExistsError class to be thrown when local error occurs.
    """
    def __init__(self, message, status=402, payload=None):
        self.message = message
        self.status = status
        self.payload = payload


class UserDoesNotExist(UnprocessableEntity):
    """
    Custom UserDoesNotExist class to be thrown when local error occurs.
    """
    def __init__(self, message,  status=402, payload=None):
        self.message = message
        self.status = status
        self.payload = payload


class OrganizationDoesNotExist(UnprocessableEntity):
    """
    Custom OrganizationDoesNotExist class to be thrown when local error occurs.
    """
    def __init__(self, message, status=402, payload=None):
        self.message = message
        self.status = status
        self.payload = payload


class DatabaseSchemaError(NotFound):
    """
    Custom DatabaseSchemaError class to be thrown when local error occurs.
    """
    def __init__(self, message, status=404, payload=None):
        self.message = message
        self.status = status
        self.payload = payload
