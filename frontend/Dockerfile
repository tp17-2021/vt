# first build the static files for FE
FROM node:12 AS build

WORKDIR /app

COPY package.json ./
COPY package-lock.json ./
RUN npm install

COPY . ./
RUN npm run build

# copy static files to nginx server and use this image for deployment
FROM nginx:1.19-alpine
COPY --from=build /app/public /usr/share/nginx/html
