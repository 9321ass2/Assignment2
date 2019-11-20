import secrets
import json
import numpy as np
from restapi import client
Userdb = client.USER
TokenCollection = Userdb.tokens


def User_Token(user,token):
    Valid = False
    query = TokenCollection.find_one({'username':user,'token':token})
    if query is not None:
        Valid = True
    return Valid


