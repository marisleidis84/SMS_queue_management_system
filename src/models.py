import os
from twilio.rest import Client

class Queue:
    def __init__(self):
        self.account_sid = os.environ['TWILIO_ACCOUNT_SID'] # Definir sid
        self.auth_token = os.environ['TWILIO_AUTH_TOKEN']
        self.client = Client(self.account_sid, self.auth_token) #Ceando instancia de cliente
        self._queue = []
        self._mode = 'FIFO'

    def enqueue(self, item):
        self._queue.append(item)
        message = self.client.messages.create(
                body='Welcome,' + str(item['name']) + 'You will be attended after of' + str(self.size()) +' '+ 'persons!!',
                from_='+15182174741',
                to=str(item['phone'])
            )

        print(message.sid)      

    def dequeue(self):
        if self.size() > 0:
            if self._mode == 'FIFO':
                item = self._queue.pop(-1)
                return item
            elif self._mode == 'LIFO':
                item = self._queue.pop()
                return item
        else:
            msg = {
                "msg": "Fila sin elementos"
            }
            return msg

    def get_queue(self):
        return self._queue

    def size(self):
        return len(self._queue)