# another-email-client
A simple email client written in python

## Example Usage

### Import
```python
from anotheremailclient import EmailClient
```

### Starting a session during initialization
```python
client = EmailClient("gmail.com", 587, True)
```

### Initialize without starting a session
```python
client = EmailClient()
```

### Set server name and port
```python
client.set_server_name("gmail.com")
client.set_port(587)
```

### Start a session
```python
client.start()
```

### Start a session with server and port
```python
client.start("gmail.com", 587)
```

### Shutdown server
```python
client.shutdown()
```

## Login
```python
client.login("you@gmail.com", "password")
```

### Send message
```python
client.send_msg("Message Subject", "Message Body", "recipient@gmail.com")
```

### Create EmailMessage object
```python
msg = client.create_msg("Message Subject", "Message Body", "recipient@gmail.com")
```

### Send message object
```python
client.send_msg_obj(msg)
```

### Add message to the queue
```python
client.queue_msg(msg)
```

### Send every message in the queue
```python
client.send_queue()
```

### Send first 5 messages in the queue
```python
client.send_queue(5)
```

### Check if message queue is full
```python
client.is_msg_queue_full()
```

### Check if message queue is empty
```python
client.is_msg_queue_empty()
```