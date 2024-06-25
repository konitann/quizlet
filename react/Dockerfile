FROM node:20
ENV NODE_ENV=development

WORKDIR /usr/src/app

COPY package.json package-lock.json ./
RUN npm install --save --legacy-peer-deps
RUN npm install -g react-scripts

COPY . .

CMD ["npm", "start"]
