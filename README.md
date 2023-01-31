![](https://img.shields.io/badge/version-0.1.0-success) ![](https://img.shields.io/badge/code-Python-4B8BBE?logo=python&logoColor=white)
# rdstation-python

*rdstation-python* is an API wrapper for RD Station, written in Python.  
This library uses Oauth2 for authentication.
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
1. Get authorization URL:
```
url = client.authorization_url(redirect_uri)
```
2. Get access token using code
```
response = client.get_access_token(code)
```
3. Set access token
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
### LEADS
#### Create Lead
```
lead_example = {
    "event_type": "CONVERSION",
    "event_family": "CDP",
    "payload": {
        "conversion_identifier": "Name of the conversion event",
        "name": "Nome",
        "email": "email@email.com",
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
        "company_name": "company name",
        "company_site": "company website",
        "company_address": "company address",
        "tags": ["mql", "2022"],
        "available_for_mailing": True,
        "legal_bases": [{"category": "communications", "type": "consent", "status": "granted"}],
    }
}
created = client.create_deal(lead_example)
```

