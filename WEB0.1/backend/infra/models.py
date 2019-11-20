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
Format_Countries = {
    "Country": fields.String(required=True),
    "Region": fields.String(required=True),
    "Population": fields.Integer(required=True),
    "region_sale": fields.Float,
    "region_population": fields.Integer,
    "region_per_person": fields.Float,
    "country_sale": fields.Float,
    "Identifier": fields.Integer(required=True)
  }
Format_Games = {
  "Identifier": fields.Integer(required=True),
  "Name": fields.String(required=True),
  "Genre": fields.String(required=True),
  "ESRB_Rating": fields.String,
  "Platform": fields.String(required=True),
  "Publisher": fields.String(required=True),
  "Developer": fields.String(required=True),
  "Critic_Score": fields.Float,
  "User_Score": fields.Float,
  "Global_Sales": fields.Float,
  "NA_Sales": fields.Float,
  "PAL_Sales": fields.Float,
  "JP_Sales": fields.Float,
  "Other_Sales": fields.Float,
  "Year": fields.Integer(required=True, example='2019')
}
Format_Games_model = api.model('Format_Games',Format_Games)
Format_Countries_model =  api.model('Format_Countries',Format_Countries)

Format_Token = api.parser().add_argument('AUTH-TOKEN',location='headers',help=' put your TOKEN here')
Format_Credential1 = api.parser().add_argument('username',location='headers',required=True)
Format_Credential2 = api.parser().add_argument('password',location='headers',required=True)