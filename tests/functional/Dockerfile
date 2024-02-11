FROM python:3.12-slim

RUN mkdir /tests
WORKDIR /tests
COPY ./requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

COPY . .

CMD ["pytest", "-v", "./mock"]
