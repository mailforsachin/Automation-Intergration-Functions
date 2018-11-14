from pymongo import MongoClient
import datetime, ssl

#connection_string = 'mongodb://serivice-desk-store:pMzmGDeCcbMZEJ7hVirY9YEA7NMm6abpGF6oNz32D6MNTqsmdqzvdg3MLVw80eMlztxPP03vxsKxtatgPOiCFg==@serivice-desk-store.documents.azure.com:10255/?ssl=true&replicaSet=globaldb'

connection_string = 'mongodb://hodor:vEhB8bzn4I1FZqvmpTJMB8VIhVdj7DTqWQdYiLVg0sBIbyjQWGU59aaCzOocj79xyIxYy9qRviComqJmSbOtwA==@hodor.documents.azure.com:10255/?replicaSet=globaldb'

client = MongoClient(connection_string, ssl=True, ssl_cert_reqs=ssl.CERT_NONE)
db = client.hodor

def startConversation(data):
    timestamp = datetime.datetime.utcnow()
    msg = {
        'user': data['user_name'],
        'text': data['message'],
        'timestamp': timestamp
    }
    doc = {
        '_id':data['callsid'],
        'phone_number': data['phone_number'],
        'chat': [msg],
        'timestamp': timestamp,
        'status': "on"
    }

    conversations = db.conversations
    return conversations.insert_one(doc).inserted_id

def logMessage(data):
    timestamp = datetime.datetime.utcnow()

    msg = {
        'user': data['user_name'],
        'text': data['message'],
        'timestamp': timestamp
    }
    conversations = db.conversations
    conversations.update({"_id":data['callsid'] }, {"$push": {"chat": msg}})


def endConversation(data):
    timestamp = datetime.datetime.utcnow()
    newDoc = {
        'status':'ended',
        'end_timestamp': timestamp
    }
    conversations = db.conversations
    conversations.update({"_id":data['callsid'] }, {'$set':newDoc})

fx = {
    'startConversation': startConversation,
    'logMessage': logMessage,
    'endConversation': endConversation
}