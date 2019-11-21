from restapi import api
from flask_restplus import fields,reqparse


Format_Recommend_PUT = api.model('Format_Recommend_PUT', {
  'preference': fields.List(fields.String,description='use Rank'),
})
Format_Recommend_POST = api.model('Format_Recommend_POST', {
  'username':fields.String(required=True),
  'preference': fields.List(fields.String,description='use Rank')
})
Format_User_PUT = api.model('Format_User_PUT', {
  'email': fields.String(required=True),
})
Format_Register = api.model('Format_Register', {
  'username': fields.String(required=True),
  'password': fields.String(required=True),
  'email': fields.String(required=True),
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

Format_Token = api.parser().add_argument('AUTH-TOKEN',location='headers',help=' put your TOKEN here if you\'re not using API ')
Format_Credential1 = api.parser().add_argument('username',location='headers',required=True)
Format_Credential2 = api.parser().add_argument('password',location='headers',required=True)

platform_text = """
    choose one of the platforms, empty would be all.
    ['Wii', 'NES', 'PC', 'GB', 'DS', 'X360', 'SNES', 'PS3', 'PS4',
     '3DS', 'PS2', 'GBA', 'NS', 'GEN', 
    'N64', 'PS', 'XOne', 'WiiU', 'XB', 'PSP', '2600', 'GC', 'GBC', 'PSN', 'PSV', 'DC', 'SAT', 'SCD', 
    'WS', 'XBL', 'Amig', 'VC', 'NG', 'WW', 'PCE', '3DO', 'GG', 'OSX', 'PCFX', 'Mob', 'And', 'Ouya', 'DSiW',
     'MS', 'DSi', 'VB', 'Linux', 'MSD', 'C128', 'AST', 'Lynx', '7800', '5200', 'S32X', 'MSX', 'FMT', 'ACPC',
      'C64', 'BRW', 'AJ', 'ZXS', 'NGage',
     'GIZ', 'WinP', 'iQue', 'iOS', 'Arc', 'ApII', 'Aco', 'BBCM', 'TG16', 'CDi', 'CD32', 'Int']
"""
region_text = """
    choose one of the region, empty is Global_Sales
    ['Global_Sales', 'NA_Sales', 'PAL_Sales', 'JP_Sales', 'Other_Sales']
"""
genre_text = """
    choose one of the genre, empty would be all.
    ['Sports', 'Platform', 'Racing', 'Shooter', 'Role-Playing',
     'Puzzle', 'Misc', 'Party', 'Simulation', 'Action', 'Action-Adventure',
      'Fighting', 'Strategy', 'Adventure', 'Music', 'MMO', 'Sandbox',
       'Visual Novel', 'Board Game', 'Education']
"""
TopSale_parser = reqparse.RequestParser()
TopSale_parser.add_argument('top', help='     top(?)  ,top10 if empty',type=int)
TopSale_parser.add_argument('region', help=region_text)
TopSale_parser.add_argument('year', help='    after 1970 ~    ',type=int)
TopSale_parser.add_argument('platform',help=platform_text)
TopSale_parser.add_argument('genre',help=genre_text)


TopScore_parser = reqparse.RequestParser()
TopScore_parser.add_argument('top', help='     top(?)  ,top10 if empty',type=int)
TopScore_parser.add_argument('year', help='    after 1970 ~    ',type=int)
TopScore_parser.add_argument('platform',help=platform_text)
TopScore_parser.add_argument('genre',help=genre_text)

LinearP_parser = reqparse.RequestParser()
LinearP_parser.add_argument('year', help='    after 2019    ',type=int)
LinearP_parser.add_argument('platform',help=platform_text)
LinearP_parser.add_argument('genre',help=genre_text)

ESRB_parser = reqparse.RequestParser()
ESRB_parser.add_argument('game_information')