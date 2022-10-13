FROM python:3.10.8

RUN apt-get update; \
    apt-get install -y --no-install-recommends \
        # To fetch from pip
        git \
        libmemcached-dev \
        zlib1g-dev \
       ; \
    rm -rf /var/lib/apt/lists/*;

WORKDIR /
COPY requirements.txt /

RUN pip install --use-deprecated=legacy-resolver -U -r requirements.txt

COPY / /web

ENV DOMAIN="duckhunt.me"
ENV SECRET_KEY=""
ENV DEBUG="False"
ENV DB_PORT="5432"
ENV DB_USER=""
ENV DB_PASSWORD=""
ENV DB_NAME=""
ENV MEMCACHED_LOC=""
ENV DH_API_KEY=""
ENV DH_API_URL=""

COPY docker_run.sh /run.sh

WORKDIR /web/src/

ENTRYPOINT ["sh"]
CMD ["/run.sh"]

EXPOSE 8080/tcp