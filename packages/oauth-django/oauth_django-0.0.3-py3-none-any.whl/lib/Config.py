from .oauth_utils import Printtoken, Printverifier, Printstate, Printaccess

class GrantInit:

    def __init__(self, client_id, client_secret, base_url, redirect_uri, certificate, request):

        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url
        self.redirect_uri = redirect_uri
        self.certificate = certificate
        self.set_get_token = Printtoken(request)
        self.set_get_verifier = Printverifier(request)
        self.set_get_state = Printstate(request)


class PasswordInit:

    def __init__(self, client_id, client_secret, username, password, request):

        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = 'v.xecurify.com'
        self.username = username
        self.password = password
        self.set_get_token = Printtoken(request)
        self.set_get_access = Printaccess(request)