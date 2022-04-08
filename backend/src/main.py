import asyncio
from enum import Enum
import logging
import os
import sys
import json
import time
import subprocess

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
registered_printer = False

### ----gateway websocket----
import socketio

sio = socketio.AsyncClient(
    reconnection=True,
    reconnection_attempts=3,
    logger=True,
    engineio_logger=True
)

@sio.event
def connect():
    print("I'm connected! SID", sio.sid)

@sio.on('actual_state')
async def on_actual_state_message(data):
    print('recieved actual_state!', data)
    state = data['state']

    await change_state_and_send_to_frontend(ElectionStates.WAITING_FOR_NFC_TAG if(state == 'start') else ElectionStates.ELECTIONS_NOT_STARTED)
    await send_current_election_state_to_gateway()

### ----gateway websocket----

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



async def receive_config_from_gateway() -> None:
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

async def send_current_election_state_to_gateway() -> None:
    """
    Method for sending election state to gateway

    """

    global election_state, vt_id

    # Emit event to gateway
    print("emiting status", election_state)
    await sio.emit('vt_stauts',
        {
            'status': election_state,
            'vt_id': vt_id,
            'sid': sio.sid,
        }
    )


def encrypt_message(data: dict):
    with open('/secret/private_key.txt', 'r') as f:
        my_private_key = f.read()

    with open('/idk_data/g_public_key.txt', 'r') as f:
        g_public_key = f.read()


    encrypted_data = electiersa.encrypt_vote(data, my_private_key, g_public_key)

    return encrypted_data


async def change_state_and_send_to_frontend(new_state: str) -> None:
    """
    Method for changing election state and sending it to client
    """

    global election_state

    # # continue only if state was changed
    if new_state == election_state:
        return

    if new_state == ElectionStates.TOKEN_VALID and election_state == ElectionStates.ELECTIONS_NOT_STARTED:
        raise HTTPException(status_code=400, detail='Election not started (2)')

    if new_state == ElectionStates.TOKEN_NOT_VALID and election_state == ElectionStates.ELECTIONS_NOT_STARTED:
        raise HTTPException(status_code=400, detail='Election not started (3)')

    # do not change to waiting_for_scan if already is user casting to vote - fixes bug, if user scans NFC tag before waiting for NFC tag is shown
    # if new_state == ElectionStates.WAITING_FOR_NFC_TAG and election_state == ElectionStates.TOKEN_VALID:
    #     return

    # does the state exist in enum?
    if new_state not in [ElectionStates.ELECTIONS_NOT_STARTED, ElectionStates.WAITING_FOR_NFC_TAG, ElectionStates.TOKEN_VALID, ElectionStates.TOKEN_NOT_VALID, ElectionStates.VOTE_SUCCESS, ElectionStates.VOTE_ERROR]:
        print('Invalid state - ' + str(new_state))
        raise HTTPException(status_code=400, detail='Invalid state - ' + str(new_state))



    # Download config from gateway if election just started
    if new_state == ElectionStates.WAITING_FOR_NFC_TAG and election_state == ElectionStates.ELECTIONS_NOT_STARTED:
        await receive_config_from_gateway()

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
            await asyncio.sleep(5)
            if election_state == ElectionStates.TOKEN_NOT_VALID:
                await change_state_and_send_to_frontend(ElectionStates.ELECTIONS_NOT_STARTED)
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
        await asyncio.sleep(5)
        if election_state == ElectionStates.TOKEN_NOT_VALID:
            await change_state_and_send_to_frontend(ElectionStates.WAITING_FOR_NFC_TAG)

async def transform_vote_to_print(vote: dict) -> dict:

    with open(config_file_path, 'rb') as f:
        data = json.load(f)
        res_dict = {}
        res_dict['title'] = "Voľby do národnej rady"
        res_dict["candidates"] = []

        for party in data["parties"]:
            if party["party_number"] == vote["party_id"]:
                res_dict["party"] = party["name"]

                # print(party["candidates"])
                for i,candidate in enumerate(party["candidates"]):
                    # id_in_sequence = i+1 
                    if candidate["order"] in vote["candidate_ids"]:
                        name = str(candidate["order"]) +". "+ candidate["first_name"] +" "+ candidate["last_name"]
                        res_dict["candidates"].append(name)

    
    print(res_dict)
    return res_dict

async def send_vote_to_gateway(vote: dict, status_code=200) -> None:
    """
    Method for sending recieved vote to gateway. Backend send "success" to client
    if saving of vote was successfull.

    Keyword arguments:
    vote -- vote object that user created in his action

    """
    global registered_printer
    # skip while on dev mode
    if  'VT_ONLY_DEV' in os.environ and os.environ['VT_ONLY_DEV'] == '1':

        token = get_validated_token()
        print_vote_ = await transform_vote_to_print(vote)
        printing_data = {
            'token': token,
            'vote': print_vote_
        }
        await print_vote(printing_data)

        if registered_printer == False:
            await register_printer()
            registered_printer = True
        

        await print_ticket_out()

        return

    token = get_validated_token()

    data = {
        'token': token,
        'vote': vote
    }

    print_vote_ = await transform_vote_to_print(vote)
    printing_data = {
        'token': token,
        'vote': print_vote_
    }
    await print_vote(printing_data)

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
        if election_state == ElectionStates.VOTE_SUCCESS:
            await change_state_and_send_to_frontend(ElectionStates.WAITING_FOR_NFC_TAG)
    except Exception as e:
        print("/api/vote_generated - exception",  e)
        await change_state_and_send_to_frontend(ElectionStates.VOTE_ERROR)
        await asyncio.sleep(5)
        if election_state == ElectionStates.VOTE_ERROR:
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
            try:
                print('Error message:', r.json()['detail'])

                if r.json()['detail'] == 'Registration is disabled':
                    print("Can't register to gateway yet, sleeping for 5 seconds...")
                    time.sleep(5)
                    print('Stopping.')

                    sys.exit(1)

            except KeyError as e:
                print('This is NOT a register allowance related error')
                print('Response:', r.status_code, r.text)
                print('Stopping.')

                sys.exit(1)


        g_public_key = r.json()['gateway_public_key']
        vt_id = my_id = r.json()['new_id']

        with open('/idk_data/g_public_key.txt', 'w') as f:
            f.write(g_public_key)

        with open('/idk_data/my_id.txt', 'w') as f:
            f.write(str(my_id))

    # connect to gateway websocket
    websocket_host = 'http://' + os.environ['VOTING_PROCESS_MANAGER_HOST']
    print("host",websocket_host, "path", os.environ['VOTING_PROCESS_MANAGER_HOST_SOCKET_PATH'])
    await sio.connect(
        websocket_host,
        socketio_path = os.environ['VOTING_PROCESS_MANAGER_HOST_SOCKET_PATH'],
        transports=['polling']
    )

    await send_current_election_state_to_gateway()



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
    Used for testing purposes to unlock frontend
    """
    await change_state_and_send_to_frontend(ElectionStates.TOKEN_VALID)


@app.get("/test_token_invalid")
async def test_token_invalid():
    """
    TESTING - set election state to ElectionStates.TOKEN_NOT_VALID
    Used for testing purposes to lock frontend
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

@app.get("/get_register_printer")
async def register_printer():
    print('SOM TUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU')
    os.system('rc-service cupsd restart')

    time.sleep(2)

    os.system('lpadmin -p TM- -v socket://192.168.192.168/TM- -P /code/printer_driver/ppd/tm-ba-thermal-rastertotmtr-203.ppd -E')

@app.post('/api/election/state')
async def receive_current_election_state_from_gateway(state: dict) -> None:
    """
    Method for receiving current election state from gateway

    Keyword arguments:
    state -- current election state

    """
    print("-------------------", state['status'])
    await change_state_and_send_to_frontend(state['status'])



    
@app.get("/get_print_ticket")
async def print_ticket_out():
    command = "lpr -o TmxPaperCut=CutPerJob -P TM- /code/src/PDF_creator/NewTicket.pdf"
    subprocess.run(command, shell=True, check=True)

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=80)
