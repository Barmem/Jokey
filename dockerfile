FROM python:3.8-slim
LABEL maintainer="Barmem"
LABEL version="0.8.0"

WORKDIR /usr/src/Jokey
ADD . .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python", "main.py" ]
CMD [ "-h" ]