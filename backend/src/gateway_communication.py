import os
import requests

import src.imports as imports
from src.imports import ElectionStates, app, get_validated_token, set_validated_token, sio

import src.utils
from src.utils import transform_vote_to_print, get_config, encrypt_message, prepare_printing_vote, reg_printer, print_ticket_out

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
            os.environ['HYPERTEXT_PROTOCOL'] + os.environ['STATE_VECTOR_PATH'] + "/config/config.json",
        )

        with open(config_file_path, 'wb') as f:
            f.write(r.content)


async def send_current_election_state_to_gateway() -> None:
    """
    Method for sending election state to gateway

    """

    if  'VT_ONLY_DEV' in os.environ and os.environ['VT_ONLY_DEV'] == '1':
        return

    # Emit event to gateway
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

    # dont valid token on G while dev mode
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
        os.environ['HYPERTEXT_PROTOCOL'] + os.environ['VOTING_SERVICE_PATH'] + "/api/token-validity",
        json={
            'payload': encrypted_data.__dict__,
            'voting_terminal_id': my_id,
        }
    )

    if r.status_code == 200:
        await change_state_and_send_to_frontend(ElectionStates.TOKEN_VALID)

        imports.__validated_token = token

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
    # skip while on dev mode

    if imports.registered_printer == False:
        await reg_printer()
        imports.registered_printer = True
    
    if  'VT_ONLY_DEV' in os.environ and os.environ['VT_ONLY_DEV'] == '1':

        token = get_validated_token()

        print_vote_ = await transform_vote_to_print(vote)
        printing_data = {
            'token': token,
            'vote': print_vote_
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
        os.environ['HYPERTEXT_PROTOCOL'] + os.environ['VOTING_SERVICE_PATH'] + "/api/vote",
        json={
            'payload': encrypted_data.__dict__,
            'voting_terminal_id': my_id,
        }
    )

    r.raise_for_status()

    print_vote_ = await transform_vote_to_print(vote)
    printing_data = {
        'token': token,
        'vote': print_vote_
    }

    await prepare_printing_vote(printing_data)
    await print_ticket_out()

