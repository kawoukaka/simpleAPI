from flask import Flask, request
from flask_cors import CORS
from flask_restplus import Api, Resource

from api_server.app_logging import AppLogging
from api_server.flask_models import (
    create_organization_model,
    create_user_model,
    add_user_to_organization_model,
    delete_user_from_organization_model,
    get_all_organization_from_user_model,
    get_all_user_model,
)
from api_server.error_handler import (
    OrganizationAlreadyExistsError,
    UserAlreadyExistsError,
    OrganizationDoesNotExist,
    UserDoesNotExist,
    DatabaseSchemaError
)
from api_server.example_db import (
    user_tb,
    organization_tb,
    user_org_tb
)

import logging

# Flask Initialization
# =========================================================================
app = Flask(__name__)
app.config.from_object('api_server.config')

# Logging Initialization
# =========================================================================
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)

AppLogging().set_logging(app)

# Security Initialization
# =========================================================================
app.secret_key = app.config['SECRET_KEY']
CORS(app, resources={
    r"/*": {
        "origins": app.config.get('CORS_ORIGINS', '*')
    }
})

# Swagger API Initialization
# =========================================================================
api = Api(app,
          prefix='',
          version='1.0',
          title='simple API',
          description='''The simple api provides create/view/edit
          on the users in an organization''',
          catch_all_404s=True)


simple_ns = api.namespace('v1', description='Simple API Endpoints')

# Payload model
# =========================================================================
create_organization_payload = simple_ns.model('Simple API - Create Organization', create_organization_model)
create_user_payload = simple_ns.model('Simple API - Create User', create_user_model)
add_user_to_organization_payload = simple_ns.model('Simple API - Add User To Organization',
                                                   add_user_to_organization_model)
delete_user_from_organization_payload = simple_ns.model('Simple API - Delete User From Organization',
                                                        delete_user_from_organization_model)
get_all_user_payload = simple_ns.model('Simple API - Get All Users From An Organization', get_all_user_model)
get_all_organization_from_user_payload = simple_ns.model('Simple API - Get All Organizations From An User Profile',
                                                         get_all_organization_from_user_model)


responses = {
    200: 'Success',
    400: 'Wrong Payload',
    401: 'Unauthorized',
    402: 'Server error in process',
    404: 'Resource not found',
    500: 'Internal Server Error',
    503: 'Service Unavailable'
}


# Endpoints
# =========================================================================
@simple_ns.route('/create_organization')
class CreateOrganization(Resource):

    @simple_ns.expect(create_organization_payload, validate=True)
    @simple_ns.doc(response=responses)
    def post(self):
        """
        Create Organization API

        Create a single Organization in database
        """
        args = request.get_json()
        org_name = args.get('org_name')
        org_address = args.get('org_address')
        org_phone = args.get('org_phone')
        try:
            if 'organizations' in organization_tb:
                for org in organization_tb['organizations']:
                    if org['org_name'] == org_name:
                        raise OrganizationAlreadyExistsError('Organization name existed!', 402, args)
                else:
                    organization_tb['organizations'].append({
                        'org_name': org_name,
                        'org_address': org_address,
                        'org_phone': org_phone,
                    })
            else:
                raise DatabaseSchemaError('Database Schema Error!', 404, args)
            if 'organizations' in user_org_tb:
                user_org_tb['organizations'].append({
                    'org_name': org_name,
                    'users': []
                })
            else:
                raise DatabaseSchemaError('Database Schema Error!', 404, args)
        except OrganizationAlreadyExistsError as e:
            return {'message': e.message, 'payload': args}, e.status
        except Exception:
            logger.exception('Unexpected Error!')
            return {'message': 'Unexpected Error!', 'payload': args}, 500
        return {'message': 'Created Organization!', 'payload': args}, 200


@simple_ns.route('/create_user')
class CreateUser(Resource):

    @simple_ns.expect(create_user_payload, validate=True)
    @simple_ns.doc(response=responses)
    def post(self):
        """
        Create User API

        Create a single User in database
        """
        args = request.get_json()
        user_first_name = args.get('user_first_name')
        user_last_name = args.get('user_last_name')
        user_email = args.get('user_email')
        user_address = args.get('user_address')
        user_phone = args.get('user_phone')
        try:
            if 'users' in user_tb:
                for user in user_tb['users']:
                    if user['user_email'] == user_email:
                        raise UserAlreadyExistsError('User name existed!', 402, args)
                else:
                    user_tb['users'].append({
                        'user_email': user_email,
                        'user_first_name': user_first_name,
                        'user_last_name': user_last_name,
                        'user_address': user_address,
                        'user_phone': user_phone
                    })
            else:
                raise DatabaseSchemaError('Database Schema Error!', 404, args)
            if 'users' in user_org_tb:
                user_org_tb['users'].append({
                    'user_email': user_email,
                    'organizations': []
                })
            else:
                raise DatabaseSchemaError('Database Schema Error!', 404, args)
        except UserAlreadyExistsError as e:
            return {'message': e.message, 'payload': args}, e.status
        except Exception:
            logger.exception('Unexpected Error!')
            return {'message': 'Unexpected Error!', 'payload': args}, 500
        return {'message': 'Created User!', 'payload': args}, 200


@simple_ns.route('/add_user_to_organization')
class AddUserToOrganization(Resource):

    @simple_ns.expect(add_user_to_organization_payload, validate=True)
    @simple_ns.doc(response=responses)
    def post(self):
        """
        Add User To Organization API

        Add a single User to Organization in database
        """
        args = request.get_json()
        org_name = args.get('org_name')
        user_email = args.get('user_email')
        try:
            if len(user_tb['users']) == 0:
                raise UserDoesNotExist('User does not exist!', 402, args)
            for user in user_tb['users']:
                if user['user_email'] != user_email or len(user_tb['users']) == 0:
                    raise UserDoesNotExist('User does not exist!', 402, args)
            if len(organization_tb['organizations']) == 0:
                raise OrganizationDoesNotExist('Organization does not exist!', 402, args)
            for org in organization_tb['organizations']:
                if org['org_name'] != org_name:
                    raise OrganizationDoesNotExist('Organization does not exist!', 402, args)
            if 'organizations' in user_org_tb:
                for org in user_org_tb['organizations']:
                    if org['org_name'] == org_name:
                        if user_email in org['users']:
                            raise UserAlreadyExistsError('User existed in the organization!', 402, args)
                        org['users'].append(user_email)
                        break
                else:
                    raise OrganizationDoesNotExist('Organization does not exist!', 402, args)
            else:
                raise DatabaseSchemaError('Database Schema Error!', 404, args)
            if 'users' in user_org_tb:
                for user in user_org_tb['users']:
                    if user['user_email'] == user_email:
                        if org_name in user['organizations']:
                            raise OrganizationAlreadyExistsError('Organization that belongs to user existed!', 402, args)
                        user['organizations'].append(org_name)
                        break
                else:
                    raise UserDoesNotExist('User does not exist!', 402, args)
            else:
                raise DatabaseSchemaError('Database Schema Error!', 404, args)

        except (
                UserDoesNotExist,
                OrganizationDoesNotExist,
                OrganizationAlreadyExistsError,
                UserAlreadyExistsError,
                DatabaseSchemaError) as e:
            return {'message': e.message, 'payload': args}, e.status
        except Exception:
            logger.exception('Unexpected Error!')
            return {'message': 'Unexpected Error!', 'payload': args}, 500
        return {'message': 'Added User in Organization!', 'payload': args}, 200


@simple_ns.route('/delete_user_from_organization')
class DeleteUserFromOrganization(Resource):

    @simple_ns.expect(delete_user_from_organization_payload, validate=True)
    @simple_ns.doc(response=responses)
    def post(self):
        """
        Delete User From Organization API

        Delete a single User to Organization in database
        """
        args = request.get_json()
        org_name = args.get('org_name')
        user_email = args.get('user_email')
        try:
            if len(user_tb['users']) == 0:
                raise UserDoesNotExist('User does not exist!', 402, args)
            for user in user_tb['users']:
                if user['user_email'] != user_email or len(user_tb['users']) == 0:
                    raise UserDoesNotExist('User does not exist!', 402, args)
            if len(organization_tb['organizations']) == 0:
                raise OrganizationDoesNotExist('Organization does not exist!', 402, args)
            for org in organization_tb['organizations']:
                if org['org_name'] != org_name or len(organization_tb['organizations']) == 0:
                    raise OrganizationDoesNotExist('Organization does not exist!', 402, args)
            if 'organizations' in user_org_tb:
                for org in user_org_tb['organizations']:
                    if org['org_name'] == org_name and user_email in org['users']:
                        org['users'].remove(user_email)
                        break
                else:
                    raise OrganizationDoesNotExist('Organization does not exist!', 402, args)
            else:
                raise DatabaseSchemaError('Database Schema Error!', 404, args)
            if 'users' in user_org_tb:
                for user in user_org_tb['users']:
                    if user['user_email'] == user_email and org_name in user['organizations']:
                        user['organizations'].remove(org_name)
                        break
                else:
                    raise UserDoesNotExist('Organization does not belong to user!', 402, args)
            else:
                raise DatabaseSchemaError('Database Schema Error!', 404, args)
        except (UserDoesNotExist, OrganizationDoesNotExist, DatabaseSchemaError) as e:
            return {'message': e.message, 'payload': args}, e.status
        except Exception:
            logger.exception('Unexpected Error!')
            return {'message': 'Unexpected Error!', 'payload': args}, 500
        return {'message': 'Deleted User from organization!', 'payload': args}, 200


@simple_ns.route('/get_users_from_organization')
class GetUsersFromOrganization(Resource):

    @simple_ns.expect(get_all_user_payload, validate=True)
    @simple_ns.doc(response=responses)
    def post(self):
        """
        Get Users From Organization API

        Get Users From Organization in database
        """
        args = request.get_json()
        org_name = args.get('org_name')
        try:
            if len(organization_tb['organizations']) == 0:
                raise OrganizationDoesNotExist('Organization does not exist!', 402, args)
            for org in organization_tb['organizations']:
                if org['org_name'] != org_name:
                    raise OrganizationDoesNotExist('Organization does not exist!', 402, args)
            if 'organizations' in user_org_tb:
                for org in user_org_tb['organizations']:
                    if org['org_name'] == org_name:
                        return {'results': org['users'], 'payload': args}, 200
                else:
                    raise OrganizationDoesNotExist('Organization does not exist!', 402, args)
            else:
                raise DatabaseSchemaError('Database Schema Error!', 404, args)
        except (OrganizationDoesNotExist, DatabaseSchemaError) as e:
            return {'message': e.message, 'payload': args}, e.status
        except Exception:
            logger.exception('Unexpected Error!')
            return {'message': 'Unexpected Error!', 'payload': args}, 500


@simple_ns.route('/get_organizations_belong_to_user')
class GetOrganizationsBelongToUser(Resource):

    @simple_ns.expect(get_all_organization_from_user_payload, validate=True)
    @simple_ns.doc(response=responses)
    def post(self):
        """
        Get Organizations Belong To User API

        Get Organizations Belong To User in database
        """
        args = request.get_json()
        user_email = args.get('user_email')
        try:
            if len(user_tb['users']) == 0:
                raise UserDoesNotExist('User does not exist!', 402, args)
            for user in user_tb['users']:
                if user['user_email'] != user_email:
                    raise UserDoesNotExist('User does not exist!', 402, args)
            if 'users' in user_org_tb:
                for user in user_org_tb['users']:
                    if user['user_email'] == user_email:
                        return {'results': user['organizations'], 'payload': args}, 200
                else:
                    raise UserDoesNotExist('User does not exist!', 402, args)
            else:
                raise DatabaseSchemaError('Database Schema Error!', 404, args)
        except (UserDoesNotExist, DatabaseSchemaError) as e:
            return {'message': e.message, 'payload': args}, e.status
        except Exception:
            logger.exception('Unexpected Error!')
            return {'message': 'Unexpected Error!', 'payload': args}, 500


if __name__ == '__main__':
    app.run()
