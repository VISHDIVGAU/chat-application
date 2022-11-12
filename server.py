from concurrent import futures
import grpc
import time
import chat_pb2 as chat
import chat_pb2_grpc as rpc
import pymongo


class ChatServer(rpc.ChatServiceServicer): 
    def __init__(self):
        self.client = pymongo.MongoClient("127.0.0.1", 27017)
        self.db= self.client['ChatApplication']
        self.coll= self.db['UserChats']

    def ChatStream(self, request_iterator: chat.ChatId, context):
        lastindex = 0
        while True:
            chats= self.coll.find_one({'chat_id': request_iterator.chat_id})
            if chats != None:
                while len(chats['chat_history']) > lastindex:
                    data = chats['chat_history'][lastindex]
                    n= chat.Note()
                    n.name= data['name']
                    n.message= data['message']
                    n.chat_id= chats['chat_id']
                    lastindex += 1
                    yield n

    def SendNote(self, request: chat.Note, context):
        print("[{}] {}".format(request.name, request.message))
        saved_record= self.coll.find_one({'chat_id': request.chat_id})
        #print(request.chat_id)
        data= dict()
        data={
                'name': request.name,
                'message': request.message
                }
        if saved_record == None:
            record={
                    'chat_id': request.chat_id,
                    'chat_history': list()
                    }
            history=record['chat_history']
            history.append(data)
            self.coll.insert_one(record)
        else:
            history=saved_record['chat_history']
            history.append(data)
            self.coll.update_one({'chat_id': request.chat_id},
                    {
                        "$set": {
                            'chat_history': history
                            }
                        })
        #print(self.chats)
        return chat.Empty()


if __name__ == '__main__':
    port = 50051
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10)) 
    rpc.add_ChatServiceServicer_to_server(ChatServer(), server) 
    print('Starting server. Listening...')
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    while True:
        time.sleep(64 * 64 * 100)

