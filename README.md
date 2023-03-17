# rdstation-python
![](https://img.shields.io/badge/version-0.2.1-success) ![](https://img.shields.io/badge/Python-3.8%20|%203.9%20|%203.10%20|%203.11-4B8BBE?logo=python&logoColor=white)  

*rdstation-python* is an API wrapper for RD Station, written in Python.
1. [RD Station Marketing](#1-rd-station-marketing) (This product uses Oauth2 for authentication and webhook notifications). 
2. [RD Station CRM](#2-rd-station-crm)

## Installing
```
pip install rdstation-python
```
## 1. RD Station Marketing
### Usage
```python
from rdstation.client import Client
client = Client(client_id, client_secret)
```
To obtain and set an access token, follow this instructions:
1. **Get authorization URL**
```python
url = client.authorization_url(redirect_uri)
```
2. **Get access token using code**
```python
response = client.get_access_token(code)
```
3. **Set access token**
```python
client.set_token(access_token)
```
If your access token expired, you can get a new one using refresh token:
```python
response = client.refresh_access_token(refresh_token)
```
And then set access token again...  
Check more information about RD Station Oauth: https://legacydevelopers.rdstation.com/es/authentication
#### Get account info
```python
info = client.get_account_info()
```
#### Get contact by email
```python
contact = client.get_contact_by_email(email)
```
#### Get contact fields
```python
fields = client.get_contact_fields()
```
### Leads
#### Create Lead
```python
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
```python
webhooks = client.list_webhooks()
```
#### Create webhook
```python
webhook = client.create_webhook(event_type, url, event_identifiers: list = None, include_relations: list =None)
# event type options: "WEBHOOK.CONVERTED", "WEBHOOK.MARKED_OPPORTUNITY"
```
#### Delete webhook
```python
client.delete_webhook(uuid)
```

## 2. RD Station CRM
Check this site for more information: https://developers.rdstation.com/reference/instru%C3%A7%C3%B5es-e-requisitos
### Usage
```python
from rdstation.crm import CRMClient
client = CRMClient(token)
```
### Users
#### List users
```python
users = client.list_users()
```
### Contacts
#### List contacts
```python
contacts = client.list_contacts(page=None, limit=None, order=None, direction=None, email=None, query=None)
# limit: default is 20. Max is 200.
# order: field to be sorted. Default is 'name'
# direction: 'asc' or 'desc', defaulti is 'asc'
# email: filter by email
# query: name of contact to be searched"
```
#### Create Contact
```python
example = {
    "name": "juan python 3",
    "name": "contact name 3",
    "title": "3 title",
    "birthday": {"day": 11, "month": 9, "year": 1989},
    "emails": [{"email": "fulano@email.com.br"}],
    "phones": [{"phone": "71304556"}]
} 
custom_fields_example = [
    {
        "custom_field_id": "6414c0fc43ba490012f96c64",
        "value": "a text custom field"
    }
]
contact = client.create_contact(example, custom_fields_example)
```
### Companies
#### List companies
```python
companies = client.list_companies(page=None, limit=None, order=None, direction=None, user_id=None, query=None)
# limit: default is 20. Max is 200.
# order: field to be sorted. Default is 'name'
# direction: 'asc' or 'desc', defaulti is 'asc'
# query: name of company to be searched"
```
### Opportunities
#### List opportunities
```python
opportunities = client.list_opportunities(
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
)
```
#### Create opportunity
```python
#TODO: actualizar esto:
example = {
    "name": "juan python 3",
} 
custom_fields_example = [
    {
        "custom_field_id": "6414c0fc43ba490012f96c64",
        "value": "a text custom field"
    }
]
contact = client.create_contact(example, custom_fields_example)
```
#### List deal stages
```python
stages = client.list_deal_stages(page=None, limit=None)
```
#### List deal pipelines
```python
stages = client.list_deal_pipelines()
```
#### List deal sources
```python
stages = client.list_deal_sources()
```
### Custom fields
```python
fields = client.list_custom_fields(option=None)
# option: "contact", "deal", "organization"
```
