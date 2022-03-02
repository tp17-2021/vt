import logging
import os
import sys

from fastapi import Body, FastAPI, status, HTTPException, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from fastapi_socketio import SocketManager
import uvicorn
import requests

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import logging

from electiersa import electiersa
# from src.schemas.votes import VotePartial
from src.PDF_creator.BaseTicket import BaseTicket
from src.PDF_creator.PresidentTicket import PresidentTicket
from src.PDF_creator.NationalTicket import NationalTicket
from src.PDF_creator.MunicipalTicket import MunicipalTicket

from src.schemas.votes import VotePartial


app = FastAPI(root_path=os.environ['ROOT_PATH'])

LOGGER = logging.getLogger(__name__)

START_STATE = 'start'

app.mount("/public", StaticFiles(directory="src/public"), name="public")

# origins = ["http://localhost:8079/", "http://localhost:5000/"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# host.docker.internal  - toto odoslne na cely pocitac a nie dockerovsky

socket_manager = SocketManager(app=app)

__validated_token = "valid"
election_config = None
election_state = 'inactive'

@app.get('/')
async def hello ():
    """ Sample testing endpoint """

    return {'message': 'Hello from VT backend!'}

def get_validated_token() -> str:
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


async def print_vote(vote: dict) -> None:
    """
    Method to print vote

    Keyword arguments:
    vote -- users vote in JSON format

    """

    try:
        ticket = NationalTicket(vote)
        ticket.create_pdf()

    except Exception as e:
        print('Print failed:', e)

    

async def receive_config_from_gateway(file: UploadFile = File(...)) -> None:
    """
    Method for receiving election config from gateway

    """
    
    config_file_path = os.path.join(os.getcwd(), './src/public/config.json')
    
    # use local config.json while in dev mode
    if  'VT_ONLY_DEV' in os.environ and os.environ['VT_ONLY_DEV'] == '1':
        with open(config_file_path, 'wb') as f, open('/code/tests/config.json', 'rb') as f2:
            f.write(f2.read())        
    
    else:
        r = requests.get(
            "http://" + os.environ['STATE_VECTOR_PATH'] + "/config/config.json",
        )


        with open(config_file_path, 'wb') as f:
            f.write(r.content)


@app.post('/api/election/state')
async def receive_current_election_state_from_gateway(state: dict) -> None:
    """
    Method for receiving current election state from gateway

    Keyword arguments:
    state -- current election state

    """

    global election_state

    election_state = state['status']

    # Download config from gateway if election just started
    if state == START_STATE:
        receive_config_from_gateway()

    await send_current_election_state_to_client(election_state)


async def send_current_election_state_to_client(state: dict) -> None:
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


def encrypt_message(data: dict):
    with open('/secret/private_key.txt', 'r') as f:
        my_private_key = f.read()

    with open('/idk_data/g_public_key.txt', 'r') as f:
        g_public_key = f.read()


    encrypted_data = electiersa.encrypt_vote(data, my_private_key, g_public_key)

    return encrypted_data


async def send_token_to_gateway(token: str) -> None:
    """
    Method for sending token to gateway to validate it

    Keyword arguments:
    token -- token that voter used in NFC reader

    """
    
    # dont valid token on G while dev mode
    if  'VT_ONLY_DEV' in os.environ and os.environ['VT_ONLY_DEV'] == '1':
        await send_validated_token_to_client(token)
        
        return

    encrypted_data = encrypt_message({'token': token})

    with open('/idk_data/my_id.txt', 'r') as f:
        my_id = f.read()

    r = requests.post(
        "http://" + os.environ['VOTING_SERVICE_PATH'] + "/api/token-validity",
        json={
            'payload': encrypted_data.__dict__,
            'voting_terminal_id': my_id,
        }
    )

    if r.status_code == 200:
        await send_validated_token_to_client(token)
    else:
        await validation_of_token_failed()


async def send_validated_token_to_client(token: str) -> None:
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


async def validation_of_token_failed() -> None:
    """
    Method for sending client a message that validation of token failed

    """

    await app.sio.emit(
        'validated_token', {
            "data": "",
            "message": "This token is not valid. Help."
        }
    )


async def send_vote_to_gateway(vote: dict, status_code=200) -> None:
    """
    Method for sending recieved vote to gateway. Backend send "success" to client
    if saving of vote was successfull.

    Keyword arguments:
    vote -- vote object that user created in his action

    """

    # skip while on dev mode
    if  'VT_ONLY_DEV' in os.environ and os.environ['VT_ONLY_DEV'] == '1':
        return

    token = get_validated_token()

    data = {
        'token': token,
        'vote': vote
    }

    await print_vote(vote)

    encrypted_data = encrypt_message(data)

    with open('/idk_data/my_id.txt', 'r') as f:
        my_id = f.read()

    r = requests.post(
        "http://" + os.environ['VOTING_SERVICE_PATH'] + "/api/vote",
        json={
            'payload': encrypted_data.__dict__,
            'voting_terminal_id': my_id,
        }
    )

    r.raise_for_status()


@app.post('/api/vote_generated', status_code=200)
async def vote(
    vote: VotePartial = Body(...),
) -> None:
    """
    Api method for recieving vote from client

    Keyword arguments:
    vote -- vote object that user created in his action

    """

    r = await send_vote_to_gateway(vote.__dict__)


@app.on_event("startup")
async def startup_event():
    """ Method that connect to gateway at start of running VT """
    private_key, public_key = electiersa.get_rsa_key_pair()
    with open('/secret/private_key.txt', 'w') as f:
        f.write(private_key)

    if  'VT_ONLY_DEV' in os.environ and os.environ['VT_ONLY_DEV'] == '1':
        with open('/idk_data/g_public_key.txt', 'w') as f:
            f.write(electiersa.get_rsa_key_pair()[1])

        with open('/idk_data/my_id.txt', 'w') as f:
            f.write(str('vtdev1'))
        
    else:
        r = requests.post(
            "http://" + os.environ['VOTING_PROCESS_MANAGER_PATH'] + '/register-vt',
            json={
                'public_key': public_key
            }
        )

        if r.status_code != 200:
            raise Exception("Not connected to gateway !!!")

        g_public_key = r.json()['gateway_public_key']
        my_id = r.json()['new_id']

        with open('/idk_data/g_public_key.txt', 'w') as f:
            f.write(g_public_key)

        with open('/idk_data/my_id.txt', 'w') as f:
            f.write(str(my_id))


# post method for recieving token from client
@app.post('/token', status_code=200)
async def token(
    token: str = Body(...),
) -> None:
    """
    Api method for recieving token from client

    Keyword arguments:
    token -- token that voter user

    """

    await send_token_to_gateway(token)


# This is for future usage, please keep it here, in final code, this won't be here :)

# TESTING
@app.get("/test_token_valid")
async def test_token_valid():
    await send_token_to_gateway("valid")


@app.get("/test_token_invalid")
async def test_token_invalid():
    await send_token_to_gateway("invalid")


@app.get("/get_config_from_gateway")
async def test_getting_config():
    await receive_config_from_gateway()



@app.get("/test_print")
async def test_print():
    data = {}
    data['title'] = "Volby do narodnej rady"
    data["party"] = "Smer - socialna demokracia"
    data["candidates"] = [
        '1. Marek Ceľuch',
        '2. Matúš StaŠ',
        '3. Lucia Janikova',
        '4. Lilbor Duda',
        '5. Denis Klenovic',
        '6. Timotej Kralik',
        '7. Jaro Erdelyi',
        '8. Voldemort Voldemort',
        '9. Neviem Neviem',
        ]

    await print_vote(data)

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=80)
