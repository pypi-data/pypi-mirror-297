import http.client
import urllib.parse
import json
import logging
from django.http import HttpResponse
from .Config import PasswordInit
from .logging_file import logger


class GrantTokenBase(PasswordInit):

    def get_access_token(self, request):
        raise NotImplementedError("Subclasses must implement this method to handle specific grant types.")

class PasswordGrantToken(GrantTokenBase):

    def get_access_token(self, request):
        conn = http.client.HTTPSConnection(self.base_url)
        payload = urllib.parse.urlencode({
            'grant_type': 'password',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'username': self.username,
            'password': self.password
        })
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        try:
            conn.request('POST', '/moas/rest/oauth/token', body=payload, headers=headers)
            response = conn.getresponse()

            if response.status == 200:
                response_body = response.read().decode()
                result = json.loads(response_body)
                access_token = result.get('access_token')
                logger.info("Access token in PasswordGrantToken:")
                logger.info(access_token)
                self.set_get_access.set_access(access_token)
                return HttpResponse(f"Access token: {access_token}")
            else:
                return HttpResponse(f"Failed with status code {response.status}", status=response.status)
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=500)
        finally:
            conn.close()
