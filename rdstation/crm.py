import json

import requests

from rdstation.exceptions import UnauthorizedError, WrongFormatInputError, ContactsLimitExceededError


class CRMClient(object):
    URL = "https://crm.rdstation.com/api/v1/"
    AUTH_ENDPOINT = "auth/dialog?"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    def __init__(self, token):
        self.TOKEN = token

    def list_users(self):
        return self.get("users")

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

    def create_contact(
        self,
        name,
        title=None,
        birthday=None,
        email=None,
        phone=None,
        organization_id=None,
        deal_ids: list = None,
        custom_data=None,
    ):
        """
        birthday format must be: 'YYYY-MM-DD' \n
        deal_ids must be an array of deal ids strings
        """
        item = {"contact": {"name": name}}
        if title is not None:
            item["contact"]["title"] = title
        if birthday is not None:
            try:
                year, month, day = birthday.split("-")
            except ValueError:
                return "Error: Birthday format must be 'YYYY-MM-DD'"
            item["contact"]["birthday"] = {"day": day, "month": month, "year": year}
        if email is not None:
            item["contact"]["emails"] = [{"email": email}]
        if email is not None:
            item["contact"]["phones"] = [{"phone": phone}]
        if organization_id is not None:
            item["contact"]["organization_id"] = organization_id
        if deal_ids is not None:
            item["contact"]["deal_ids"] = deal_ids
        if custom_data is not None:
            item["contact"]["contact_custom_fields"] = custom_data
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

    def list_opportunities(
        self,
        page=None,
        limit=None,
        order=None,
        direction=None,
        name=None,
        win=None,
        user_id=None,
        closed_at=None,
        closed_at_period=None,
        created_at_period=None,
        prediction_date_period=None,
        start_date=None,
        end_date=None,
        campaign_id=None,
        deal_stage_id=None,
        deal_pipeline_id=None,
        organization=None,
        hold=None,
    ):
        """
        Check this site if you need more information about how these filters work: \n
        https://developers.rdstation.com/reference/listar-2
        """
        params = {}
        args = locals()
        for arg in args:
            if args[arg] is not None and arg != "self" and arg != "params":
                params.update({f"{arg}": args[arg]})
        return self.get("deals", params=params)

    def create_opportunity(
        self,
        name,
        deal_stage_id=None,
        organization_id=None,
        deal_source_id=None,
        campaign_id=None,
        user_id=None,
        hold: bool = None,
        rating=None,
        win: bool = None,
        prediction_date=None,
        custom_data=None,
    ):
        """
        Custom data must be an array of dicts with the following structure: \n
        custom_data = [
            {
                "custom_field_id": "6414c0fc43ba490012f96c64",
                "value": "A text custom field"
            }
        ]
        Check this site for more information: https://developers.rdstation.com/reference/oportunidades
        """
        data = {"deal": {"name": name}}
        args = locals()
        first_layer_args = ["organization_id", "deal_source_id", "campaign_id"]
        ignore_args = ["self", "data", "name"]
        for arg in args:
            if arg not in ignore_args and args[arg] is not None:
                if arg in first_layer_args:
                    data[arg.replace("_id", "")] = {"_id": args[arg]}
                elif arg == "custom_data":
                    data["deal"]["deal_custom_fields"] = custom_data
                else:
                    data["deal"][arg] = args[arg]
        return self.post("deals", data=json.dumps(data))

    def list_custom_fields(self, option=None):
        """
        option: "contact", "deal", "organization"
        """
        params = {}
        if option is not None:
            params.update({"for": option})
        return self.get("custom_fields", params=params)

    def list_deal_stages(self, page=None, limit=None):
        params = {}
        if page is not None:
            params.update(page=page)
        if limit is not None:
            params.update(limit=limit)
        return self.get("deal_stages", params=params)

    def list_deal_pipelines(self):
        return self.get("deal_pipelines")

    def list_deal_sources(self):
        return self.get("deal_sources")

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
