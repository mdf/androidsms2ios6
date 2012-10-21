# assumptions
#    one thread / chat per contact
#    numbers are gb
#    android db created with backup restore sms app
#    sms only
#    no attachments
#    random guids won't clash

import uuid
import sqlite3
import shutil


def make_guid():
    
    return str(uuid.uuid4()).upper()


def make_date(date):

    return int((date / 1000) - 978307200)


def make_canonical(phonenumber):
    
    if(phonenumber.startswith('+44')):
        return phonenumber
    else:
        return '+44' + phonenumber[1:]

def copy_ios_msg(db, row, handle):
    
    db.execute('insert into message(guid, \
                                     text, \
                                     replace, \
                                     service_center, \
                                     handle_id, \
                                     subject, \
                                     country, \
                                     attributedBody, \
                                     version, \
                                     type, \
                                     service, \
                                     account, \
                                     account_guid, \
                                     error, \
                                     date, \
                                     date_read, \
                                     date_delivered, \
                                     is_delivered, \
                                     is_finished, \
                                     is_emote, \
                                     is_from_me, \
                                     is_empty, \
                                     is_delayed, \
                                     is_auto_reply, \
                                     is_prepared, \
                                     is_read, \
                                     is_system_message, \
                                     is_sent, \
                                     has_dd_results, \
                                     is_service_message, \
                                     is_forward, \
                                     was_downgraded, \
                                     is_archive, \
                                     cache_has_attachments, \
                                     cache_roomnames, \
                                     was_data_detected, \
                                     was_deduplicated) \
                                     values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, \
                                     ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, \
                                     ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, \
                                     ?, ?, ?, ?, ?, ?, ?)',
                                     (row['guid'], #guid
                                     row['text'], #text
                                     row['replace'], #replace
                                     row['service_center'], #service_center
                                     handle, #handle_id
                                     row['subject'], #subject
                                     row['country'], #country
                                     row['attributedBody'], #attributedBody
                                     row['version'], #version
                                     row['type'], #type
                                     row['service'], #service
                                     row['account'], #account
                                     row['account_guid'], #account_guid
                                     row['error'], #error
                                     row['date'], #date
                                     row['date_read'], #date_read
                                     row['date_delivered'], #date_delivered
                                     row['is_delivered'], #is_delivered
                                     row['is_finished'], #is_finished
                                     row['is_emote'], #is_emote
                                     row['is_from_me'], #is_from_me
                                     row['is_empty'], #is_empty
                                     row['is_delayed'], #is_delayed
                                     row['is_auto_reply'], #is_auto_reply
                                     row['is_prepared'], #is_prepared
                                     row['is_read'], #is_read
                                     row['is_system_message'], #is_system_message
                                     row['is_sent'], #is_sent
                                     row['has_dd_results'], #has_dd_results
                                     row['is_service_message'], #is_service_message
                                     row['is_forward'], #is_forward
                                     row['was_downgraded'], #was_downgraded
                                     row['is_archive'], #is_archive
                                     row['cache_has_attachments'], #cache_has_attachments
                                     row['cache_roomnames'], #cache_roomnames
                                     row['was_data_detected'], #was_data_detected
                                     row['was_deduplicated'])) #was_deduplicated
    return db.lastrowid

def insert_android_msg(db, guid, date, body, handle, is_delivered, is_from_me, is_read, is_sent, account, account_guid):
    
    db.execute('insert into message(guid, \
                                     text, \
                                     replace, \
                                     service_center, \
                                     handle_id, \
                                     subject, \
                                     country, \
                                     attributedBody, \
                                     version, \
                                     type, \
                                     service, \
                                     account, \
                                     account_guid, \
                                     error, \
                                     date, \
                                     date_read, \
                                     date_delivered, \
                                     is_delivered, \
                                     is_finished, \
                                     is_emote, \
                                     is_from_me, \
                                     is_empty, \
                                     is_delayed, \
                                     is_auto_reply, \
                                     is_prepared, \
                                     is_read, \
                                     is_system_message, \
                                     is_sent, \
                                     has_dd_results, \
                                     is_service_message, \
                                     is_forward, \
                                     was_downgraded, \
                                     is_archive, \
                                     cache_has_attachments, \
                                     cache_roomnames, \
                                     was_data_detected, \
                                     was_deduplicated) \
                                     values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, \
                                     ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, \
                                     ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, \
                                     ?, ?, ?, ?, ?, ?, ?)',
                                     (guid, #guid
                                     body, #text
                                     0, #replace
                                     None, #service_center
                                     handle, #handle_id
                                     None, #subject
                                     None, #country
                                     None, #attributedBody
                                     10, #version
                                     0, #type
                                     "SMS", #service
                                     account, #account
                                     account_guid, #account_guid
                                     0, #error
                                     date, #date
                                     date, #date_read
                                     date, #date_delivered
                                     is_delivered, #is_delivered
                                     1, #is_finished
                                     0, #is_emote
                                     is_from_me, #is_from_me
                                     0, #is_empty
                                     0, #is_delayed
                                     0, #is_auto_reply
                                     0, #is_prepared
                                     is_read, #is_read
                                     0, #is_system_message
                                     is_sent, #is_sent
                                     0, #has_dd_results
                                     0, #is_service_message
                                     0, #is_forward
                                     0, #was_downgraded
                                     0, #is_archive
                                     0, #cache_has_attachments
                                     None, #cache_roomnames
                                     1, #was_data_detected
                                     0)) #was_deduplicated
    return db.lastrowid


def get_handle(db, address, uncanonical_address):
    
    # do we have a handle
    db.execute('select ROWID from handle where id = ?', (address,))
    res = db.fetchone()
    
    if(res == None):
        # add handle
        db.execute('insert into handle(id, country, service, uncanonicalized_id) \
            values(?, ?, ?, ?)',
            (address, None, 'SMS', uncanonical_address))
        handle = db.lastrowid
        print("new handle %d" % handle)
    else:
        # existing handle
        handle = res[0]
        print("got handle %d" % handle)
        
    return handle


def get_chat(db, address, account_guid, account_login):
        
    # do we have a chat
    db.execute('select ROWID from chat where chat_identifier = ?', (address,))
    res = db.fetchone()
    
    if(res == None):
        # add a chat
        chat_guid = "SMS;-;" + address
        db.execute('insert into chat(guid, \
                                      style, \
                                      state, \
                                      account_id, \
                                      properties, \
                                      chat_identifier, \
                                      service_name, \
                                      room_name, \
                                      account_login, \
                                      is_archived, \
                                      last_addressed_handle) \
                                      values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                                      (chat_guid, #guid
                                      45, #style
                                      3, #state
                                      account_guid, #account_id
                                      None, #properties
                                      address, #chat_identifier
                                      "SMS", #service_name
                                      None, #room_name
                                      account_login, #account_login
                                      0, #is_archived
                                      None)) #last_addressed_handle
        chat_id = db.lastrowid
        print("new chat %d" % chat_id)
    else:
        # existing chat
        chat_id = res[0]
        print("got chat %d" % chat_id)
    
    return chat_id

    
def join_chat_handle(db, chat_id, handle_id):
    
    db.execute('select ROWID from chat_handle_join where handle_id = ? ', (handle_id,))
    res = db.fetchone()
    
    if(res == None):
        db.execute('insert into chat_handle_join(chat_id, handle_id) values(?,?)',
                    (chat_id, handle_id))


def join_chat_message(db, chat_id, msg_id):
    
    # join chat and msg
    db.execute('insert into chat_message_join(chat_id, message_id) values(?,?)',
                (chat_id, msg_id))

#3d0d7e5fb2ce288813306e4d4636395e047a3d28
shutil.copy2('ios_org.db', 'ios_new.db')
 
androidDb = sqlite3.connect('android.db')
androidDb.row_factory = sqlite3.Row
android = androidDb.cursor()

iosDb = sqlite3.connect('ios_new.db')
iosDb.isolation_level = None
ios = iosDb.cursor()

# delete old messages
ios.execute('delete from message')
ios.execute('delete from chat')
ios.execute('delete from handle')
ios.execute('delete from chat_handle_join')
ios.execute('delete from chat_message_join')
ios.execute('update sqlite_sequence set seq=0 where name in ("handle", "chat", "message")')

iosDbOrg = sqlite3.connect('ios_org.db')
iosDbOrg.row_factory = sqlite3.Row
iosOrg = iosDbOrg.cursor()

iosOrg.execute('select * from message')
res = iosOrg.fetchone()

account = res['account']

iosOrg.execute('select * from chat')
res = iosOrg.fetchone()

account_guid = res['account_id']
account_login = res['account_login']

android.execute('select * from smstable')
msgs = android.fetchall()

for msg in msgs:

    guid = make_guid()
    date = make_date(msg['date'])
    body = msg['body']
    address = make_canonical(msg['address'])
    uncanonical_address = msg['address']
    
    # 1 = received, 2 = sent, 5 = not sent
    if(msg['type']==1):
        is_delivered = 1
        is_from_me = 0
        is_read = 1
        is_sent = 0
    elif(msg['type']==2):
        is_delivered = 0
        is_from_me = 1
        is_read = 0
        is_sent = 1
    else:
        continue
    
    # get handle
    handle = get_handle(ios, address, uncanonical_address)

    # get chat
    chat_id = get_chat(ios, address, account_guid, account_login)

    # join chat and handle
    join_chat_handle(ios, chat_id, handle)
    
    # insert msg
    msg_id = insert_android_msg(ios, guid, date, body, handle, is_delivered, is_from_me, is_read, is_sent, account, account_guid)
    
    # join chat and message
    join_chat_message(ios, chat_id, msg_id)
    

android.close()

# copy ios messages
iosOrg.execute('select * from message')
msgs = iosOrg.fetchall()

for msg in msgs:

    # lookup handle in original db
    iosOrg.execute('select * from handle where ROWID = ?', (msg['handle_id'],))
    res = iosOrg.fetchone()
    
    if(res == None):
        print("could not find ios handle?")
        continue
    
    address = res['id']
    uncanonical_address = res['uncanonicalized_id']
    
    # get handle
    handle = get_handle(ios, address, uncanonical_address)

    # get chat
    chat_id = get_chat(ios, address, account_guid, account_login)

    # join chat and handle
    join_chat_handle(ios, chat_id, handle)
    
    # insert msg
    msg_id = copy_ios_msg(ios, msg, handle)
    
    # join chat and message
    join_chat_message(ios, chat_id, msg_id)


#close dbs
ios.close()
iosOrg.close()

print('done')

