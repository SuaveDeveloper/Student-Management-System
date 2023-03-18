# from flask import request,jsonify
# from flask_restx import Namespace, Resource, fields, Api
# # from ..models.users import User
# from ..models.students import Student
# from ..utils import db
# from werkzeug.security import generate_password_hash, check_password_hash
# from http import HTTPStatus
# from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity,unset_jwt_cookies


# auth_namespace = Namespace ('Auth', description= 'Namespace for Authentication')

# @auth_namespace.route('/')
# class HelloAuth(Resource):
#     def get(self):
#         return {"message": "Hello Auth nice to meet you"}

# signup_model = auth_namespace.model(
#     'SignUp', {
#         # 'id': fields.Integer(),
#         'full_name':fields.String(required=True, description= 'A fullname'),
#         'email':fields.String(required=True, description= 'An email'),
#         'password':fields.String(required=True, description= 'A password')
#     }

# )

# login_model = auth_namespace.model(
#     'Login', {
#         'email': fields.String(required=True, description="An email"),
#         'password': fields.String(required=True, description="A password")
#     }
# )

# user_model = auth_namespace.model(
#     'User', {
#         'id': fields.Integer(),
#         'full_name': fields.String(required=True, description="A username"),
#         'email': fields.String(required=True, description="An email"),
#         'password': fields.String(required=True, description="A password"),
#         # 'is_active': fields.Boolean(description="This shows if a User is active or not"),
#         # 'is_staff': fields.Boolean(description="This shows that if a User is a member of staff")
#     }
# )

# @auth_namespace.route('/signup')
# class SignUp(Resource):

#     print('it hit')

#     @auth_namespace.expect(signup_model)
#     @auth_namespace.marshal_with(user_model)
#     def post(self):
        
#         """
#             Sign up a user
#         """
#         data= request.get_json()
#         # print(data, 'it received')

#         # data = {'username': 'Sanmi', 'email': 'sanmi@gmail.com', 'password': 'namyown'}

#         new_user = Student(
#             full_name = data.get('full_name'),
#             email = data.get('email'),
#             password = generate_password_hash(data.get('password'))

#         )
#         print(new_user)
#         new_user.save()
        
#         return new_user, HTTPStatus.CREATED

# @auth_namespace.route('/login')
# class Login(Resource):
#     @auth_namespace.expect(login_model)
#     def post(self):


#         """
#             Generate JWT Token
#         """
#         data = request.get_json()

#         email = data.get('email')
#         password = data.get('password')

#         user = Student.query.filter_by(email=email).first()

#         if (user is not None) and check_password_hash(user.password_hash, password):
#             access_token = create_access_token(identity=user.username)
#             refresh_token = create_refresh_token(identity=user.username)

#             response = {
#                 'access_token': access_token,
#                 'refresh_token': refresh_token
#             }

#             return response, HTTPStatus.CREATED


# @auth_namespace.route('/refresh')
# class Refresh(Resource):
#     @jwt_required(refresh=True)
#     def post(self):
#         """
#             Generate Refresh Token
#         """
#         username = get_jwt_identity()

#         access_token = create_access_token(identity=username)

#         return {'access_token': access_token}, HTTPStatus.OK


# @auth_namespace.route('/logout')
# class Logout(Resource):
#     @jwt_required()
#     def post(self):
#         """
#             Log the User Out
#         """

#         unset_jwt_cookies
#         db.session.commit()
#         return {"message": "Successfully Logout Out"}, HTTPStatus.OK




from flask import request
from flask_restx import Namespace, Resource, fields
from ..models.users import User
from ..utils.blacklist import BLACKLIST
from ..utils.decorators import admin_required
from werkzeug.security import check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt

auth_namespace = Namespace('auth', description='Namespace for Authentication')

user_model = auth_namespace.model(
    'User', {
        'id': fields.Integer(description="User ID"),
        'first_name': fields.String(required=True, description="First Name"),
        'last_name': fields.String(required=True, description="Last Name"),
        'email': fields.String(required=True, description="User's Email"),
        'password_hash': fields.String(required=True, description="User's Password"),
        'user_type': fields.String(required=True, description="Type of User")  
    }
)

login_model = auth_namespace.model(
    'Login', {
        'email': fields.String(required=True, description="User's Email"),
        'password': fields.String(required=True, description="User's Password")
    }
)

@auth_namespace.route('/users')
class GetAllUsers(Resource):
    @auth_namespace.marshal_with(user_model)
    @auth_namespace.doc(
        description="Retrieve all users"
    )
    @admin_required()
    def get(self):
        """
            Retrieve all Users - Admins Only
        """
        users = User.query.all()

        return users, HTTPStatus.OK

@auth_namespace.route('/login')
class Login(Resource):
    @auth_namespace.expect(login_model)
    def post(self):
        """
            Generate JWT Token
        """
        data = auth_namespace.payload

        email = data['email']
        password = data['password']

        user = User.query.filter_by(email=email).first()

        if (user is not None) and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)

            response = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }

            return response, HTTPStatus.CREATED


@auth_namespace.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """
            Refresh Access Token
        """
        user = get_jwt_identity()

        access_token = create_access_token(identity=user)

        return {'access_token': access_token}, HTTPStatus.OK


@auth_namespace.route('/logout')
class Logout(Resource):
    @jwt_required(verify_type=False)
    def post(self):
        """
            Revoke Access/Refresh Token
        """
        token = get_jwt()
        jti = token["jti"]
        token_type = token["type"]
        BLACKLIST.add(jti)
        return {"message": f"{token_type.capitalize()} token successfully revoked"}, HTTPStatus.OK