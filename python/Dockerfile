FROM python:3.12-slim

RUN mkdir /app
WORKDIR /app

# Install dependencies first so that we can cache the dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy the source code
COPY ./src /app

CMD flask --app main run --host=0.0.0.0

