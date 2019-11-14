from restapi import api
from flask_restplus import fields


Format_LOGIN = api.model('Format_LOGIN', {
  'username': fields.String(required=True, example='xX_greginator_Xx'),
  'password': fields.String(required=True, example='1234'),
})


Format_Register = api.model('Format_Register', {
  'username': fields.String(required=True, example='xX_greginator_Xx'),
  'password': fields.String(required=True, example='1234'),
  'email': fields.String(required=True, example='greg@fred.com'),
  'role':  fields.String(required=True, example='player or developer')
})

credential_model = api.model('credential', {
    'username': fields.String,
    'password': fields.String
})
