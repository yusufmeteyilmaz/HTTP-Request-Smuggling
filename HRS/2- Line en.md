ding

If we can't determine where the data ends, we can't process it properly. Even if we attempt to process it, it would only lead to issues.

Imagine your job is to process a sentence, word by word, adding punctuation, setting capitalization, and so on as you go. Data arrives word by word, but you don’t know how much will be sent, and there may be delays.

Example:
They send ['the', 'sentence', 'ends] in one go. What would you do?
Wait for more or process the data?

You wait a bit more, and the data becomes:
['the', 'sentence', 'ends', 'when', 'you', 'start', 'to', 'think', 'about']

Do you wait more or process it?

You wait a bit more:
['the', 'sentence', 'ends', 'when', 'you', 'start', 'to', 'think', 'about', 'where', 'it', 'begins']

A bit more:
['the', 'sentence', 'ends', 'when', 'you', 'start', 'to', 'think', 'about', 'where', 'it', 'begins', "it's", 'just', 'a', 'matter', 'of', 'when', 'ends', 'begins']

The same problem applies to requests.
#### How do we know when a request ends and other starts?

Before we answer that question, we need to understand basics of a request.
##### Parts of a request:

1. Request line
2. Headers
3. Body

Request line: This is one line long and ends with `\r\n`(CR-LF) 
method + path + http version
`GET /test1234 HTTP/1.1`

Headers: Provides additional information about the request. Each header line ends with `\r\n`.  
The header section is terminated by **two** `\r\n` (CR-LF) sequences.
`Host: example.com\r\n`

Body: This is used to transfer information (e.g., form data, JSON payloads, etc.).

Example request:
![](../Images/2-%20Line%20en/burp_cr_lf_get.png)

This part is fine but what about if our request had a body?

==Note: You can send any http request with body, such as GET, POST,PUT,UPDATE..., apparently except for TRACE(?)==
==But whether it will be accepted or not depends on the server.==

Example Post Request:

![](../Images/2-%20Line%20en/post_requests/post_request_1.png)
![](../Images/2-%20Line%20en/post_requests/post_response_1.png)

![](../Images/2-%20Line%20en/post_requests/post_request_2.png)

![](../Images/2-%20Line%20en/post_requests/post_response_2.png)

A few example of different Content-Type:

![](../Images/2-%20Line%20en/httpbin/httpbin_0.png)
![](../Images/2-%20Line%20en/httpbin/httpbin_1.png)
![](../Images/2-%20Line%20en/httpbin/httpbin_2.png)
![](../Images/2-%20Line%20en/httpbin/httpbin_3.png)

What would happen if we change the Content-Length?

Uncheck "Update Content-Length", so burp won't update content-length header
![](../Images/2-%20Line%20en/uncheck_update_cl.png)

![](../Images/2-%20Line%20en/post_requests/post_request_4.png)

![](../Images/2-%20Line%20en/post_requests/post_response_4.png)

Content-Length: 4
![](../Images/2-%20Line%20en/post_requests/post_request_5.png)
![](../Images/2-%20Line%20en/post_requests/post_response_5.png)
Even though we sent test=abc, server only read up to Content-Length's value.
(Content-Length: 4, means 4 bytes. Each char is 1 byte. \r 1 byte, \n 1 byte)

Since we talk about how do we know when a request ends, the answer is we do not. That's why we use Content-Length or Transfer-Encoding headers to determine length of a request/response.

We saw how Content-Length works above, let's see how Transfer-Encoding: chunked works.

Chunked: 
This is normally used when we don't know how much data is going to send/received.

Structure:

```
length\r\n
data\r\n

length1\r\n
data1\r\n

0\r\n
\r\n
```
length: length of the data as bytes in hexadecimal
note: above example just for demonstration, there isn't space between chunks.
see below:

5\r\n
cool_\r\n
9\r\n
gallipoli\r\n
0\r\n
\r\n

![](../Images/2-%20Line%20en/chunked_0.png)

Example  from wikipedia:
![](../Images/2-%20Line%20en/wikipedia.png)

![](../Images/2-%20Line%20en/chunked_1.png)
