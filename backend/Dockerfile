FROM python:3.10-alpine as base

WORKDIR /code

COPY ./requirements.txt ./code/requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r ./code/requirements.txt

COPY ./src /code/src


FROM base as test

COPY ./requirements_test.txt ./code/requirements_test.txt
RUN pip3 install --no-cache-dir --upgrade -r ./code/requirements_test.txt

COPY ./tests.py /code/tests.py
CMD [ "pytest", "tests.py", "-rP", "--verbose", "--asyncio-mode=strict" ]


FROM base as build
CMD [ "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80" ]