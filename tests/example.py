from sendbee_api import SendbeeApi, SendbeeRequestApiException

#if True:
if False:
    SendbeeApi.base_url = 'dashboard-api-dev.sendbee.io:4010'
    api = SendbeeApi('2hXaZ3ZbnrDKrKj84kIq',
                     'zodux3ITAPW4cGsvn6rGbLEAgRNLphPJ7OF121nl', debug=True)

if True:
#if False:
    SendbeeApi.base_url = '127.0.0.1:8010'
    SendbeeApi.protocol = 'http'
    api = SendbeeApi('ocDZzVs7rYIUdcpb4luY',
                     'vilgNdQrptFYoSWFGYWt9uUruS8dtX6tECJYbadB', debug=True)

#if True:
if False:
    api = SendbeeApi(
        '0NYMTmdOb8cc5hruEmEP', # bawa
        'JVZh2y3TZ9r03EKl7yovjDjrVMMXJ1PbwdBXRZZQ', debug=True
    )

#if True:
if False:
    contacts = api.contacts(status='subscribed')
    for contact in contacts:
        print()
        print(contact.id)
        print(contact.status)
        print(contact.folder)
        print(contact.created_at)
        print()
        print(contact.name)
        print(contact.phone)
        print()

        for tag in contact.tags:
            print('   ' + tag.id)
            print('   ' + tag.name)
        print()
        for note in contact.notes:
            print('   ' + str(note.value))
        print()
        for contact_field in contact.contact_fields:
            print('   ' + contact_field.key)
            print('   ' + contact_field.value)
        print('----------')

#if True:
if False:
    """contact_field = api.create_contact_field(name='lala2',
                                             type='list', options=['opt3', 'opt4'])
    print(contact_field.id, contact_field.type,
          contact_field.name, contact_field.options)"""

    contact_field = api.update_contact_field(id='6652c031-0fee-42e1-bf7e-b2b667c960a1', name='lala',
                                             type='list', options=['opt1', 'opt2', 'opt3'])
    print(contact_field.id, contact_field.type,
          contact_field.name, contact_field.options)

    """print(api.delete_contact_field(id=contact_field.id).message)"""


#if True:
if False:
    contact_fields = api.contact_fields()
    for contact_field in contact_fields:
        print(contact_field.id, contact_field.type,
              contact_field.name, contact_field.options)

#if True:
if False:
    tags = api.tags()
    for tag in tags:
        print(tag.name)

#if True:
if False:
    contact = api.subscribe_contact(
    #contact = api.update_contact(
        #id='2a103292-b4ff-4ca5-b7b7-235ecf579164',
        phone='+385993037744',
        #tags=['TagTest2'],
        name='Ivan',
        #contact_fields={
        #    'email': 'pajo3@patak.com',
        #    'student id': '12333333',
        #    'lala': 'opt2',
        #    'kustom': '321333333',
        #    'bla cla': 'no',
        #    'bla': 'bla2',
        #    'test': 'ggggggggg',
        #},
        #notes=['not3333333']
    )
    print()
    print(contact.id)
    print(contact.status)
    print(contact.folder)
    print(contact.created_at)
    print()
    print(contact.name)
    print(contact.phone)
    print()

    for tag in contact.tags:
        print('   ' + tag.id)
        print('   ' + tag.name)
    print()
    for note in contact.notes:
        print('   ' + str(note.value))
    print()
    for contact_field in contact.contact_fields:
        print('   ' + contact_field.key)
        print('   ' + contact_field.value)
    print('----------')

#if True:
if False:
    try:
        templates = api.message_templates(approved=True)
        for template in templates:
            print(template.keyword)
            print(template.language)
            for tag in template.tags:
                print(tag.name)
    except SendbeeRequestApiException as e:
        print(e)
        print()

#if True:
if False:
    response = api.send_template_message(
        phone='+385993037744',
        template_keyword='order_dispatched',
        language='hr_HR',
        tags={1: ' foo ', 2: ' bar '},
        prevent_bot_off=True,
        agent_id='d5ca1075-2004-44c5-81d8-3590ba243b75'
    )
    print(response.conversation_id)
    print()

    """response = api.send_template_message(
        phone='+385993037744',
        template_keyword='statement_ready_new',
        language='en',
        tags={"1": "test","2": "test","3": "test","4": "test","5": "test"}
    )
    print(response.conversation_id)"""

#if True:
if False:
    response = api.send_message(
        phone='+385993037744',
        text='test',
        #media_url='https://sendbee.io/images/sendbee-social.png',
        #media_url='https://sendbee-dev.s3.amazonaws.com/chat-media/b4176198-40f8-43b9-af1b-7e4a0be29154/sample.pdf',
        prevent_bot_off=True,
        agent_id='940e92c2-2f13-4012-97d0-f8289c62c20b'
    )
    print(response.conversation_id, response.status)

#if True:
if False:
    try:
        response = api.chatbot_activity(conversation_id='37a5fed6-1c9e-459a-a0e9-5192753c5131', active=False)
        print(response.message)
    except Exception as e:
        print(e)


#if True:
if False:
    bot_activity = api.chatbot_activity_status(conversation_id='df4828ed-272e-4b3e-abbc-23a40a988f61')
    print(bot_activity.conversation_id, bot_activity.chatbot_active)


#if True:
if False:
    conversations = api.conversations()
    for conversation in conversations:
        print(conversation.id)
        # print(conversation.folder)
        # print(conversation.chatbot_active)
        # print(conversation.platform)
        # print(conversation.created_at)
        # print(conversation.contact.id)
        # print(conversation.contact.name)
        # print(conversation.contact.phone)
        # print(conversation.last_message.direction)
        # print(conversation.last_message.status)
        # print(conversation.last_message.inbound_sent_at)
        # print(conversation.last_message.outbound_sent_at)
        # print()

    print(conversations.has_next())

#if True:
if False:
    for i in range(1,3):
        messages = api.messages(conversation_id='b4176198-40f8-43b9-af1b-7e4a0be29154', page=i)
        for message in messages:
            print(message.body)
            """print(message.media_type)
            print(message.media_url)
            print(message.status)
            print(message.direction)
            print(message.sent_at)
            print()"""
        print('=========')


#if True:
if False:
    teams = api.teams(member_id='e590ef16-2b28-4c61-9192-345b19b98d58')
    for team in teams:
        print(team.id, team.name)
        for member in team.members:
            print('    ', member.id, member.name, member.role)
        print()


if True:
#if False:
    members = api.members(team_id='a0049772-ce46-48d9-994d-024ca255703c')
    for member in members:
        print(member.id, member.name, member.role)
        for team in member.teams:
            print('    ', team.id, team.name)
        print()
