FROM python:3.10-alpine as base

WORKDIR /code

RUN apk update
RUN apk add -U gcc g++ bash
RUN apk add jpeg-dev zlib-dev libjpeg
RUN apk add --upgrade poppler
RUN apk add --upgrade poppler-utils

COPY ./requirements.txt ./code/requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade -r ./code/requirements.txt

COPY ./requirements_test.txt ./code/requirements_test.txt
RUN pip3 install --upgrade -r ./code/requirements_test.txt

RUN mkdir /secret
RUN mkdir /idk_data

COPY ./tests /code/tests
COPY ./src /code/src


FROM base as test

COPY ./start_test.sh ./start_test.sh
RUN chmod 700 ./start_test.sh
CMD [ "bash", "start_test.sh" ]



FROM base as build

COPY ./start.sh ./start.sh
RUN chmod 700 ./start.sh
CMD [ "bash", "start.sh" ]
