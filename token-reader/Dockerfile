FROM python:3.10-alpine3.14 as base

WORKDIR /code

RUN apk add	-U bash libusb-dev gcc linux-headers musl-dev eudev-dev

COPY ./requirements.txt /code/requirements.txt

RUN pip install --upgrade -r /code/requirements.txt

COPY ./src /code/src

FROM base as test
COPY ./test.py /code/test.py
CMD [ "pytest", "test.py",  "-rP", "--verbose", "--asyncio-mode=strict" ]


FROM base as build
CMD [ "python3", "src/main.py" ]