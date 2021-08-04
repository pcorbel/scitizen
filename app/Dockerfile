FROM node:16.6.1-buster AS builder

WORKDIR /app

COPY ./package.json /app/package.json
COPY ./yarn.lock /app/yarn.lock
RUN yarn install --pure-lockfile

COPY . /app/
RUN yarn generate

FROM nginx:1.21.1-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
