import smtplib 
import queue
from email.message import EmailMessage

class EmailClient:

    def __init__(self, server_name=None, port=None, start_session=False):
        self.server = None
        self.server_name = server_name
        self.server_port = port
        self.sender_address = None
        self.msg_queue = queue.Queue()

        if start_session:
            self.start(self.server_name, self.server_port)
                
    def set_server_name(self, name):
        print("Set server name = " + name)
        self.server_name = name

    def set_port(self, port):
        print("Set port = " + str(port))
        self.server_port = port

    def start(self, name=None, port=None):
        print('Starting up server...')
        if name is not None and port is not None:    
            self.server = smtplib.SMTP("smtp." + name, port)
            self.server_name = name
            self.server_port = port
        elif self.server_name is not None and self.server_port is not None:
            self.server = smtplib.SMTP("smtp." + self.server_name, self.server_port)
        else:
            print("Can't start due to missing server name and/or port")      
            return      
        self.server.ehlo()
        self.server.starttls()

    def shutdown(self):
        self.server = None  
        print("Shutting down server...")

    def session_started(self):
        return self.server is not None

    def login(self, email, password):
        self.server.login(email, password)
        print("Logged in as "+email)

    def create_msg(self, subject, body, recipients):
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = self.sender_address
        msg['To'] = recipients
        msg.set_content(body)
        print('Message with subject "' +subject+ '" created')
        return msg

    def enqueue_msg(self, email_msg):
        self.msg_queue.put(email_msg)

    def clear_msg_queue(self):
        self.msg_queue = queue.Queue()

    def get_msg_queue_size():
        return self.msg_queue.qsize()

    def is_msg_queue_full(self):
        return self.msg_queue.full()

    def is_msg_queue_empty(self):
        return self.msg_queue.empty()

    def send_queue(self, number=None):
        if number is None:
            print("Attemping to send all "+ str(self.msg_queue.qsize()) + " messages from the queue...")
            while self.msg_queue.empty() is False:
                self._send(self.msg_queue.get())
        else:
            try:
                int(number)
            except:
                print("Can't send. The number of messages to be sent must be an integer")
                return

            if number < 1:
                print("Can't send. The number of messages to be sent must be > 0")
                return

            print("Attemping to send "+ str(number) +" messages from the queue...")
            for i in range(number):
                if self.msg_queue.empty() is False:
                    self._send(self.msg_queue.get())

    def send_msg_obj(self, msg):
        self._send(msg)

    def send_msg(self, subject, body, recipients):
        msg = self.create_msg(subject, body, recipients)
        self._send(msg)

    def _send(self, msg):
        self.server.send_message(msg)
        print('Message with subject "'+msg['Subject']+'" sent')
