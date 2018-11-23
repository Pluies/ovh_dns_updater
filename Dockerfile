FROM python:3

RUN pip install ovh kubernetes

ADD ovh_dns_updater.py ovh_dns_updater.py

CMD python ovh_dns_updater.py
