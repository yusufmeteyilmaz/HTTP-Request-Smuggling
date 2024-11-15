
This is just solution and little bit of analysis. We won't talk about how to detect it, there is a timing technique explained in youtube, portswigger labs.
(https://www.youtube.com/playlist?list=PLGb2cDlBWRUX1_7RAIjRkZDYgAB3VbUSw)

First let's start by mitmproxy. (on port 8002)

Check the source code (lab_extras folder),
read.py for mitmproxy
message.py for gunicorn

In mitmproxy:
```
if "chunked" in headers.get("transfer-encoding", "").lower():
```
In gunicorn:
```
if value.lower() == "chunked":
```

If I set transfer-encoding: Xchunked

mitmproxy would accept this as valid, but gunicorn won't.
mitmproxy checks if "chunked" in "Xchunked", while gunicorn checks if it is exactly equal to "chunked".

What we know?
- If we provide Xchunked, frontend will parse the request as chunked, while backend will parse it as content-length (because backend thinks it is not chunked)
Craft a request:
- It should pass mitmproxy as whole, mitmproxy should forward entire request to backend.
- Backend will parse request by checking content-length header, so you must choose it carefully.

![](../Images/5-%20Lab%20Solution%201/base_req.png)

We need to fill data and length fields.
Let's use very straight forward approach.
data:
```
GET /flag HTTP/1.1\r\n
Host: nothing\r\n\r\n
```
length: 37 bytes (0x25)

![](../Images/5-%20Lab%20Solution%201/post_req_0.png)

Total length: 48 bytes

What do we expect to happen now?
- Frontend will check chunked, forward request to backend.
- Backend will check chunked, fail, then parse it as CL header indicates.

So we need to set CL header accordingly:
![](../Images/5-%20Lab%20Solution%201/post_req_1.png)

Backend will see 3 different requests:

```
POST / HTTP/1.1\r\n
Host: we_do_not_need_host\r\n
Content-Length: 4\r\n
Transfer-Encoding: chunked\r\n
\r\n
25\r\n
```

```
GET /flag HTTP/1.1\r\n
Host: nothing\r\n\r\n
```

```
\r\n
0\r\n\r\n
```

So it needs to send 3 responses? Let see!!!

![](../Images/5-%20Lab%20Solution%201/oh_no_post.png)

Ooops, let's try get

![](../Images/5-%20Lab%20Solution%201/wireshark_0.png)

Nope?

Let see other wireshark in docker.
![[Images/5- Lab Solution 1/wireshark_1.png]]

Edit-->Preferences-->Name Resolution-->Resolve network (ip) adresses
View-->Name Resolution-->Edit Resolved Name

![[Images/5- Lab Solution 1/wireshark_2.png]]

Servers sent 3 responses to mitmproxy but mitmproxy only sent me 1 response.

We can say "mitmproxy only wants to send 1 response to 1 request"
But it is better to don't assume things, every proxy and server can act different.
Nevertheless we have an easy way out. (I'll show you in a min)

What happens if we send one more request?
![[Images/5- Lab Solution 1/wireshark_3.png]]

It didn't work because our single tcp connection closed, we can confirm it by checking stream id. Meaning? There is a time limit apparently, if x request not send in y seconds, why would we keep connection open? Maybe.. It could be for many reasons, but this is what we know right now.

![[Images/5- Lab Solution 1/wireshark_4.png]]

Let's try to send requests in a single tcp connection, but fast.
![](../Images/5-%20Lab%20Solution%201/post_req_2.png)

![](../Images/5-%20Lab%20Solution%201/post_req_3.png)

Nice that worked! 
Another way to do that:
At first it maybe confusing but think as sending data not request.

![](../Images/5-%20Lab%20Solution%201/post_req_4.png)
![[Images/5- Lab Solution 1/wireshark_5.png]]

The key difference is, in this case we sent all requests at once, rather than sending request & waiting response cycle. (http pipelining)

![](../Images/5-%20Lab%20Solution%201/wireshark_6.png)

