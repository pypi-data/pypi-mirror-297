import http.client
import json
from django.http import HttpResponse
from .Config import PasswordInit
from .logging_file import logger


class GrantUserInfoBase(PasswordInit):


    def get_user_info(self, request):
        raise NotImplementedError("Subclasses must implement this method to handle specific grant types.")

class PasswordGrantUserInfo(GrantUserInfoBase):
    def get_user_info(self, request):

        access_token = self.set_get_access.get_access()

        logger.info("Access token for user info:")
        logger.info(access_token)

        conn = http.client.HTTPSConnection(self.base_url)
        headers = {'Authorization': f'Bearer {access_token}'}

        try:
            conn.request('GET', '/moas/rest/oauth/getuserinfo', headers=headers)
            response = conn.getresponse()
            response_body = response.read().decode()

            if response.status == 200:
                user_data = json.loads(response_body)
                logger.info("User info retrieved:")
                logger.info(user_data)
                self.set_get_token.set_decoded_token(user_data)
                return HttpResponse(f"User Data: {user_data}")
            else:
                return HttpResponse(f"Failed with status code {response.status}", status=response.status)
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=500)
        finally:
            conn.close()
