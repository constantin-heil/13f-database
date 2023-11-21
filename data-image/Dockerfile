FROM alpine:latest

COPY datadownload.py .
COPY requirements.txt .
COPY dataspecs /dataspecs

RUN apk update && apk add python3
RUN python3 -m ensurepip
RUN python3 -m pip install -r requirements.txt

EXPOSE 3306

RUN mkdir /logging
CMD ["python3", "datadownload.py"]
