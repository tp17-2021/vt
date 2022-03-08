# first build the static files for FE
FROM node:16 AS build

WORKDIR /app

COPY package.json ./
COPY package-lock.json ./
RUN npm install

COPY . ./
ARG vite_base_path
ENV VITE_BASE_PATH=$vite_base_path
RUN echo $vite_base_path > /app/.env.production
RUN npm run build

# copy static files to nginx server and use this image for deployment
FROM nginx:1.19-alpine
COPY ./conf.d /etc/nginx/conf.d
COPY --from=build /app/dist /usr/share/nginx/html
