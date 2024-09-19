import urllib.parse
from django.shortcuts import redirect
from .Config import GrantInit
from .logging_file import logger
from .oauth_utils import generate_random_state, generate_code_verifier, generate_code_challenge

class GrantRedirectBase(GrantInit):

    def grant_redirect(self, request):


        state = generate_random_state()
        logger.info("grant_redirect")

        payload = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': 'openid',
            'response_type': 'code',
            'state': state,
        }

        logger.info("set payload")
        self.modify_payload_for_grant_type(payload)


        query_string = urllib.parse.urlencode(payload)
        logger.info("query_string")
        url = f"{self.base_url}?{query_string}"


        self.set_get_state.set_state(state)

        return redirect(url)

    def modify_payload_for_grant_type(self, payload):
        logger.info("in modify_payload_for_grant_type")
        raise NotImplementedError("Subclasses must implement this method")

class AuthorizationCodeGrantRedirect(GrantRedirectBase):
    def modify_payload_for_grant_type(self, payload):
        logger.info("in AuthorizationCodeGrantRedirect modify_payload_for_grant_type")
        pass

class PKCEGrantRedirect(GrantRedirectBase):
    def modify_payload_for_grant_type(self, payload):

        code_verifier = generate_code_verifier()
        code_challenge = generate_code_challenge(code_verifier)
        self.set_get_verifier.set_verifier(code_verifier)

        payload.update({
            'code_challenge': code_challenge,
            'code_challenge_method': 'S256',
        })

        self.set_get_verifier.set_verifier(code_verifier)
        logger.info("in PKCEGrantRedirect modify_payload_for_grant_type")

class ImplicitGrantRedirect(GrantRedirectBase):
    def modify_payload_for_grant_type(self, payload):

        payload['response_type'] = 'token'
        logger.info("in ImplicitGrantRedirect modify_payload_for_grant_type")
