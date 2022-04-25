if [ "$VT_ONLY_DEV" == "1" ]
then
    # generate python class from local test file
    datamodel-codegen --input /code/tests/datamodels.yaml --output /code/src/schemas/votes.py

else
    # generate python vote class from json spec
    datamodel-codegen --url http://$STATE_VECTOR_PATH/config/datamodels.yaml --output /code/src/schemas/votes.py
    # datamodel-codegen --url https://$STATE_VECTOR_PATH/config/datamodels.yaml --output /code/src/schemas/votes.py

fi

ls -lah /code/src/schemas

# start server
uvicorn src.main:app --host 0.0.0.0 --port 80
