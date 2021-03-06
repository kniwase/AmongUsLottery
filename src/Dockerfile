# Pythonの環境セットアップ
FROM python:3.8-buster

WORKDIR /work
COPY ./src/requirements.txt ./
RUN pip3 install --no-cache-dir -r ./requirements.txt
WORKDIR /app
RUN apt-get -y autoremove && \
    apt-get -y clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /work
