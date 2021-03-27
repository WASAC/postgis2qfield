FROM osgeo/gdal:ubuntu-small-3.2.2 AS builder
WORKDIR /usr/src/app

RUN apt update \
  && apt -y upgrade \
  && apt-get install -y python3 python3-pip

COPY Pipfile ./
RUN pip3 install pipenv \
  && pipenv install

COPY . ./

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]