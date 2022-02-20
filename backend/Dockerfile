FROM python:3.10-alpine as base

WORKDIR /code

RUN apk add -U gcc g++ bash

COPY ./requirements.txt ./code/requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r ./code/requirements.txt

RUN mkdir /secret
RUN mkdir /idk_data

COPY ./src /code/src


FROM base as test

COPY ./requirements_test.txt ./code/requirements_test.txt
RUN pip3 install --no-cache-dir --upgrade -r ./code/requirements_test.txt

COPY ./tests /code/tests

COPY ./start_test.sh ./start_test.sh
RUN chmod 700 ./start_test.sh
CMD [ "bash", "start_test.sh" ]



FROM base as build

COPY ./start.sh ./start.sh
RUN chmod 700 ./start.sh
CMD [ "bash", "start.sh" ]
