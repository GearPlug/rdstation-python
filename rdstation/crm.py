import json

from urllib.parse import urlencode
import requests

from rdstation.exceptions import UnauthorizedError, WrongFormatInputError, ContactsLimitExceededError


class CRMClient(object):
    URL = "https://crm.rdstation.com/api/v1/"
    AUTH_ENDPOINT = "auth/dialog?"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    def __init__(self, token):
        self.TOKEN = token

    def list_contacts(self, page=None, limit=None, order=None, direction=None, email=None, query=None):
        """
        limit: default is 20. Max is 200. \n
        order: field to be sorted. Default is 'name' \n
        direction: 'asc' or 'desc', defaulti is 'asc' \n
        email: filter by email \n
        query: name of contact to be searched" \n
        """
        params = {}
        if page is not None:
            params.update(page=page)
        if limit is not None:
            params.update(limit=limit)
        if order is not None:
            params.update(order=order)
        if direction is not None:
            params.update(direction=direction)
        if email is not None:
            params.update(email=email)
        if query is not None:
            params.update(query=query)
        return self.get("contacts", params=params)

    def create_contact(self, contact_data, custom_data=None):
        if custom_data is not None:
            contact_data["contact_custom_fields"] = custom_data
        item = {"contact": contact_data}
        return self.post("contacts", data=json.dumps(item))

    def list_companies(self, page=None, limit=None, order=None, direction=None, user_id=None, query=None):
        if page is not None:
            params.update(page=page)
        if limit is not None:
            params.update(limit=limit)
        if order is not None:
            params.update(order=order)
        if direction is not None:
            params.update(direction=direction)
        if user_id is not None:
            params.update(user_id=user_id)
        if query is not None:
            params.update(q=query)
        params = {}
        return self.get("organizations", params=params)

    def list_custom_fields(self, option=None):
        """
        option: "contact", "deal", "organization"
        """
        params = {}
        if option is not None:
            params.update({"for": option})
        return self.get("custom_fields", params=params)

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

    def request(self, method, endpoint, headers=None, params={}, **kwargs):
        params.update(token=self.TOKEN)
        return requests.request(method, self.URL + endpoint, headers=self.headers, params=params, **kwargs)

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
