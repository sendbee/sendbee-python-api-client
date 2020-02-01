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

## Installation  

```bash
> pip install sendbee_api  
# not on pypi right now, but will be 

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
contacts = api.contacts([tags=["...", ...]], [search_query="..."])

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
contact = api.subscribe_contact(phone='+...', [tags=["...", ...]])

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
response = api.send_template_message(id='...', name='...')

response.conversation_id
# save this id, and when you get sent message status requests on
# your webhook, you'll get this same id to identify the conversation

```
