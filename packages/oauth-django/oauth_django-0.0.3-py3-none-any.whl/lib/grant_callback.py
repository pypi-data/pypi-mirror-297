import http.client
import json
import urllib.parse
#import jwt
from django.http import HttpResponse
from .Config import GrantInit
from .logging_file import logger
import urllib.parse
from .oauth_utils import decode_and_respond_token


class GrantCallbackBase(GrantInit):

    def grant_callback(self, request):

        logger.info("in GrantCallbackBase grant_callback")
        state = request.GET.get('state')
        logger.info("state")

        stored_state = self.set_get_state.get_state()

        if state != stored_state:
            return HttpResponse("State mismatch", status=400)

        code = request.GET.get('code')
        logger.info(code)
        logger.info("code")
        logger.info(code)

        if code:
            logger.info("in if code:")
            payload = self.create_payload(code)
            token = self.request_token(payload)
        else:
            logger.info("in else:")
            token = request.GET.get('id_token')

        logger.info("outside code")
        if token:
            logger.info("in token")
            logger.info(token)
            return decode_and_respond_token(token, self.certificate, self.client_id)
        else:
            return HttpResponse("----No token received----")

    def create_payload(self, code):
        logger.info("in create_payload")
        raise NotImplementedError("Subclasses must implement this method")

    @staticmethod
    def request_token(payload):
        logger.info("in request_token")
        conn = http.client.HTTPSConnection('v.xecurify.com')
        logger.info("conn")
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        try:
            logger.info("in try block")
            conn.request('POST', '/moas/rest/oauth/token', body=payload, headers=headers)
            response = conn.getresponse()
            logger.info(response)
            if response.status == 200:
                logger.info("in if ")
                response_body = response.read().decode()
                logger.info("print result")
                result = json.loads(response_body)
                logger.info(result)
                return result.get('id_token')
            else:
                logger.info("in else")
                return None
        finally:
            conn.close()


class AuthorizationCodeGrantCallback(GrantCallbackBase):
    def create_payload(self, code):
        return urllib.parse.urlencode({
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'code': code
        })


class PKCEGrantCallback(GrantCallbackBase):
    def create_payload(self, code):

        code_verifier = self.set_get_verifier.get_verifier()

        return urllib.parse.urlencode({
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'code': code,
            'code_verifier': code_verifier
        })


class ImplicitGrantCallback(GrantCallbackBase):

    def create_payload(self, code):
        logger.info("in ImplicitGrantCallback create_payload")
        pass
