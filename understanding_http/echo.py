import socket

host = ''
port = 7331

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen()

conn, addr = sock.accept()

print('Connected by', addr)
while 1:
  data = conn.recv(1024)
  if not data: break
  conn.sendall(data)
conn.close()
