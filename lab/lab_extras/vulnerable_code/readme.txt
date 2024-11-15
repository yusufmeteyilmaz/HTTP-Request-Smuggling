read.py for mitmproxy
message.py for gunicorn

To get the files yourself:
- Run the lab
- Find container id of mitmproxy
- Find container id of gunicorn
- Copy read.py from mitmproxy
- Copy message.py from gunicorn

sudo docker-compose up -d
sudo docker ps -a
sudo docker cp [mitmproxy_container_id]:/usr/local/lib/python3.9/site-packages/mitmproxy/net/http/http1/read.py .
sudo docker cp [gunicorn_container_id]:/usr/local/lib/python3.13/site-packages/gunicorn/http/message.py .
