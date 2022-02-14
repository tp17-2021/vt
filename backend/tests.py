import pytest
import asyncio
import uvicorn
import requests
from requests_async import ASGISession
from httpx import AsyncClient
import requests_mock

from fastapi.testclient import TestClient

import src.main
from src.main import app
from src.main import election_config
from src.main import election_state
from src.main import send_vote_to_gateway
from src.main import send_token_to_gateway

client_2 = ASGISession(app)


@pytest.fixture()
def mock_send_current_election_state_to_client(mocker):
    future = asyncio.Future()
    mocker.patch('src.main' + '.send_current_election_state_to_client', return_value = future)
    return future


@pytest.fixture()
def mock_send_validated_token_to_client(mocker):
    future = asyncio.Future()
    mocker.patch('src.main' + '.send_validated_token_to_client', return_value = future)
    return future


# @pytest.mark.asyncio
# async def test_config_received(mock_send_election_config_to_client):

#     test_config = {"Test":"Test"}

#     global election_config
#     assert election_config == None

#     mock_send_election_config_to_client.set_result( { "code":200, "dict":{} } )

#     response = await client_2.post("/api/election/config", json = test_config)
#     assert response.status_code == 200
#     assert src.main.election_config == test_config


# @pytest.mark.asyncio
# async def test_election_state(mock_send_current_election_state_to_client):

#     test_state = {"status": "end"}

#     global election_state
#     assert election_state == 'end'

#     mock_send_current_election_state_to_client.set_result( { "code": 200, "status": "end" } )

#     response = await client_2.post("/api/election/state", json = test_state)
#     assert response.status_code == 200
#     assert src.main.election_state == test_state['status']


# @pytest.mark.asyncio
# async def test_send_token_to_gateway(mock_send_validated_token_to_client):
#     ### Not done

#     with requests_mock.Mocker() as mock_request:
#         mock_request.post("http://host.docker.internal/voting-service-api/api/token-validity", text="true", status_code=200 )

#         mock_send_validated_token_to_client.set_result( { "code":200} )

#         response = await send_token_to_gateway('valid')



# @pytest.mark.asyncio
# async def test_send_vote_to_gateway():

#     with requests_mock.Mocker() as mock_request:
#         mock_request.post("http://host.docker.internal/voting-service-api/api/vote", text="true", status_code=200 )
#         response = requests.post("http://host.docker.internal/voting-service-api/api/vote",json={ 'token':"valid",'vote':{} } )
#         assert response.text == "true"
#         assert response.status_code == 200


