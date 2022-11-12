import pymongo
import random



class CService():
    def __init__(self):
        self.client = pymongo.MongoClient("127.0.0.1", 27017)
        self.db= self.client['ChatApplication']
        self.coll= self.db['UserDetails']

    def getUserslist(self, email):
        records= self.coll.find()
        user= list()
        for record in records:
            if record['email'] != email:
                user.append(record)
        return user

    def getChatId(self, sender, receiver):
        chatcol= self.db['chatId']
        record= chatcol.find_one({'sender': sender, 'receiver': receiver})
        if record == None:
            chat_id= random.random()
            record= {
                    'sender': sender,
                    'receiver': receiver,
                    'chat_id': chat_id
                    }
            record1={
                    'sender': receiver,
                    'receiver': sender,
                    'chat_id': chat_id
                    }
            chatcol.insert_one(record)
            chatcol.insert_one(record1)
            return chat_id
        else:
            return record['chat_id']





