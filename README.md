# Sendbee Python API Client  

```

                .' '.            __
       .        .   .           (__\_
        .         .         . -{{_(|8)
          ' .  . ' ' .  . '     (__/

```  

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
    contact.status
    contact.folder
    contact.created_at
    
    contact.name
    contact.phone
    contact.email
    contact.twitter_link
    contact.facebook_link
    
    for tag in contact.tags:
        tag.id
        tag.name
    
    for note in contact.notes:
        note.value
    
    for custom_field in contact.custom_fields:
        custom_field.key
        custom_field.value
```

### Subscribe contact  

```python
contact = api.subscribe_contact(
    phone='+...',
    # this is mandatory the most important information
    # about the subscribing contact
    
    [tags=['...', ...]], 
    # tag new contact
    # if tag doesn't exist, it will be created
    
    [name='...'], [email='...'],
    [facebook_link='...'],[twitter_link='...'],
    [address={
        'line': '...',
        'city': '...',
        'postal_code': '...'
    }],
    
    [notes=[...]], 
    # write notes about your new subscriber
    
    [custom_fields={'__field_name__': '__field_value__', ...}],
    # fill custom fields with your data (value part)
    # custom fields must be pre-created in Sendbee Dashboard
    # any non-existent field will be ignored 
    
    [block_notifications=[True|False]],
    # prevent sending browser push notification and email 
    # notification to agents, when new contact subscribes
    # (default is True) 
    
    [block_automation=[True|False]]
    # prevent sending automated template messages to newly
    # subscribed contact (if any is set in Sendbee Dashboard) 
    # (default is True) 
)

contact.id
contact.status
contact.folder
contact.created_at

contact.name
contact.phone
contact.email
contact.twitter_link
contact.facebook_link

for tag in contact.tags:
    tag.id
    tag.name

for note in contact.notes:
    note.value

for custom_field in contact.custom_fields:
    custom_field.key
    custom_field.value
```

### Update contact  

```python
contact = api.update_contact(
    id='...',
    # contact is identified with ID
    
    [phone='+...'],
    # this is the most important information 
    # about the subscribing contact
    
    [tags=['...', ...]], 
    # tag new contact
    # if tag doesn't exist, it will be created
    
    [name='...'], [email='...'],
    [facebook_link='...'],[twitter_link='...'],
    [address={
        'line': '...',
        'city': '...',
        'postal_code': '...'
    }],
    
    [notes=[...]], 
    # write notes about your new subscriber
    # if there are notes already saved for this contact
    # new notes will be appended
    
    [custom_fields={'__field_name__': '__field_value__', ...}],
    # fill custom fields with your data (value part)
    # custom fields must be pre-created in Sendbee Dashboard
    # any non-existent field will be ignored 
    # if there are fields already filled with data for this contact
    # it will be overwritten with new data 
)

contact.id
contact.status
contact.folder
contact.created_at

contact.name
contact.phone
contact.email
contact.twitter_link
contact.facebook_link

for tag in contact.tags:
    tag.id
    tag.name

for note in contact.notes:
    note.value

for custom_field in contact.custom_fields:
    custom_field.key
    custom_field.value
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
response = api.delete_tag(id='...')

response.message
```

### Fetch custom fields  

```python
custom_fields = api.custom_fields([search_query='...'])

for custom_field in custom_fields:
    custom_field.slug
    custom_field.name
    custom_field.type
```

### Create custom field  

```python
custom_field = api.create_custom_field(
    name='...', type='text|number|list|date|boolean'
)

custom_field.slug
custom_field.name
custom_field.type
```

### Update custom field  

```python
custom_field = api.update_custom_field(
    slug='...', [name='...'], [type='text|number|list|date|boolean']
)

custom_field.slug
custom_field.name
custom_field.type
```

### Delete custom field  

```python
response = api.delete_custom_field(slug='...')

response.message
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
    phone='+...',
    
    template_keyword='...',
    # every pre-created and approved message template
    # is identified with a keyword
    
    language='...', 
    # language keyword
    # example: en (for english)
    
    tags={'__tag_key__': '__tag_value__', ...}
    # tags for template messages are parts of the message that need
    # to be filled with your custom data
    # example:
    # template message: "Welcome {name}! How can we help you?"
    # tags: {"name": contact.name}
)

response.conversation_id
# save this id, and when you get sent message status requests on
# your webhook, you'll get this same id to identify the conversation

```

### Authenticate webhook request  

After activating your webhook URL in Sendbee Dashboard, we will start sending requests on that URL depending on which webhook type is linked with that webhook URL.  
Every request that we make will have authorization token in header, like this:  

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
