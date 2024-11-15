 ### What is HTTP ?
HTTP, or Hypertext Transfer Protocol, is the foundational protocol used for transmitting data over the web.

HTTP is stateless, each request is isolated from others.
"There isn't relationship maintained between one connection and another, even from the same client."
So server can't know who send which request, it needs cookies & headers to differentiate from each other. [https://stackoverflow.com/questions/13200152/why-is-it-said-that-http-is-a-stateless-protocol]

"As a real life analogy, a stateless communication is like radio conversation between pilot and ground controllers, where you're expected to always state your callsign and usually the callsign of the message destination with every spurt of messages. On the other hand, a stateful protocol is like a telephone conversation, where you rely that the person on the other side to remember who you are." [https://www.linkedin.com/pulse/tcp-state-ful-protocol-http-state-less-why-nikhil-goyal/]

Stateless:
![](../Images/1-%20What's/ground_station.png)
[https://www.aopa.org/-/media/files/aopa/home/pilot-resources/asi/sampleradiocalls.pdf]
### What is HTTP 1.0 ?
In HTTP 1.0, you have to open TCP connection each time you request something:
![](../Images/1-%20What's/HTTP_1.0.png)

### What is HTTP 1.1 ?
In HTTP 1.1, you can use same TCP connection over and over again.
![](../Images/1-%20What's/HTTP_1.1.png)

##### What is Connection: keep-alive, close and Pipeline ?

When HTTP/1.0 created, connection was always closed after being used once.
So "Connection: close" was default behaviour.

By late 1995, web servers and some browsers began using 'Connection: keep-alive'. If we want to explicitly use same connection, we can use Connection: keep-alive.
Default for HTTP/1.0:
![](../Images/1-%20What's/HTTP_1.0_conn_default.png)

We are explicitly asking for connection reuse:
![](../Images/1-%20What's/HTTP_1.0_conn_alive.png)
Note for Burp Suite:
![](../Images/1-%20What's/burp_conn_reuse_setting.png)

You do not need Connection: keep-alive in HTTP/1.1 since it is default anyways.

Default for HTTP/1.1:
![](../Images/1-%20What's/HTTP_1.1_default.png)

But if you want to close connection somewhy, you can use it in HTTP/1.1 too.

Connection: close, HTTP/1.1:
![](../Images/1-%20What's/HTTP_1.1_conn_close.png)

##### What is HTTP Pipelining?

This feature is part of HTTP/1.1. With HTTP/1.1, you can send multiple requests over a single connection and wait for the corresponding responses. The responses will arrive in the same order they were sent.

Normally, in HTTP/1.1, even when using a single connection, you must wait for the previous response to arrive before making another request.

Example:
![](../Images/1-%20What's/without_pipelining.png)
It took 6 seconds without using pipelining.
We had to wait previous request's response before making a new request.

Pipelining:
![](../Images/1-%20What's/with_pipelining.png)

We send all requests and wait for responses. (in same order)