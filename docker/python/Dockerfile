FROM debian:jessie

RUN awk '$1 ~ "^deb" { $3 = $3 "-backports"; print; exit }' /etc/apt/sources.list > /etc/apt/sources.list.d/backports.list

RUN apt-get update && \
 	apt-get install -y python-setuptools && \
 	apt-get install -y python-pip

RUN pip install redis

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

WORKDIR /src

EXPOSE 5000 5000

ENTRYPOINT ["python"]

CMD ["/src/app.py"]
