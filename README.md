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
If your access token expired, you can get a new one using refresh_token:
```
response = client.refresh_access_token(refresh_token)
```
And then set access token again...
Check more information about RD Station Oauth: https://legacydevelopers.rdstation.com/es/authentication
#### Get account info
```
info = client.get_account_info()
```

