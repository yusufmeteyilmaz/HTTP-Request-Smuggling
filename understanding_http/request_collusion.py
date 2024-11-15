import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("httpbin.org", 80))

# Function to send a request and receive a response
def send_request(request_data):
    sock.send(request_data)

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
            content_length = parse_content_length(headers)

            if content_length is None:
                raise ValueError("Content-Length header not found in the response")

            # Now read the body based on Content-Length
            body = read_body(sock, content_length, body)

            # Combine headers and body
            full_response = headers + b"\r\n\r\n" + body
            return full_response.decode()  # Return the full HTTP response

# Function to parse the Content-Length from the headers
def parse_content_length(headers):
    headers_decoded = headers.decode()
    for line in headers_decoded.split("\r\n"):
        if line.lower().startswith("content-length:"):
            return int(line.split(":")[1].strip())
    return None

# Function to read the body based on Content-Length
def read_body(sock, content_length, body):
    bytes_received = len(body)
    remaining_content = content_length - bytes_received

    # If body is not complete, continue receiving data
    while bytes_received < content_length:
        chunk = sock.recv(min(4096, remaining_content))
        body += chunk
        bytes_received += len(chunk)
        remaining_content = content_length - bytes_received

    return body

if __name__ == "__main__":
    request_data_1 = b"POST /post HTTP/1.1\r\nHost: httpbin.org\r\nContent-Length: 4\r\n\r\nCoolP"
    response_1 = send_request(request_data_1)
    print("Response 1:\n" + response_1)

    request_data_2 = b"OST /post HTTP/1.1\r\nHost: httpbin.org\r\nContent-Length: 2\r\n\r\nhi"
    response_2 = send_request(request_data_2)
    print("Response 2:\n" + response_2)
    sock.close()

