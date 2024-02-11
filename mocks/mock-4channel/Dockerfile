FROM node:20-slim

WORKDIR /app

COPY ./package* .

RUN npm install && npm install -g nodemon

USER node

COPY . .

CMD ["node", "index.js"]
