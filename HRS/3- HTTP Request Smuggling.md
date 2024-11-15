No one knows where a request ends or not.
That's why we are using content-length and transfer-encoding.
And it may cause problems.

![](../Images/3-%20HTTP%20Request%20Smuggling/single_conn.png)
Note: this is single tcp connection. (keep-alive)

![](../Images/3-%20HTTP%20Request%20Smuggling/feature_not_bug.png)

#### What if, content-length was wrong?

![](../Images/3-%20HTTP%20Request%20Smuggling/feature_not_bug_1.png)

![](../Images/3-%20HTTP%20Request%20Smuggling/feature_not_bug_2.png)

#### But we can't exploit anyone! (yet)

![](../Images/3-%20HTTP%20Request%20Smuggling/too_far.png)

We can only affect requests that are using same connection.
So we only affect ourself, nice!

Wish there was something that force everyone to use same connection.
Like so:
![](../Images/3-%20HTTP%20Request%20Smuggling/wish.png)

Actually that's possible:
![](../Images/3-%20HTTP%20Request%20Smuggling/reverse_proxy.png)
If reverse proxy using HTTP/1.1 to talk server, attacker can craft a request.
Note: it doesn't have to be reverse proxy, it can be anything that does the job.
(e.g., waf, load balancer..)

Attacker's goal:
- Craft a request that will:
1- Pass reverse proxy safely
2- Confuse the server to become more than 1 request (1, 2 maybe 1.5 request)

Example:
Front end server prioritizes CL (Content Length).
Backend server prioritizes TE (Transfer encoding).
![](../Images/3-%20HTTP%20Request%20Smuggling/setup.png)
Attacker sends this request:
![](../Images/3-%20HTTP%20Request%20Smuggling/frontend.png)

--> Front end saw this and said "This is only a 1 request. I am waiting for 1 response." 
--> Front end using CL, it will read 26 bytes, so it will completely read body and reconstruct the request and move to backend, then it will check it's socket until there is a response. (It needs to parse the request, otherwise it can't process it, so it doesn't just redirect request to backend. It takes the request, process it, rebuild it and maybe add some internal headers, then it will send request to backend)

- Parse request
- Reconstruct it, forward to backend
- Check socket, is there a response? If so forward it back to user

But backend prioritizes TE:
data:

```
POST / HTTP/1.1\r\nContent-Length: 26\r\nTransfer-Encoding: chunked\r\n\r\n0\r\n\r\nGET /xss HTTP/1.1\r\n\r\n
```

![](../Images/3-%20HTTP%20Request%20Smuggling/to_backend_0.png)

When that *data* arrives the backend:
It will check TE header, TE header says "I don't have any data"
Backend ends processing first request, sends response back.

Request 1:
![](../Images/3-%20HTTP%20Request%20Smuggling/backend_0.png)
Response 1:
```
HTTP/1.1 400 Bad Request
...
```

![](../Images/3-%20HTTP%20Request%20Smuggling/from_backend_0.png)

Backend will process remaining data, because connection: keep-alive, unlimited data flow..

It will parse request, create a respond.

Request 2:
![[backend_1.png]]

Response 2:
![](../Images/3-%20HTTP%20Request%20Smuggling/from_backend_1.png)

Backend responds but frontend server has no where to forward it, so response just sits in frontend's socket.

When client sends a request:

```
GET /index.html HTTP/1.1\r\n\r\n
```

![](../Images/3-%20HTTP%20Request%20Smuggling/to_backend_1.png)

Front end server received the request, parsed it, processed it, sent to backend server. Then started waiting while checking it's socket.

But there is data already in the socket! So it thinks that must be belong to that request! And sends to client.

![](../Images/3-%20HTTP%20Request%20Smuggling/from_front_end_0.png)

What about client's request you may ask?

![](../Images/3-%20HTTP%20Request%20Smuggling/from_backend_2.png)

It will sit in the socket, so on..

Main idea is like above, but in real life even in lab condition, many things can change.

Note: Normally almost every request has "Host" header too, I gave above example without one.