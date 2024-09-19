import base64
import hashlib
import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import secrets
from django.http import HttpResponse
from .logging_file import logger
import os


def generate_code_verifier():
    code_verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('ascii')
    logger.info("In generate_code_verifier " + code_verifier)
    return code_verifier



def generate_code_challenge(verifier):
    hashed = hashlib.sha256(verifier.encode('ascii')).digest()
    logger.info("In generate_code_challenge hashing code_verifier ")
    code_challenge = base64.urlsafe_b64encode(hashed).rstrip(b'=').decode('ascii')
    logger.info("In generate_code_challenge code challenge generated")
    logger.info(code_challenge)
    return code_challenge


def decode_jwt_token(token, certificate, client_id):

    logger.info("certificate")
    logger.info(certificate)
    logger.info("token")
    logger.info(token)
    logger.info("client_id")
    logger.info(client_id)

    public_key = serialization.load_pem_public_key(certificate.encode(), backend=default_backend())

    try:
        decoded_token = jwt.decode(token, public_key, algorithms=["RS256"], audience=client_id, leeway=60)
        logger.info("got decoded_token")
        logger.info(decoded_token)
        return decoded_token
    except jwt.ExpiredSignatureError:
        logger.info("Token expired")
        raise
    except jwt.InvalidTokenError:
        logger.info("Invalid token")
        raise


def decode_and_respond_token(token, certificate, client_id):
    try:
        decoded_token = decode_jwt_token(token, certificate, client_id)
        logger.info("in try of decode_and_respond_token")
        return decoded_token


    except jwt.ExpiredSignatureError:
        logger.error("Token expired")
        return HttpResponse("Token expired")
    except jwt.InvalidTokenError:
        logger.error("Invalid token")
        return HttpResponse("Invalid token")


def generate_random_state(length=16):
    state = secrets.token_urlsafe(length)
    logger.info(f"Generated random state: {state}")
    return state


class Printtoken:

    def __init__(self, request):
        self.request = request

    def set_decoded_token(self, decoded_token):
        logger.info("In set_decoded_token")
        logger.info(decoded_token)
        self.request.session['token'] = decoded_token

    def get_decoded_token(self):
        logger.info("In get_decoded_token")
        return self.request.session.get('token')


class Printverifier:

    def __init__(self, request):
        self.request = request

    def set_verifier(self, decoded_token):
        logger.info("In set_verifier")
        logger.info(decoded_token)
        self.request.session['token'] = decoded_token

    def get_verifier(self):
        logger.info("In get_verifier")
        return self.request.session.get('token')


class Printstate:

    def __init__(self, request):
        self.request = request

    def set_state(self, state):
        logger.info("In set_state")
        logger.info(state)
        # request.session['state'] = state
        self.request.session['state'] = state

    def get_state(self):
        logger.info("In get_state")
        return self.request.session.get('state')


class Printaccess:

    def __init__(self, request):
        self.request = request

    def set_access(self, access_token):
        logger.info("In set_access")
        logger.info(access_token)
        self.request.session['access_token'] = access_token

    def get_access(self):
        logger.info("In get_access")
        logger.info(self.request.session.get('access_token'))
        return self.request.session.get('access_token')


