# ARM64 uyumlu bir base imajı kullanıyoruz
FROM arm64v8/python:3.9-slim

# Sistem güncellemeleri ve gerekli araçlar
RUN apt-get update && apt-get install -y \
    gcc \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install markupsafe==2.0.1

# Mitmproxy'yi pip ile kuruyoruz
RUN pip install mitmproxy==6.0.2 --break-system-packages

# Çalışma dizini
WORKDIR /app

# Filtre scriptinizi Docker konteynerine kopyalayın
COPY filter.py filter.py

# Mitmproxy'yi başlatan komut
ENTRYPOINT mitmdump --mode reverse:http://${SERVER_HOSTNAME}:${SERVER_PORT} -p 8002 -s filter.py --set block_global=false --no-http2

