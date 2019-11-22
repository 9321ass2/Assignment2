import secrets
import json
import numpy as np
from restapi import client

Userdb = client.USER
TokenCollection = Userdb.tokens


def User_Token(user, token):
    Valid = False
    query = TokenCollection.find_one({'username': user, 'token': token})
    if query is not None:
        Valid = True
    return Valid


def isAdmin(token):
    Valid = False
    query = TokenCollection.find_one({'token': token})
    if query['username'] == 'admin':
        Valid = True
    return Valid


def df_to_json(df):
    json_str = df.to_json(orient='index')
    ds = json.loads(json_str)
    ret = []
    for idx in ds:
        ele = ds[idx]
        ele['Identifier'] = int(idx)
        ret.append(ele)
    return ret