import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('example.com', 80))

content_items = [
    'GET / HTTP/1.0',
    'Host: example.com',
    'Connection: keep-alive',
    'Accept: text/html',
    '\n'
]

content = '\n'.join(content_items)
print('----mes----')
print(content)
print('----end----')
sock.send(content.encode())
res = sock.recv(10024)
print(res.decode())
