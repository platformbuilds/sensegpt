
FROM node:lts-bullseye as build

WORKDIR /app
COPY ./package*.json ./
COPY ./package.json ./

RUN npm install

COPY . .
RUN npm run build

FROM nginx:stable-bookworm-otel
COPY --from=build /app/build /usr/share/nginx/html
