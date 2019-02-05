import email, smtplib, imaplib, queue, datetime
from email.message import EmailMessage

class EmailClient:

    def __init__(self, server_name=None, port=None, start_session=False):
        self.smtp_conn = None
        self.imap_conn = None
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
            self.smtp_conn = smtplib.SMTP("smtp." + name, port)
            self.imap_conn = imaplib.IMAP4_SSL("imap." + name)
            self.server_name = name
            self.server_port = port
        elif self.server_name is not None and self.server_port is not None:
            self.smtp_conn = smtplib.SMTP("smtp." + self.server_name, self.server_port)
            self.imap_conn = imaplib.IMAP4_SSL("imap." + self.server_name)
        else:
            print("Can't start due to missing server name and/or port")      
            return      
        self.smtp_conn.ehlo()
        self.smtp_conn.starttls()

    def restart(self):
        self.start()

    def shutdown(self):
        print("Shutting down server...")
        self.smtp_conn.quit()
        self.smtp_conn = None
        self.imap_conn.logout()
        self.imap_conn = None

    def session_started(self):
        return self.smtp_conn is not None and self.imap_conn is not None

    def login(self, email, password):
        self.smtp_conn.login(email, password)
        self.imap_conn.login(email, password)
        print("Logged in as "+email)

    def get_inbox(self, scope='ALL'):
        inbox = list()
        selected = self.imap_conn.select('INBOX')
        result, data = self.imap_conn.uid('search', None, scope)
        num_messages = len(data[0].split())

        for x in range(num_messages):
            latest_email_uid = data[0].split()[x]
            result, email_data = self.imap_conn.uid('fetch', latest_email_uid, '(RFC822)')

            raw_email = email_data[0][1]
            raw_email_string = raw_email.decode('utf-8')
            email_message = email.message_from_string(raw_email_string)

            msg = EmailMessage()
            msg['To'] = email.utils.parseaddr(email_message['To'])[1]
            msg['From'] = email.utils.parseaddr(email_message['From'])[1]
            msg['Subject'] = email_message['Subject']

            date_tuple = email.utils.parsedate_tz(email_message['Date'])
            if date_tuple:
                local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
                msg['Date'] = "%s" %(str(local_date.strftime("%a, %d %b %Y %H:%M:%S")))

            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True)
                    msg.set_content(str(body))
                else:
                    continue                
            inbox.append(msg)
        return inbox

    def create_msg(self, subject, body, recipients):
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = self.sender_address
        msg['To'] = recipients
        msg.set_content(body)
        print('Message with subject "' +subject+ '" created')
        return msg

    def add_attachment(self, msg, file):
        content = file.read()
        ft = file.name.split('.')[1]
        mt = 'application/'+ft
        msg.add_attachment(content, maintype=mt, subtype=ft, filename=file.name)

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
        self.smtp_conn.send_message(msg)
        print('Message with subject "'+msg['Subject']+'" sent')
