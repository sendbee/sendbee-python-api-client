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

## Table of contents  

-   [Installation](#installation)  
-   [Initialization](#initialization)    

#### Contacts  

-   [Fetch contacts](#fetch-contacts)  
-   [Subscribe contact](#subscribe-contact)  
-   [Update contact](#update-contact)  

#### Contact Tags  

-   [Fetch tags](#fetch-tags)  
-   [Create tag](#create-tag)  
-   [Update tag](#update-tag)  
-   [Delete tag](#delete-tag)  

#### Custom Fields  

-   [Fetch custom fields](#fetch-custom-fields)  
-   [Create custom field](#create-custom-field)  
-   [Update custom field](#update-custom-field)  
-   [Delete custom field](#delete-custom-field)  

#### Messages  

-   [Fetch message templates](#fetch-message-templates)  
-   [Send template message](#send-template-message)  
-   [Send message](#send-message)  

#### Automation  

-   [Toggle bot for conversation with contact on off](#Toggle-bot-for-conversation-with-contact-on-off)  

#### Mics  

-   [Exception handling](#exception-handling)  
-   [Authenticate webhook request](#authenticate-webhook-request)  
-   [Warnings](#warnings)  
-   [Debugging](#debugging)  

## <a href='installation'>Installation</a>  

```bash
> pip install sendbee-api
```

## Usage  

### <a href='initialization'>Initialization</a>  

```python
from sendbee_api import SendbeeApi

api = SendbeeApi(
    '__your_api_key_here__', '__your_secret_key_here__',
    '__business_id_here__'
)
```

### <a href='fetch-contacts'>Fetch contacts</a>  

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

### <a href='subscribe-contact'>Subscribe contact</a>  

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

### <a href='update-contact'>Update contact</a>  

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

### <a href='fetch-tags'>Fetch tags</a>  

```python
tags = api.tags([name='...'])

for tag in tags:
    tag.id
    tag.name
```

### <a href='create-tag'>Create tag</a>  

```python
tag = api.create_tag(name='...')

tag.id
tag.name
```

### <a href='update-tag'>Update tag</a>  

```python
tag = api.update_tag(id='...', name='...')

tag.id
tag.name
```

### <a href='update-tag'>Update tag</a>  

```python
response = api.delete_tag(id='...')

response.message
```

### <a href='fetch-custom-fields'>Fetch custom fields</a>  

```python
custom_fields = api.custom_fields([search_query='...'])

for custom_field in custom_fields:
    custom_field.slug
    custom_field.name
    custom_field.type
```

### <a href='create-custom-field'>Create custom field</a>  

```python
custom_field = api.create_custom_field(
    name='...', type='text|number|list|date|boolean'
)

custom_field.slug
custom_field.name
custom_field.type
```

### <a href='update-custom-field'>Update custom field</a>  

```python
custom_field = api.update_custom_field(
    slug='...', [name='...'], [type='text|number|list|date|boolean']
)

custom_field.slug
custom_field.name
custom_field.type
```

### <a href='delete-custom-field'>Delete custom field</a>  

```python
response = api.delete_custom_field(slug='...')

response.message
```

### <a href='fetch-message-templates'>Fetch message templates</a>  

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

### <a href='send-template-message'>Send template message</a>  

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

### <a href='send-message'>Send message</a>  

You can send either text message or media message.  
For media message, following formats are supported:  
Audio: AAC, M4A, AMR, MP3, OGG OPUS  
video: MP4, 3GPP  
Image: JPG/JPEG, PNG  
Documents: PDF, DOC, DOCX, PPT, PPTX, XLS, XLSX  

```python
response = api.send_message(
    phone='+...',
    
    [text='...'],
    # any kind of message text
    
    [media_url='...']
    # URL to a media. 
    # you need to upload it your self and send us the URL
)

response.conversation_id
# save this id, and when you get sent message status requests on
# your webhook, you'll get this same id to identify the conversation

```

### <a href='toggle-bot-for-conversation-with-contact-on-off'>Toggle bot for conversation with contact on off</a>  

Every contact is linked with conversation with an agent.  
Conversation could be handled by an agent or a bot (automation).  
Every time a message has been sent to a contact by an agent or using the API, the bot is automatically turned off for that conversation.  
But there is always a use case when you need to turn it on or off manually.  

```python
api.bot_on(contact_id='...')
api.bot_off(contact_id='...')
```

### <a href='exception-handling'>Exception handling</a>  

Every time something is not as it should be, like parameter is missing, parameter value is invalid, authentication fails, etc, API returns a http status code accordingly and an error message.  
By using this client library, an error message is detected and taken, and an exception is raised, so you can handle it like this:  

```python
from sendbee_api import SendbeeRequestApiException

try:
    api.send_template_message(...)
except SendbeeRequestApiException as e:
    print(e)
```    

### <a href='authenticate-webhook-request'>Authenticate webhook request</a>  

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

### <a href='warnings'>Warnings</a>  

Sometimes APi returns a worning so you could be warned about something.  
The waning is displayed in standard output:  

![Debugging](docs/images/warning.png)  

### <a href='debugging'>Debugging</a>  

This library has it's own internal debugging tool.  
By default it is disabled, and to enable it, pass the `debug` parameter:  

```python
from sendbee_api import SendbeeApi

api = SendbeeApi(
    '__your_api_key_here__', '__your_secret_key_here__',
    '__business_id_here__', debug=True
)
```  

Once you enabled the internal debug tool, every request to API will output various request and response data in standard output:  

![Debugging](docs/images/debugging.png)   
