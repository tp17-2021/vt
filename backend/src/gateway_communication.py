from fastapi import HTTPException
import requests
import asyncio
import json
import os
# from src.frontend_communication import change_state_and_send_to_frontend

import src.imports as imports
from src.imports import ElectionStates, get_validated_token, sio, app

import src.utils
from src.utils import transform_vote_to_print, encrypt_message, prepare_printing_vote, reg_printer, print_ticket_out

async def receive_config_from_gateway() -> None:
    """ Method for receiving election config from gateway """

    config_file_path = os.path.join(os.getcwd(), './src/public/config.json')

    # Use local config.json while in dev mode
    if  'VT_ONLY_DEV' in os.environ and os.environ['VT_ONLY_DEV'] == '1':
        with open(config_file_path, 'wb') as f, open('/code/tests/config.json', 'rb') as f2:
            f.write(f2.read())
    else:
        r = requests.get(
            os.environ['STATE_VECTOR_PATH'] + "/config/config.json",
        )

        with open(config_file_path, 'wb') as f:
            f.write(r.content)


async def send_current_election_state_to_gateway() -> None:
    """ Method for sending election state to gateway """

    if  'VT_ONLY_DEV' in os.environ and os.environ['VT_ONLY_DEV'] == '1':
        return

    print("emiting status", imports.election_state)
    await sio.emit('vt_stauts',
        {
            'status': imports.election_state,
            'vt_id': imports.vt_id,
            'sid': sio.sid,
        }
    )


async def send_token_to_gateway(token: str) -> None:
    """
    Method for sending token to gateway to validate it

    Keyword arguments:
    token -- token that voter used in NFC reader

    """
    # Dont valid token on G while dev mode
    if  'VT_ONLY_DEV' in os.environ and os.environ['VT_ONLY_DEV'] == '1':
        if token == 'invalid':
            await change_state_and_send_to_frontend(ElectionStates.TOKEN_NOT_VALID)
            await asyncio.sleep(5)
            if imports.election_state == ElectionStates.TOKEN_NOT_VALID:
                await change_state_and_send_to_frontend(ElectionStates.ELECTIONS_NOT_STARTED)
        else:
            await change_state_and_send_to_frontend(ElectionStates.TOKEN_VALID)
        return

    encrypted_data = encrypt_message({'token': token})

    with open('/idk_data/my_id.txt', 'r') as f:
        my_id = f.read()

    r = requests.post(
        os.environ['VOTING_SERVICE_PATH'] + "/api/token-validity",
        json={
            'payload': encrypted_data.__dict__,
            'voting_terminal_id': my_id,
        }
    )

    if r.status_code == 200:
        await change_state_and_send_to_frontend(ElectionStates.TOKEN_VALID)

        imports.validated_token = token
    else:
        await change_state_and_send_to_frontend(ElectionStates.TOKEN_NOT_VALID)
        await asyncio.sleep(5)
        if imports.election_state == ElectionStates.TOKEN_NOT_VALID:
            await change_state_and_send_to_frontend(ElectionStates.WAITING_FOR_NFC_TAG)


async def send_vote_to_gateway(vote: dict, status_code=200) -> None:
    """
    Method for sending recieved vote to gateway. Backend send "success" to client
    if saving of vote was successfull.

    Keyword arguments:
    vote -- vote object that user created in his action

    """
    # Skip while on dev mode
    if imports.registered_printer == False:
        await reg_printer()
        imports.registered_printer = True
    
    if  'VT_ONLY_DEV' in os.environ and os.environ['VT_ONLY_DEV'] == '1':
        token = get_validated_token()

        processed_printing_vote = await transform_vote_to_print(vote)
        printing_data = {
            'token': token,
            'vote': processed_printing_vote
        }

        await prepare_printing_vote(printing_data)
        await print_ticket_out()

        return

    token = get_validated_token()

    data = {
        'token': token,
        'vote': vote
    }

    encrypted_data = encrypt_message(data)

    with open('/idk_data/my_id.txt', 'r') as f:
        my_id = f.read()

    r = requests.post(
        os.environ['VOTING_SERVICE_PATH'] + "/api/vote",
        json={
            'payload': encrypted_data.__dict__,
            'voting_terminal_id': my_id,
        }
    )

    r.raise_for_status()

    processed_printing_vote = await transform_vote_to_print(vote)
    printing_data = {
        'token': token,
        'vote': processed_printing_vote
    }

    await prepare_printing_vote(printing_data)
    await print_ticket_out()


async def send_current_election_state_to_frontend() -> None:
    """
    Method for sending election config to client

    Keyword arguments:
    config -- election config

    """

    await app.sio.emit(
        'changed_election_state', {
            "state": imports.election_state
        }
    )


async def change_state_and_send_to_frontend(new_state: str) -> None:
    """
    Method for changing election state and sending it to client

    """

    global imports

    print("new_state", new_state)

    # Continue only if state was changed
    if new_state == imports.election_state:
        return

    if new_state == ElectionStates.TOKEN_VALID and imports.election_state == ElectionStates.ELECTIONS_NOT_STARTED:
        raise HTTPException(status_code=400, detail='Election not started (2)')

    if new_state == ElectionStates.TOKEN_NOT_VALID and imports.election_state == ElectionStates.ELECTIONS_NOT_STARTED:
        raise HTTPException(status_code=400, detail='Election not started (3)')

    # Do not change to waiting_for_scan if already is user casting to vote - fixes bug, if user scans NFC tag before waiting for NFC tag is shown
    # if new_state == ElectionStates.WAITING_FOR_NFC_TAG and imports.election_state == ElectionStates.TOKEN_VALID:
    #     return

    # Does the state exist in enum?
    if new_state not in [ ElectionStates.ELECTIONS_NOT_STARTED,ElectionStates.WAITING_FOR_NFC_TAG,
                        ElectionStates.TOKEN_VALID, ElectionStates.TOKEN_NOT_VALID, 
                        ElectionStates.VOTE_SUCCESS, ElectionStates.VOTE_ERROR, ElectionStates.DISCONNECTED ]:
        print('Invalid state - ' + str(new_state))
        raise HTTPException(status_code=400, detail='Invalid state - ' + str(new_state))

    # Download config from gateway if election just started
    if new_state == ElectionStates.WAITING_FOR_NFC_TAG and imports.election_state == ElectionStates.ELECTIONS_NOT_STARTED:
        await receive_config_from_gateway()

    print("Changed state to:", new_state)

    imports.election_state = new_state

    await send_current_election_state_to_frontend()
