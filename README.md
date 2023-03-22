# rdstation-python
![](https://img.shields.io/badge/version-0.2.0-success) ![](https://img.shields.io/badge/Python-3.8%20|%203.9%20|%203.10%20|%203.11-4B8BBE?logo=python&logoColor=white)  

*rdstation-python* is an API wrapper for RD Station, written in Python.
1. [RD Station Marketing](#1-rd-station-marketing) (This product uses Oauth2 for authentication and uses webhook notifications). 
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
    "personal_phone": "phone of the contact",
    "website": "website of the contact",
    "cf_custom_field_api_identifier": "custom field value",
    "company_name": "company name",
    "client_tracking_id": "lead tracking client_id",
    "traffic_source": "Google",
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
#### - List users
```python
users = client.list_users()
```
### Contacts
#### - List contacts
```python
contacts = client.list_contacts(page=None, limit=None, order=None, direction=None, email=None, query=None)
# limit: default is 20. Max is 200.
# order: field to be sorted. Default is 'name'
# direction: 'asc' or 'desc', defaulti is 'asc'
# email: filter by email
# query: name of contact to be searched"
```
#### - Create Contact
```python
custom_fields = [
    {
        "custom_field_id": "6414c0fc43ba490012f96c64",
        "value": "a text custom field"
    }
]
contact = client.create_contact("contact X", "Mr", "1991-01-04", "test@test.com", custom_data=custom_fields)
```
### Companies
#### - List companies
```python
companies = client.list_companies(page=None, limit=None, order=None, direction=None, user_id=None, query=None)
# limit: default is 20. Max is 200.
# order: field to be sorted. Default is 'name'
# direction: 'asc' or 'desc', defaulti is 'asc'
# query: name of company to be searched"
```
### Opportunities
#### - List opportunities
```python
opportunities = client.list_opportunities(limit=1, page=1, direction="desc")
```
#### - Create opportunity
```python
custom_fields_example = [
    {
        "custom_field_id": "6414c0fc43ba490012f96c64",
        "value": "a text custom field"
    }
]
oppor = client.create_opportunity(
    "opportunity name 2023",
    deal_stage_id="64148f7bff9080001bdca349",
    organization_id="6414cc9895c34b000c0fb2aa",
    deal_source_id="64148f7bff9080001bdca33b",
    rating=4,
    prediction_date="2023-11-11",
    custom_data=custom_fields_example,
)
```
Check this site for more information about creating opportunities: https://developers.rdstation.com/reference/oportunidades
#### - List deal stages
```python
stages = client.list_deal_stages(page=None, limit=None)
```
#### - List deal pipelines
```python
stages = client.list_deal_pipelines()
```
#### - List deal sources
```python
stages = client.list_deal_sources()
```
### Custom fields
#### - List custom fields
```python
fields = client.list_custom_fields(option=None)
# option: "contact", "deal", "organization"
```
