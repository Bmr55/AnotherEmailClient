from anotheremailclient import EmailClient

def test_msg_queue():
    print("Testing function(s) create_msg() & send_queue()")

    # Create EmailClient object
    client = EmailClient("gmail.com", 587, True)

    # Login to email account
    client.login("sender@gmail.com", "password")

    # Create EmailMessage objects
    msg1 = client.create_msg("Message Subject 1", "Message body 1", "test@gmail.com")
    msg2 = client.create_msg("Message Subject 2", "Message body 2", "test@gmail.com")
    msg3 = client.create_msg("Message Subject 3", "Message body 3", "test@gmail.com")

    # Add messages to the message queue
    client.queue_msg(msg1)
    client.queue_msg(msg2)
    client.queue_msg(msg3)

    # Send every message in the queue
    client.send_queue()

def test_send():
    print("Testing function(s) send_msg()")

    # Create EmailClient object
    client = EmailClient("gmail.com", 587, True)

    # Login to email account
    client.login("sender@gmail.com", "password")

    # Send a single message
    client.send_msg("Message Subject", "Message Body", "test@gmail.com")

    # Create an EmailMessage object
    msg = client.create_msg("Message Subject", "Message Body", "test@gmail.com")

    # Send EmailMessage object
    client.send_msg_obj(msg)

def test():
    client = EmailClient()
    client.set_server_name("gmail.com")
    client.set_port(587)
    client.start()

test()

