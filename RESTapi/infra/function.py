import secrets
from restapi import client


def Create_crypto():
    crypto = secrets.token_urlsafe(16)
    TokensCollection = client.User.Tokens
    duplicate = TokensCollection.find_one({"token": crypto})
    if duplicate is not None:
        crypto = secrets.token_urlsafe(16)
    return crypto


