# thanks to chatgpt :p I just did little bit of editing

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server (httpbin.org)
sock.connect(("httpbin.org", 80))

# Send a POST request
request = b"POST /post HTTP/1.1\r\nHost: httpbin.org\r\nContent-Length: 5\r\n\r\n12345"
sock.send(request)

# Initialize response variable
response = b""

# Read HTTP response headers and body
while True:
    # Receive data in chunks
    chunk = sock.recv(4096)
    response += chunk

    # Check if we have the full headers (looking for '\r\n\r\n')
    if b"\r\n\r\n" in response:
        # Split headers and body
        headers, body = response.split(b"\r\n\r\n", 1)

        # Now, parse headers for Content-Length
        headers_decoded = headers.decode()
        content_length = None
        for line in headers_decoded.split("\r\n"):
            if line.lower().startswith("content-length:"):
                content_length = int(line.split(":")[1].strip())

        if content_length is None:
            raise ValueError("Content-Length header not found in the response")

        # Now read the body based on Content-Length
        bytes_received = len(body)
        remaining_content = content_length - bytes_received

        # If body is not complete, continue receiving data
        while bytes_received < content_length:
            chunk = sock.recv(min(4096, remaining_content))
            body += chunk
            bytes_received += len(chunk)
            remaining_content = content_length - bytes_received

        break  # Exit the loop when everything is done

# Decode and print response
full_response = headers + b"\r\n\r\n" + body
print(full_response.decode())

sock.close()

