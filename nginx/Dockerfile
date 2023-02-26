FROM nginx:1.23.0-alpine

COPY ./* /etc/nginx/
COPY ./run.sh /run.sh

ENV APP_HOST=ggj23_server
ENV APP_PORT=11000

USER root

RUN apk add --no-cache openssl bash
RUN chmod +x /run.sh

VOLUME /vol/static
VOLUME /vol/www

CMD ["/run.sh"]