FROM python:3.11.4

WORKDIR /app

COPY . .

# RUN apt update \
#     && apt install -y libpq-dev build-essential \
#     && apt clean \
#     && rm -rf /var/lib/apt/lists/*

RUN pip3 install -r /app/requirements.txt --no-cache-dir