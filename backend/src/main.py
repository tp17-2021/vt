import logging
import os
import sys

from fastapi import Body, FastAPI, status, HTTPException
from fastapi.responses import HTMLResponse
from fastapi_socketio import SocketManager
import uvicorn
import requests

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI(root_path=os.environ['ROOT_PATH'])


import logging

LOGGER = logging.getLogger(__name__)

# app.mount("/public", StaticFiles(directory="/public", html = True), name="site")

# origins = ["http://localhost:8079/", "http://localhost:5000/"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

socket_manager = SocketManager(app=app)

__validated_token = "valid"
election_config = None
election_state = {"State":"OFF"}

def get_validated_token () -> str:
    """Getter for validated token"""

    global __validated_token

    return __validated_token

def set_validated_token(token) -> None:
    """
    Setter for validated token

    Keyword arguments:
    token -- validated token that voter used in NFC reader

    """

    global __validated_token

    __validated_token = token

@app.post('/api/election/config')
async def receive_config_from_gateway (config: dict) -> None:
    """
    Method for receiving election config from gateway

    Keyword arguments:
    config -- election config

    """

    global election_config

    # election_config = config

    await send_election_config_to_client(election_config)

async def send_election_config_to_client (config: dict) -> None:
    """
    Method for sending election config to client

    Keyword arguments:
    config -- election config

    """

    await app.sio.emit(
        'config', {
            "config": config
        }
    )

@app.post('/api/election/state')
async def receive_current_election_state_from_gateway (state: dict) -> None:
    """
    Method for receiving current election state from gateway

    Keyword arguments:
    config -- election config

    """

    global election_state

    # election_state = state

    await send_current_election_state_to_client(election_state)

async def send_current_election_state_to_client (state: dict) -> None:
    """
    Method for sending election config to client

    Keyword arguments:
    config -- election config

    """

    await app.sio.emit(
        'actual_state', {
            "state": state
        }
    )

async def send_token_to_gateway (token: str) -> None:
    """
    Method for sending token to gateway to validate it

    Keyword arguments:
    token -- token that voter used in NFC reader

    """

    r = requests.post(
        "http://" + os.environ['VOTING_SERVICE_PATH'] + "/api/token-validity",
        json = {'token': token}
    )

    if r.status_code == 200:
        await send_validated_token_to_client(token)
    else:
        await validation_of_token_failed()

async def send_validated_token_to_client (token: str) -> None:
    """
    Method for sending validated token to client

    Keyword arguments:
    token -- validated token that voter user

    """

    await app.sio.emit(
        'validated_token', {
            "data": 'valid',
            "message": "This token was successfully validated"
        }
    )

async def validation_of_token_failed () -> None:
    """
    Method for sending client a message that validation of token failed

    """

    await app.sio.emit(
        'validated_token', {
            "data": "",
            "message": "This token is not valid. Help."
        }
    )

async def send_vote_to_gateway (vote: dict, status_code=200) -> None:
    """
    Method for sending recieved vote to gateway. Backend send "success" to client
    if saving of vote was successfull.

    Keyword arguments:
    vote -- vote object that user created in his action

    """

    token = get_validated_token ()

    r = requests.post(
        "http://" + os.environ['VOTING_SERVICE_PATH'] + "/api/vote",
        json = {'token': token, 'vote': vote}
    )

    r.raise_for_status()


@app.post('/api/vote_generated', status_code=200)
async def vote (vote: dict) -> None:
    """
    Api method for recieving vote from client

    Keyword arguments:
    vote -- vote object that user created in his action

    """

    r = await send_vote_to_gateway(vote)


### This is for future usage, please keep it here, in final code, this won't be here :)

#######################################    TESTING
@app.get("/test_token_valid")
async def test_token_valid():
    await send_token_to_gateway("valid")

@app.get("/test_token_invalid")
async def test_token_invalid():
    await send_token_to_gateway("invalid")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=80)

