import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(("httpbin.org", 80))
sock.send(b"POST /post HTTP/1.1\r\nHost: httpbin.org\r\nContent-Length:5\r\n\r\n12345")

response = b""
while True:
    chunk = sock.recv(4096)
    if len(chunk) == 0:
        break
    response += chunk

print(response.decode())

sock.close()


