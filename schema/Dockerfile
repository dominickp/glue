FROM node:20-slim

RUN npm install -g serve

WORKDIR /app

COPY ./serve.json /app/public/serve.json

COPY ./swagger.yml /app/public/swagger.yml

CMD ["serve", "-s", "public", "--listen", "80"]

