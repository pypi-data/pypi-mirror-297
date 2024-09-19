import base64
from typing import Optional, Any

import requests
import json


class PyOptimumException(Exception):
    """
    pyoptimum Exception
    """
    pass


class Client:
    """
    Client object to facilitate connection to the
    `optimize.vicbee.net <https:optimize.vicbee.net>`_ optimization api

    Calls will be made to a URL of the form:

    ``base_url/api/prefix/entry_point``

    in which ``entry_point`` is set in :meth:`pyoptimum.Client.call`.

    :param username: the username
    :param password: the password
    :param token: an authentication token
    :param auto_token_renewal: whether to automatically renew an expired token
    :param base_url: the api base url
    :param api: the target api
    :param prefix: the target api prefix
    """

    def __init__(self,
                 username: Optional[str] = None, password: Optional[str] = None,
                 token: Optional[str] = None,
                 auto_token_renewal: Optional[bool] = True,
                 base_url: Optional[str] = 'https://optimize.vicbee.net',
                 api: Optional[str] = 'optimize',
                 prefix: Optional[str] = 'api'):

        # username and password
        self.username = username
        self.password = password

        # token
        self.token = token

        # auto token renewal
        self.auto_token_renewal = auto_token_renewal

        if not self.token and (not self.username or not self.password):
            raise PyOptimumException("Token or username/password "
                                     "have not been provided.")

        # base url
        self.base_url = base_url
        # make sure base_url does not have trailing /
        while self.base_url[-1] == '/':
            self.base_url = self.base_url[:-1]
        # add api prefix
        self.base_url = f'{self.base_url}/{api}/{prefix}'

        # initialize detail
        self.detail = None

    def get_token(self) -> None:
        """
        Retrieve authentication token
        """

        basic = base64.b64encode(bytes('{}:{}'.format(self.username, self.password),
                                       'utf-8')).decode('utf-8')
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Basic ' + basic
        }

        response = requests.get(f'{self.base_url}/get_token', headers=headers)
        self.detail = None

        if response.ok:

            self.token = response.json().get('token')

        else:

            response.raise_for_status()

    def call(self, entry_point: str, data: Any) -> Any:
        """
        Calls the api ``entry_point`` with ``data``

        :param entry_point: the api entry point
        :param data: the data
        :return: dictionary with the response
        """

        if self.token is None and not self.auto_token_renewal:
            raise PyOptimumException('No token available. Call get_token first')

        elif self.auto_token_renewal:
            # try renewing token
            self.get_token()

        # make sure entry point does not start with a slash
        while entry_point and entry_point[0] == '/':
            entry_point = entry_point[1:]

        # See https://github.com/psf/requests/issues/6014
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'X-Api-Key': self.token
        }
        response = requests.post(f'{self.base_url}/{entry_point}',
                                 data=json.dumps(data),
                                 headers=headers)

        if response.ok:

            self.detail = None
            return response.json()

        else:

            if response.status_code == 400:
                content = json.loads(response.content)
                self.detail = content.get('detail', None)
                if self.detail:
                    raise PyOptimumException(self.detail)
            response.raise_for_status()
