FROM node:20

WORKDIR /app

COPY ./package* .

RUN npm install && npm install -g nodemon

USER node

COPY ./src ./src

CMD ["node", "src/index.js"]
