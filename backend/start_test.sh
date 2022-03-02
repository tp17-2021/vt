# generate python vote class from json spec
datamodel-codegen --input /code/tests/datamodels.yaml --output /code/src/schemas/votes.py

ls -lah /code/src/schemas

# start server
pytest -rP --verbose --asyncio-mode=strict
