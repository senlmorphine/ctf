FROM node:16-slim

WORKDIR /app
COPY package.json ./
RUN npm install

COPY index.js ./
COPY public/ public/
COPY views/ views/


RUN chown -R node:node /app
USER node

EXPOSE 6969
CMD ["node", "index.js"]
