FROM    node:16 as build

ARG     BACKEND_URL

WORKDIR /opt/src

ADD     . /opt/src

RUN     npm i && npm run build

FROM    nginx:1.23 as web

COPY    --from=build /opt/src/dist/spa/ /usr/share/nginx/html/
