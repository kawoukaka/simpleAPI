# ===================================================
# Base Image
# ===================================================
From python:3.7-alpine3.10

ENV PYTHON_VERSERION=3.7

USER root

RUN apt --update --no-cache add apache2 apache2-dev \
    wget ca-certificates make gcc musl-dev

RUN /usr/local/bin/pip3 install --no-binary "mod_wsgi" mod_wsgi

RUN mkdir -p /run/apache2

WORKDIR /home/app

EXPOSE 8001

ENTRYPOINT /usr/local/bin/mod_wsgi-express start-server \
    --user www-data \
    --maximum-requests=250 \
    --access-log \
    --access-log-format "[SIMPLE-API][%>s] %h %l %u %b \"%{Referer}i\" \"%{User-agent}i\" \"%r\"" \
    --error-log-format "[SIMPLE-API][%l] %M" \
    --log-to-terminal --log-level INFO \
    --url-alias /static static \
    --host 0.0.0.0 --port 8001 \
    --working-directory /home/app \
    --application-type module app.wsgi
