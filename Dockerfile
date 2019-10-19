# ===================================================
# Base Image
# ===================================================
From python:3.7-alpine3.10

ENV PYTHON_VERSERION=3.7

USER root

# Add apache2 package
RUN apk --update --no-cache add apache2 apache2-dev \
    wget ca-certificates make gcc musl-dev

# Install mod_wsgi express
RUN /usr/local/bin/pip3 install --no-binary "mod_wsgi" mod_wsgi

# Set Apache2 Configuration
RUN mkdir -p /run/apache2

# Set testing and run server folder
RUN mkdir /home/bin
COPY ./bin /home/bin/
RUN chown -R apache.apache /home/bin/ && chmod 777 /home/bin/*.sh

# Set python code into docker
WORKDIR /home/app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./api_server ./api_server

RUN chown -R apache.apache ./

EXPOSE 8001

ENTRYPOINT /usr/local/bin/mod_wsgi-express start-server \
    --user apache \
    --maximum-requests=250 \
    --access-log \
    --access-log-format "[SIMPLE-API][%>s] %h %l %u %b \"%{Referer}i\" \"%{User-agent}i\" \"%r\"" \
    --error-log-format "[SIMPLE-API][%l] %M" \
    --log-to-terminal --log-level INFO \
    --url-alias /static static \
    --host 0.0.0.0 --port 8001 \
    --working-directory /home/app \
    --application-type module api_server.wsgi
