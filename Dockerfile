# Debian Slim with Python 3.6 on Docker
# =============================================================================
# FROM dockercentral.it.example.com:5100/com.example.dev.argos/debian:stretch-slim
FROM debian:stretch-slim

# Set the Python 3.x.x version.
# =============================================================================
ENV PYTHON_VERSION="3.7.3"

# =============================================================================
# Debian: Ensure we have an up to date package index.
# =============================================================================
RUN rm -rf /var/lib/apt/lists/*
RUN apt-get update
RUN apt-get dist-upgrade

RUN apt-get install -y locales

# Install Python3 interpreter
# =============================================================================
WORKDIR /root/python-workspace

# Set Locale to US English.
RUN localedef  -c -i en_US -f UTF-8 en_US.UTF-8 || /bin/true
ENV LC_ALL "en_US.UTF-8"

# Download and build python 3.x.x
COPY ./python_build_all.sh .
RUN  ./python_build_all.sh

# Add python shared libs to the path.
COPY python3-x86_64.conf /etc/ld.so.conf.d/
RUN ldconfig -v

# Upgrade pip.
RUN /usr/local/bin/pip3 install --upgrade pip

# Install Apache2 for use from port 80.
# =============================================================================
RUN apt-get -y install apache2 apache2-dev

# Install mod_wsgi-express over Apache2.
# =============================================================================
RUN /usr/local/bin/pip3 install mod_wsgi

# Set testing and run server folder
RUN mkdir /home/bin
COPY ./bin /home/bin/
RUN chown -R www-data.www-data /home/bin/ && chmod 777 /home/bin/*.sh

# Set python code into docker
WORKDIR /home/app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./api_server ./api_server

RUN chown -R www-data.www-data ./

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
    --application-type module api_server.wsgi
