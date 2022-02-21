# generate python vote class from json spec
datamodel-codegen --url http://$STATE_VECTOR_PATH/config/datamodels.yaml --output /code/src/schemas/votes.py

ls -lah /code/src/schemas

# start server
uvicorn src.main:app --host 0.0.0.0 --port 80
