FROM node:16-slim

WORKDIR /app
COPY package.json ./
RUN npm install

COPY index.js ./
COPY view/ view/


RUN chown -R node:node /app
USER node

EXPOSE 1337
CMD ["node", "index.js"]
