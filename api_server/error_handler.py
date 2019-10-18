from flask import jsonify
from api_server.server import app


class UserAlreadyExistsError(Exception):
    """
    Custom UserAlreadyExistsError class to be thrown when local error occurs.
    """
    def __init__(self, message, status=402, payload=None):
        self.message = message
        self.status = status
        self.payload = payload


@app.errorhandler(UserAlreadyExistsError)
def handle_user_existed_request(error):
    """
    Catch UserAlreadyExistsError exception globally,
    serialize into JSON, and respond with 400.
    """
    payload = dict(error.payload or ())
    payload['message'] = error.message
    payload['status'] = error.status
    return jsonify(payload), 402


class OrganizationAlreadyExistsError(Exception):
    """
    Custom OrganizationAlreadyExistsError class to be thrown when local error occurs.
    """
    def __init__(self, message, status=402, payload=None):
        self.message = message
        self.status = status
        self.payload = payload


@app.errorhandler(OrganizationAlreadyExistsError)
def handle_organization_existed_request(error):
    """
    Catch OrganizationAlreadyExistsError exception globally,
    serialize into JSON, and respond with 400.
    """
    payload = dict(error.payload or ())
    payload['message'] = error.message
    payload['status'] = error.status
    return jsonify(payload), 402


class UserDoesNotExist(Exception):
    """
    Custom UserDoesNotExist class to be thrown when local error occurs.
    """
    def __init__(self, message,  status=402, payload=None):
        self.message = message
        self.status = status
        self.payload = payload


@app.errorhandler(UserDoesNotExist)
def handle_user_not_exist_request(error):
    """
    Catch UserDoesNotExist exception globally,
    serialize into JSON, and respond with 400.
    """
    payload = dict(error.payload or ())
    payload['message'] = error.message
    payload['status'] = error.status
    return jsonify(payload), 402


class OrganizationDoesNotExist(Exception):
    """
    Custom OrganizationDoesNotExist class to be thrown when local error occurs.
    """
    def __init__(self, message, status=402, payload=None):
        self.message = message
        self.status = status
        self.payload = payload


@app.errorhandler(OrganizationDoesNotExist)
def handle_organization_not_exist_request(error):
    """
    Catch OrganizationDoesNotExist exception globally,
    serialize into JSON, and respond with 400.
    """
    payload = dict(error.payload or ())
    payload['message'] = error.message
    return jsonify(payload), 402


class DatabaseSchemaError(Exception):
    """
    Custom DatabaseSchemaError class to be thrown when local error occurs.
    """
    def __init__(self, message, status=400, payload=None):
        self.message = message
        self.status = status
        self.payload = payload


@app.errorhandler(DatabaseSchemaError)
def handle_database_schema_error(error):
    """
    Catch DatabaseSchemaError exception globally,
    serialize into JSON, and respond with 400.
    """
    payload = dict(error.payload or ())
    payload['message'] = error.message
    payload['status'] = error.status
    return jsonify(payload), 404
