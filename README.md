```
 _______ _______ __   _ ______  ______  _______ _______      _______  _____  _____
 |______ |______ | \  | |     \ |_____] |______ |______      |_____| |_____]   |  
 ______| |______ |  \_| |_____/ |_____] |______ |______      |     | |       __|__
                                                                                  
                .' '.            __
       .        .   .           (__\_
        .         .         . -{{_(|8)
          ' .  . ' ' .  . '     (__/
```

# Sendbee Python API Client  

[![PyPI version](https://badge.fury.io/py/sendbee-api.svg)](https://badge.fury.io/py/sendbee-api)
[![Build Status](https://travis-ci.org/sendbee/sendbee-python-api-client.svg?branch=master)](https://travis-ci.org/sendbee/sendbee-python-api-client)

![GitHub issues](https://img.shields.io/github/issues/sendbee/sendbee-python-api-client.svg)
![GitHub closed issues](https://img.shields.io/github/issues-closed/sendbee/sendbee-python-api-client.svg)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/sendbee/sendbee-python-api-client.svg)

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sendbee-api.svg)
![GitHub](https://img.shields.io/github/license/sendbee/sendbee-python-api-client.svg?color=blue)
![GitHub last commit](https://img.shields.io/github/last-commit/sendbee/sendbee-python-api-client.svg?color=blue)

## Installation  

```bash
> pip install sendbee-api
```

## Usage  

### Initialization  

```python
from sendbee_api import SendbeeApi

api = SendbeeApi(
    '__your_api_key_here__', '__your_secret_key_here__',
    '__business_id_here__'
)
```

### Fetch contacts  

```python
contacts = api.contacts([tags=['...', ...]], [search_query='...'])

for contact in contacts:
    contact.id
    contact.name
    contact.phone
    contact.email
    contact.created_at
    contact.tags
```

### Subscribe contact  

```python
contact = api.subscribe_contact(phone='+...', [tags=['...', ...]])

contact.id
contact.name
contact.phone
contact.email
contact.created_at
contact.tags
```

### Fetch tags  

```python
tags = api.tags([name='...'])

for tag in tags:
    tag.id
    tag.name
```

### Create tag  

```python
tag = api.create_tag(name='...')

tag.id
tag.name
```

### Update tag  

```python
tag = api.update_tag(id='...', name='...')

tag.id
tag.name
```

### Delete tag  

```python
tag = api.delete_tag(id='...')
```

### Fetch message templates  

```python
templates = api.message_templates([search_query='...'])

for template in templates:
    template.id
    template.text
    template.tags
    template.keyword
    template.language
    template.approved
```

### Send template message  

```python
response = api.send_template_message(
    phone='+...', template_keyword='...', language='...', tags=['...', ...]
)

response.conversation_id
# save this id, and when you get sent message status requests on
# your webhook, you'll get this same id to identify the conversation

```

### Authenticate webhook request  

After you activate your webhook URL in Sendbee Dashboard, we will start sending requests on that URL depending which webhook type is linked for that webhook URL.  
Every request that we make will have authorization token ih header, like this:  

```
{
    ...
    'X-Authorization': '__auth_token_here__',
    ...
}
```

To authenticate requests that we make to your webhook URL, take this token from request header and check it using Sendbee API Client:  

```python
from sendbee_api import SendbeeApi

api = SendbeeApi('__your_api_key_here__', '__your_secret_key_here__')

token = '...'  # taken from the request header
if api.auth.check_auth_token(token):
    print('Weeee... Sendbee sent me the data on my webhook URL \o/ :)')
```  
