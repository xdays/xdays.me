FROM python:2.7
MAINTAINER xdays <easedays@gmail.com>

WORKDIR /opt/blog
ADD requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

VOLUME /opt/blog

CMD ["./genblog.sh"]
