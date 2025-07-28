
FROM node:lts-bullseye as build

WORKDIR /app
COPY ./package*.json ./
COPY ./package.json ./


RUN npm audit fix
RUN npm install -g npm@11.5.1

COPY . .
RUN npm run build

FROM nginx:stable-bookworm-otel
COPY --from=build /app/build /usr/share/nginx/html
