import json
from urllib.parse import urlencode

import requests

from rdstation.exceptions import UnauthorizedError, WrongFormatInputError, ContactsLimitExceededError


class Client(object):
    URL = "https://api.rd.services/"
    AUTH_ENDPOINT = "auth/dialog?"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    def __init__(self, client_id=None, client_secret=None):
        self.CLIENT_ID = client_id
        self.CLIENT_SECRET = client_secret

    def authorization_url(self, redirect_uri, state=None):
        params = {"client_id": self.CLIENT_ID, "redirect_uri": redirect_uri}
        if state:
            params["state"] = state
        return self.URL + self.AUTH_ENDPOINT + urlencode(params)

    def get_access_token(self, code):
        body = {"client_id": self.CLIENT_ID, "client_secret": self.CLIENT_SECRET, "code": code}
        return self.post("auth/token", data=json.dumps(body))

    def refresh_access_token(self, refresh_token):
        body = {"client_id": self.CLIENT_ID, "client_secret": self.CLIENT_SECRET, "refresh_token": refresh_token}
        return self.post("auth/token", data=json.dumps(body))

    def set_token(self, access_token):
        self.headers.update(Authorization=f"Bearer {access_token}")

    def get_account_info(self):
        return self.get("marketing/account_info")

    def get_contact_by_email(self, email):
        return self.get(f"platform/contacts/email:{email}")

    def get_contact_fields(self):
        return self.get(f"platform/contacts/fields")

    def create_lead(self, event_type, data):
        item = {"event_type": event_type, "event_family": "CDP", "payload": data}
        return self.post("platform/events", data=json.dumps(item))

    def list_webhooks(self):
        return self.get("integrations/webhooks")

    def create_webhook(self, event_type, url, event_identifiers:list=[], include_relations:list=[]):
        data = {
            "entity_type": "CONTACT",
            "event_type": event_type,
            "event_identifiers": event_identifiers,
            "url": url,
            "http_method": "POST",
            "include_relations": include_relations
        }
        return self.post("integrations/webhooks", data=json.dumps(data))

    def delete_webhook(self, uuid):
        return self.delete(f"integrations/webhooks/{uuid}")

    def get(self, endpoint, **kwargs):
        response = self.request("GET", endpoint, **kwargs)
        return self.parse(response)

    def post(self, endpoint, **kwargs):
        response = self.request("POST", endpoint, **kwargs)
        return self.parse(response)

    def delete(self, endpoint, **kwargs):
        response = self.request("DELETE", endpoint, **kwargs)
        return self.parse(response)

    def put(self, endpoint, **kwargs):
        response = self.request("PUT", endpoint, **kwargs)
        return self.parse(response)

    def patch(self, endpoint, **kwargs):
        response = self.request("PATCH", endpoint, **kwargs)
        return self.parse(response)

    def request(self, method, endpoint, headers=None, **kwargs):
        if headers:
            self.headers.update(headers)
        return requests.request(method, self.URL + endpoint, headers=self.headers, **kwargs)

    def parse(self, response):
        status_code = response.status_code
        if "Content-Type" in response.headers and "application/json" in response.headers["Content-Type"]:
            try:
                r = response.json()
            except ValueError:
                r = response.text
        else:
            r = response.text
        if status_code == 200:
            return r
        if status_code == 204:
            return None
        if status_code == 400:
            raise WrongFormatInputError(r)
        if status_code == 401:
            raise UnauthorizedError(r)
        if status_code == 406:
            raise ContactsLimitExceededError(r)
        if status_code == 500:
            raise Exception
        return r
