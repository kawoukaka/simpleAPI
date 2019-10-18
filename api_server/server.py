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
from api_server.error_handler import *
from api_server.example_db import (
    user_db,
    organization_db,
    user_org_db
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
        try:
            if org_name in organization_db['org_name']:
                raise OrganizationAlreadyExistsError('Organization name existed!', 402, args)
            organization_db['org_name'].append(org_name)
            user_org_db['organizations'].append({
                'org_name': org_name,
                'users': []
            })
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
        user_name = args.get('user_name')
        try:
            if user_name in user_db['user_name']:
                raise UserAlreadyExistsError('User name existed!', 402, args)
            user_db['user_name'].append(user_name)
            user_org_db['users'].append({
                'user_name': user_name,
                'organizations': []
            })
        except UserAlreadyExistsError as e:
            return {'message': e.message, 'payload': args}, e.status
        except Exception:
            return {'message': 'Unexpected Error!', 'payload': args}, 500
        return {'message': 'Created User!', 'payload': args}, 200


@simple_ns.route('/add_user_to_organization')
class AddUserToOrganization(Resource):

    @simple_ns.expect(add_user_to_organization_payload, validate=True)
    @simple_ns.doc(response=responses)
    def post(self):
        """
        AddUserToOrganization API

        Add a single User to Organization in database
        """
        args = request.get_json()
        org_name = args.get('org_name')
        user_name = args.get('user_name')
        try:
            if user_name not in user_db['user_name']:
                raise UserDoesNotExist('User does not exist!', 402, args)
            if org_name not in organization_db['org_name']:
                raise OrganizationDoesNotExist('Organization does not exist!', 402, args)
            if 'organizations' in user_org_db:
                for org in user_org_db['organizations']:
                    if org['org_name'] == org_name:
                        org['users'].append(user_name)
                    else:
                        raise OrganizationDoesNotExist('Organization does not exist!', 402, args)
            else:
                raise DatabaseSchemaError('Database Schema Error')
            if 'users' in user_org_db:
                for user in user_org_db['users']:
                    if user['user_name'] == user_name:
                        user['organizations'].append(org_name)
                    else:
                        raise UserDoesNotExist('User does not exist!', 402, args)
            else:
                raise DatabaseSchemaError('Database Schema Error', 404, args)
        except (UserDoesNotExist, OrganizationDoesNotExist, DatabaseSchemaError) as e:
            return {'message': e.message, 'payload': args}, e.status
        except Exception:
            return {'message': 'Unexpected Error!', 'payload': args}, 500
        return {'message': 'Added User in Organization!', 'payload': args}, 200


@simple_ns.route('/delete_user_from_organization')
class DeleteUserFromOrganization(Resource):

    @simple_ns.expect(delete_user_from_organization_payload, validate=True)
    @simple_ns.doc(response=responses)
    def post(self):
        """
        DeleteUserFromOrganization API

        Delete a single User to Organization in database
        """
        args = request.get_json()
        org_name = args.get('org_name')
        user_name = args.get('user_name')
        try:
            if user_name not in user_db['user_name']:
                raise UserDoesNotExist('User does not exist!', 402, args)
            if org_name not in organization_db['org_name']:
                raise OrganizationDoesNotExist('Organization does not exist!', 402, args)
            if 'organizations' in user_org_db:
                for org in user_org_db['organizations']:
                    if org['org_name'] == org_name and user_name in org['users']:
                        org['users'].remove(user_name)
                    else:
                        raise OrganizationDoesNotExist('Organization does not exist!', 402, args)
            else:
                raise DatabaseSchemaError('Database Schema Error')
            if 'users' in user_org_db:
                for user in user_org_db['users']:
                    if user['user_name'] == user_name and org_name in user['organizations']:
                        user['organizations'].remove(org_name)
                    else:
                        raise UserDoesNotExist('User does not exist!', 402, args)
            else:
                raise DatabaseSchemaError('Database Schema Error', 404, args)
        except (UserDoesNotExist, OrganizationDoesNotExist, DatabaseSchemaError) as e:
            return {'message': e.message, 'payload': args}, e.status
        except Exception:
            logger.exception('')
            return {'message': 'Unexpected Error!', 'payload': args}, 500
        return {'message': 'Deleted User from organization!', 'payload': args}, 200


@simple_ns.route('/get_users_from_organization')
class GetUsersFromOrganization(Resource):

    @simple_ns.expect(get_all_user_payload, validate=True)
    @simple_ns.doc(response=responses)
    def post(self):
        """
        GetUsersFromOrganization API

        Get Users From Organization in database
        """
        args = request.get_json()
        org_name = args.get('org_name')
        try:
            if org_name not in organization_db['org_name']:
                raise OrganizationDoesNotExist('Organization does not exist!', 402, args)
            if 'organizations' in user_org_db:
                for org in user_org_db['organizations']:
                    if org['org_name'] == org_name:
                        return {'results': org['users'], 'payload':args}, 200
                    else:
                        raise OrganizationDoesNotExist('Organization does not exist!', 402, args)
            else:
                raise DatabaseSchemaError('Database Schema Error', 404, args)
        except (OrganizationDoesNotExist, DatabaseSchemaError) as e:
            return {'message': e.message, 'payload': args}, e.status
        except Exception:
            return {'message': 'Unexpected Error!', 'payload': args}, 500


@simple_ns.route('/get_organizations_belong_to_user')
class GetOrganizationsBelongToUser(Resource):

    @simple_ns.expect(get_all_organization_from_user_payload, validate=True)
    @simple_ns.doc(response=responses)
    def post(self):
        """
        GetOrganizationsBelongToUser API

        Get Organizations Belong To User in database
        """
        args = request.get_json()
        user_name = args.get('user_name')
        try:
            if user_name not in user_db['user_name']:
                raise UserDoesNotExist('User does not exist!', 402, args)
            if 'users' in user_org_db:
                for user in user_org_db['users']:
                    if user['user_name'] == user_name:
                        return {'results': user['organizations'], 'payload': args}, 200
                    else:
                        raise UserDoesNotExist('User does not exist!', 402, args)
            else:
                raise DatabaseSchemaError('Database Schema Error', 404, args)
        except (UserDoesNotExist, DatabaseSchemaError) as e:
            return {'message': e.message, 'payload': args}, e.status
        except Exception:
            logger.exception('Unexpected Error!')
            return {'message': 'Unexpected Error!', 'payload': args}, 500


if __name__ == '__main__':
    app.run(debug=True)
