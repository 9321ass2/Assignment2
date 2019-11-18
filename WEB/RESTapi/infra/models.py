from restapi import api
from flask_restplus import fields


Format_Recommend = api.model('Format_Recommend', {
  'username': fields.String(required=True, example='user'),
  'preference': fields.List(fields.String),
})
Format_Register = api.model('Format_Register', {
  'username': fields.String(required=True, example='Martin'),
  'password': fields.String(required=True, example='1234'),
  'email': fields.String(required=True, example='greg@fred.com'),
  'role':  fields.String(required=True, example='player or developer')
})

Format_Login = api.model('Format_Login', {
  'username': fields.String(required=True, example='Kelvin'),
  'password': fields.String(required=True, example='1234'),
})

Format_Token = api.parser().add_argument('AUTH-TOKEN',location='headers')
Format_Credential1 = api.parser().add_argument('username',location='headers')
Format_Credential2 = api.parser().add_argument('password',location='headers')