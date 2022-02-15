FROM node:16 AS build

WORKDIR /app

COPY frontend/package.json ./
COPY frontend/package-lock.json ./

# RUN npm install

ADD frontend/start.sh /
RUN chmod +x /start.sh

CMD ["/start.sh"]

# CMD [ "npm", "install", ";", "npm", "run", "build", "--reload" ]
# CMD [ "sleep", "1000" ]