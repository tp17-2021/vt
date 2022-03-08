import asyncio
from enum import Enum
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


# enum for election_states
class ElectionStates(object):
    ELECTIONS_NOT_STARTED = 'elections_not_started'     # elections are disabled
    WAITING_FOR_NFC_TAG = 'waiting_for_scan'            # elections are enabled and waiting for NFC tag to be scanned
    TOKEN_VALID = 'token_valid'                         # NFC tag was scanned and is valid - user is currently choosing their vote
    TOKEN_NOT_VALID = 'token_not_valid'                 # NFC tag was scanned, but is not valid
    VOTE_SUCCESS = 'vote_success'                       # (Only if TOKEN_VALID) Vote was successfully casted to the gateway
    VOTE_ERROR = 'vote_error'                           # (Only if TOKEN_VALID) There was an error sending the vote to gateway


socket_manager = SocketManager(app=app)

__validated_token = "valid"
election_config = None
election_state = 'inactive'
vt_id = None


###--------------
import socketio

sio = socketio.Client()
# connect to gateway websocket    
websocket_host = 'http://' + os.environ['VOTING_PROCESS_MANAGER_HOST']
print("host",websocket_host, "path", os.environ['VOTING_PROCESS_MANAGER_HOST_SOCKET_PATH'])
sio.connect(websocket_host, socketio_path = os.environ['VOTING_PROCESS_MANAGER_HOST_SOCKET_PATH'])

@sio.event
def connect():
    print("I'm connected! SID", sio.sid)

@sio.on('actual_state')
async def on_actual_state_message(data):
    global election_state

    print('recieved actual_state!', data)
    state = data['state']

    # save current status of voting terminal
    election_state = 'active' if(state == START_STATE) else 'inactive'

    # Download config from gateway if election just started
    if state == START_STATE:
        receive_config_from_gateway()

    await send_current_election_state_to_frontend(election_state)

    # Emit event to gateway
    print("emiting status", election_state)
    sio.emit('vt_stauts',
        {
            'status': election_state,
            'vt_id': vt_id,
            'sid': sio.sid,
        }
    )

###-------------

election_state = ElectionStates.ELECTIONS_NOT_STARTED


@app.sio.on('join')
async def handle_join(sid, *args, **kwargs):
    await send_current_election_state_to_frontend()

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



async def send_current_election_state_to_frontend() -> None:
    """
    Method for sending election config to client

    Keyword arguments:
    config -- election config

    """

    global election_state

    await app.sio.emit(
        'changed_election_state', {
            "state": election_state
        }
    )


def encrypt_message(data: dict):
    with open('/secret/private_key.txt', 'r') as f:
        my_private_key = f.read()

    with open('/idk_data/g_public_key.txt', 'r') as f:
        g_public_key = f.read()


    encrypted_data = electiersa.encrypt_vote(data, my_private_key, g_public_key)

    return encrypted_data
  

async def change_state_and_send_to_frontend(new_state: ElectionStates) -> None:
    """
    Method for changing election state and sending it to client
    """

    global election_state
    
    # continue only if state was changed
    if new_state == election_state:
        return

    if new_state == ElectionStates.TOKEN_VALID and election_state == ElectionStates.ELECTIONS_NOT_STARTED:
        raise HTTPException(status_code=400, detail='Election not started (2)')

    if new_state == ElectionStates.TOKEN_NOT_VALID and election_state == ElectionStates.ELECTIONS_NOT_STARTED:
        raise HTTPException(status_code=400, detail='Election not started (3)')

    if new_state not in [ElectionStates.ELECTIONS_NOT_STARTED, ElectionStates.WAITING_FOR_NFC_TAG, ElectionStates.TOKEN_VALID, ElectionStates.TOKEN_NOT_VALID, ElectionStates.VOTE_SUCCESS, ElectionStates.VOTE_ERROR]:
        print('Invalid state - ' + str(new_state))
        raise HTTPException(status_code=400, detail='Invalid state - ' + str(new_state))

    
    
    # Download config from gateway if election just started
    if new_state == ElectionStates.WAITING_FOR_NFC_TAG and election_state == ElectionStates.ELECTIONS_NOT_STARTED:
        receive_config_from_gateway()

    print("Changed state to:", new_state)
    election_state = new_state

    await send_current_election_state_to_frontend()


async def send_token_to_gateway(token: str) -> None:
    """
    Method for sending token to gateway to validate it

    Keyword arguments:
    token -- token that voter used in NFC reader

    """
    global __validated_token
    
    # dont valid token on G while dev mode
    if  'VT_ONLY_DEV' in os.environ and os.environ['VT_ONLY_DEV'] == '1':
        if token == 'invalid':
            await change_state_and_send_to_frontend(ElectionStates.TOKEN_NOT_VALID)
        else:
            await change_state_and_send_to_frontend(ElectionStates.TOKEN_VALID)
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
        await change_state_and_send_to_frontend(ElectionStates.TOKEN_VALID)

        __validated_token = token

    else:
        await change_state_and_send_to_frontend(ElectionStates.TOKEN_NOT_VALID)


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
    Api method for recieving vote from fronend

    Keyword arguments:
    vote -- vote object that user created in his action

    """

    if election_state == ElectionStates.ELECTIONS_NOT_STARTED:
        raise HTTPException(status_code=400, detail='Election not started (1)')

    if election_state != ElectionStates.TOKEN_VALID:
        raise HTTPException(status_code=400, detail='Token not valid')

    try:
        await send_vote_to_gateway(vote.__dict__)
        # raise ValueError("Simulated error")
        await change_state_and_send_to_frontend(ElectionStates.VOTE_SUCCESS)
        await asyncio.sleep(5)
        await change_state_and_send_to_frontend(ElectionStates.WAITING_FOR_NFC_TAG)
    except Exception as e:
        print("/api/vote_generated - exception",  e)
        await change_state_and_send_to_frontend(ElectionStates.VOTE_ERROR)
        await asyncio.sleep(5)
        await change_state_and_send_to_frontend(ElectionStates.WAITING_FOR_NFC_TAG)

    

    


@app.on_event("startup")
async def startup_event():
    """ Method that connect to gateway at start of running VT """
    global vt_id

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
        vt_id = my_id = r.json()['new_id']

        with open('/idk_data/g_public_key.txt', 'w') as f:
            f.write(g_public_key)

        with open('/idk_data/my_id.txt', 'w') as f:
            f.write(str(my_id))
    

    # Emit event to gateway
    sio.emit('vt_stauts',
        {
            'status': election_state,
            'vt_id': vt_id,
            'sid': sio.sid,
        }
    )



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
    """
    TESTING - set election state to ElectionStates.TOKEN_VALID
    """
    await change_state_and_send_to_frontend(ElectionStates.TOKEN_VALID)


@app.get("/test_token_invalid")
async def test_token_invalid():
    """
    TESTING - set election state to ElectionStates.TOKEN_NOT_VALID
    """
    await change_state_and_send_to_frontend(ElectionStates.TOKEN_NOT_VALID)

@app.get("/test_election_start")
async def test_election_start():
    """
    TESTING - set election state to ElectionStates.WAITING_FOR_NFC_TAG
    """
    await change_state_and_send_to_frontend(ElectionStates.WAITING_FOR_NFC_TAG)

@app.get("/test_election_stop")
async def test_election_stop():
    """
    TESTING - set election state to ElectionStates.ELECTIONS_NOT_STARTED
    """
    await change_state_and_send_to_frontend(ElectionStates.ELECTIONS_NOT_STARTED)


@app.get("/get_config_from_gateway")
async def test_getting_config():
    await receive_config_from_gateway()

    
@app.post('/api/election/state')
async def receive_current_election_state_from_gateway(state: dict) -> None:
    """
    Method for receiving current election state from gateway

    Keyword arguments:
    state -- current election state

    """
    print("-------------------", state['status'])
    await change_state_and_send_to_frontend(state['status'])



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
