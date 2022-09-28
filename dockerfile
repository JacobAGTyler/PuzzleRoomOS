# syntax=docker/dockerfile:1

FROM python:3.10-alpine as build

RUN apk add --no-cache apache2 apache2-dev apache2-mod-wsgi python3-dev build-base linux-headers pcre-dev

RUN pip install uwsgi

#ENV APACHE_RUN_USER www-data
#ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2

ADD server/site-config.conf /etc/apache2/conf.d/site.conf

WORKDIR /var/www/html

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ADD . .

FROM build as test
CMD ["python", "-m", "pytest"]


FROM build as verify
CMD ["python", "verification.py"]


FROM build as listener
CMD ["python", "listener/listener.py"]


FROM build as server
CMD ["python", "server/server.py"]


FROM build as webserver
STOPSIGNAL SIGWINCH
CMD ["/usr/sbin/httpd", "-D", "FOREGROUND"]
