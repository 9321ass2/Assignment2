from restapi import api
from flask_restplus import fields


Format_Recommend_Post = api.model('Format_Recommend_POST', {
  'username': fields.String(required=True, example='xX_greginator_Xx'),
  'preference': fields.List(fields.Integer),
})
Format_Recommend_Get = api.model('Format_Recommend_GET', {
  'username': fields.String(required=True, example='xX_greginator_Xx'),
})

Format_Register = api.model('Format_Register', {
  'username': fields.String(required=True, example='xX_greginator_Xx'),
  'password': fields.String(required=True, example='1234'),
  'email': fields.String(required=True, example='greg@fred.com'),
  'role':  fields.String(required=True, example='player or developer')
})

Format_Login = api.model('Format_Login', {
  'username': fields.String(required=True, example='xX_greginator_Xx'),
  'password': fields.String(required=True, example='1234'),
})



Format_Token = api.parser().add_argument('AUTH-TOKEN',location='headers')
Format_Credential1 = api.parser().add_argument('username',location='headers')
Format_Credential2 = api.parser().add_argument('password',location='headers')