FROM arm64v8/node:20-slim

WORKDIR /app

# Install dependencies first so that we can cache the dependencies
COPY ./package* .
RUN npm install && npm install -g nodemon

# Install curl for healthchecks
RUN apt update && apt install -y curl

USER node

COPY ./src ./src

CMD ["node", "src/index.js"]
