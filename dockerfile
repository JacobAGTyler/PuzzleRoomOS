# syntax=docker/dockerfile:1

FROM python:3.11-alpine as build

RUN apk add --no-cache apache2 apache2-dev apache2-mod-wsgi python3-dev build-base linux-headers pcre-dev

RUN python -m pip install --upgrade pip
RUN pip install uwsgi mariadb

#ENV APACHE_RUN_USER www-data
#ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2

ADD server/site-config.conf /etc/apache2/conf.d/site.conf

WORKDIR /var/www/html

RUN pip install virtualenv
RUN python -m venv --system-site-packages /var/www/html/venv
RUN source /var/www/html/venv/bin/activate
RUN python -m pip install --upgrade pip

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ADD . .

FROM build as test
WORKDIR /var/www/html
CMD ["python", "-m", "pytest"]


FROM build as verify
CMD ["python", "verification.py"]


FROM build as listener
WORKDIR /var/www/html
CMD ["python", "-m", "listener.listener"]


FROM build as server
WORKDIR /var/www/html
CMD ["python", "-m", "server.server"]


FROM build as webserver
WORKDIR /var/www/html
RUN sed -i "s/#ServerName www.example.com:80/ServerName puzzle-webserver:80/g" /etc/apache2/httpd.conf

STOPSIGNAL SIGWINCH
CMD ["/usr/sbin/httpd", "-D", "FOREGROUND", "-f", "/etc/apache2/httpd.conf"]