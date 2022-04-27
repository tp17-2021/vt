import asyncio
import signal
import os
import sys
import json
import time
import uvicorn
import requests

import src.imports as imports
from src.imports import *

from electiersa import electiersa

import src.utils
from src.utils import get_config

import src.schemas.votes
from src.schemas.votes import VotePartial

# import src.frontend_communication
# from src.frontend_communication import send_current_election_state_to_frontend, change_state_and_send_to_frontend

import src.gateway_communication
from src.gateway_communication import receive_config_from_gateway, send_current_election_state_to_gateway, \
                                        send_token_to_gateway, send_vote_to_gateway, \
                                        send_current_election_state_to_frontend, \
                                        change_state_and_send_to_frontend

socket_manager = SocketManager(app=app)

imports.validated_token = "valid"
election_config = None
imports.election_state = 'inactive'
imports.vt_id = None
imports.registered_printer = False

@sio.event
def connect():
    """ Hello world """
    print("I'm connected! SID", sio.sid)


# Restart VT beckend on socket disconnect
@sio.event
async def disconnect():
    print("I'm disconnected from G WS!")
    await change_state_and_send_to_frontend(ElectionStates.DISCONNECTED)
    os.kill(os.getpid(), signal.SIGINT)

@sio.on('actual_state')
async def on_actual_state_message(data):
    """ Method for communicating actual election state of VT backend to gateway and frontend """
    print('recieved actual_state!', data)
    state = data['state']

    await change_state_and_send_to_frontend(ElectionStates.WAITING_FOR_NFC_TAG if(state == 'start') else ElectionStates.ELECTIONS_NOT_STARTED)
    await send_current_election_state_to_gateway()


@app.sio.on('join')
async def handle_join(sid, *args, **kwargs):
    """ Method for sending info to frontend about connecting gateway with frontend """
    await send_current_election_state_to_frontend()


@app.get('/')
async def hello ():
    """ Sample testing endpoint """

    return {'message': 'Hello from VT backend!'}


@app.post('/api/vote_generated', status_code=200)
async def vote(
    vote: VotePartial = Body(...),
) -> None:
    """
    Api method for recieving vote from fronend

    Keyword arguments:
    vote -- vote object that user created in his action

    """

    if imports.election_state == ElectionStates.ELECTIONS_NOT_STARTED:
        raise HTTPException(status_code=400, detail='Election not started (1)')

    if imports.election_state != ElectionStates.TOKEN_VALID:
        raise HTTPException(status_code=400, detail='Token not valid')

    try:
        await send_vote_to_gateway(vote.__dict__)
        await change_state_and_send_to_frontend(ElectionStates.VOTE_SUCCESS)
        await asyncio.sleep(5)
        if imports.election_state == ElectionStates.VOTE_SUCCESS:
            await change_state_and_send_to_frontend(ElectionStates.WAITING_FOR_NFC_TAG)

    except Exception as e:
        print("/api/vote_generated - exception", e)
        await change_state_and_send_to_frontend(ElectionStates.VOTE_ERROR)
        await asyncio.sleep(5)
        if imports.election_state == ElectionStates.VOTE_ERROR:
            await change_state_and_send_to_frontend(ElectionStates.WAITING_FOR_NFC_TAG)


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
            
        imports.election_state = ElectionStates.WAITING_FOR_NFC_TAG
    else:
        r = requests.post(
            os.environ['VOTING_PROCESS_MANAGER_PATH'] + '/register-vt',
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
        imports.vt_id = my_id = r.json()['new_id']

        with open('/idk_data/g_public_key.txt', 'w') as f:
            f.write(g_public_key)

        with open('/idk_data/my_id.txt', 'w') as f:
            f.write(str(my_id))

        websocket_host = os.environ['VOTING_PROCESS_MANAGER_HOST']
        print("host",websocket_host, "path", os.environ['VOTING_PROCESS_MANAGER_HOST_SOCKET_PATH'])
        await sio.connect(
            websocket_host,
            socketio_path = os.environ['VOTING_PROCESS_MANAGER_HOST_SOCKET_PATH'],
            transports=['polling']
        )
        
    await check_waiting_for_tag()
    await receive_config_from_gateway()
    await send_current_election_state_to_gateway()


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


@app.post('/api/election/state')
async def receive_current_election_state_from_gateway(state: dict) -> None:
    """
    Method for receiving current election state from gateway

    Keyword arguments:
    state -- current election state

    """
    await change_state_and_send_to_frontend(state['status'])


@repeat_every(seconds=5)
async def check_waiting_for_tag() -> None:
    """ 
    DEVELOPING USAGE - This method approve user to go voting even without NFC reader

    """
    if  'DONT_WAIT_FOR_TOKEN' in os.environ and os.environ['DONT_WAIT_FOR_TOKEN'] == '1' and imports.election_state == ElectionStates.WAITING_FOR_NFC_TAG:
        # await test_token_valid()
        print('TOFO valid token')


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=80)
