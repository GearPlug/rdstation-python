![](https://img.shields.io/badge/version-0.1.2-success) ![](https://img.shields.io/badge/Python-3.8%20|%203.9%20|%203.10%20|%203.11-4B8BBE?logo=python&logoColor=white)
# rdstation-python

*rdstation-python* is an API wrapper for RD Station, written in Python.  
This library uses Oauth2 for authentication and webhook notifications.
## Installing
```
pip install rdstation-python
```
## Usage
```
from rdstation.client import Client
client = Client(client_id, client_secret)
```
To obtain and set an access token, follow this instructions:
1. **Get authorization URL**
```
url = client.authorization_url(redirect_uri)
```
2. **Get access token using code**
```
response = client.get_access_token(code)
```
3. **Set access token**
```
client.set_token(access_token)
```
If your access token expired, you can get a new one using refresh token:
```
response = client.refresh_access_token(refresh_token)
```
And then set access token again...  
Check more information about RD Station Oauth: https://legacydevelopers.rdstation.com/es/authentication
#### Get account info
```
info = client.get_account_info()
```
#### Get contact by email
```
contact = client.get_contact_by_email(email)
```
#### Get contact fields
```
fields = client.get_contact_fields()
```
### Leads
#### Create Lead
```
lead_example = {
    "conversion_identifier": "Name of the conversion event",
    "name": "Nome",
    "email": "email2@email.com",
    "job_title": "job title value",
    "state": "state of the contact",
    "city": "city of the contact",
    "country": "country of the contact",
    "personal_phone": "phone of the contact",
    "mobile_phone": "mobile_phone of the contact",
    "twitter": "twitter handler of the contact",
    "facebook": "facebook name of the contact",
    "linkedin": "linkedin user name of the contact",
    "website": "website of the contact",
    "cf_custom_field_api_identifier": "custom field value",
    "company_name": "company name",
    "company_site": "company website",
    "company_address": "company address",
    "client_tracking_id": "lead tracking client_id",
    "traffic_source": "Google",
    "traffic_medium": "cpc",
    "traffic_campaign": "easter-50-off",
    "traffic_value": "easter eggs",
    "tags": ["cml", "2022"],
    "available_for_mailing": True,
    "legal_bases": [{"category": "communications", "type": "consent", "status": "granted"}],
}
event_type = "CONVERSION"
created = client.create_lead(event_type, lead_example)
# event_type options are: CONVERSION, OPPORTUNITY, SALE, OPPORTUNITY_LOST, ORDER_PLACED, ORDER_PLACED_ITEM, CART_ABANDONED, CART_ABANDONED_ITEM, CHAT_STARTED, CHAT_FINISHED, CALL_FINISHED, MEDIA_PLAYBACK_STARTED, MEDIA_PLAYBACK_STOPPED
```
Depending on event type, sent data should be different, check https://legacydevelopers.rdstation.com/es/reference/events for more info.
### Webhooks
#### List webhooks
```
webhooks = client.list_webhooks()
```
#### Create webhook
```
webhook = client.create_webhook(event_type, url, event_identifiers: list = None, include_relations: list =None)
# event type options: "WEBHOOK.CONVERTED", "WEBHOOK.MARKED_OPPORTUNITY"
```
#### Delete webhook
```
client.delete_webhook(uuid)
```
