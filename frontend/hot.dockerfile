FROM node:16 AS build

WORKDIR /app

COPY package.json ./
COPY package-lock.json ./

# RUN npm install

ADD ./start.sh /
RUN chmod +x /start.sh

CMD ["/start.sh"]

# CMD [ "npm", "install", ";", "npm", "run", "build", "--reload" ]
# CMD [ "sleep", "1000" ]