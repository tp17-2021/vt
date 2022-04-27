# from fastapi import HTTPException
# import src.imports as imports
# from src.imports import ElectionStates, app

# from src.gateway_communication import receive_config_from_gateway

# async def send_current_election_state_to_frontend() -> None:
#     """
#     Method for sending election config to client

#     Keyword arguments:
#     config -- election config

#     """

#     await app.sio.emit(
#         'changed_election_state', {
#             "state": imports.election_state
#         }
#     )


# async def change_state_and_send_to_frontend(new_state: str) -> None:
#     """
#     Method for changing election state and sending it to client

#     """
#     # Continue only if state was changed
#     if new_state == imports.election_state:
#         return

#     if new_state == ElectionStates.TOKEN_VALID and imports.election_state == ElectionStates.ELECTIONS_NOT_STARTED:
#         raise HTTPException(status_code=400, detail='Election not started (2)')

#     if new_state == ElectionStates.TOKEN_NOT_VALID and imports.election_state == ElectionStates.ELECTIONS_NOT_STARTED:
#         raise HTTPException(status_code=400, detail='Election not started (3)')

#     # Do not change to waiting_for_scan if already is user casting to vote - fixes bug, if user scans NFC tag before waiting for NFC tag is shown
#     # if new_state == ElectionStates.WAITING_FOR_NFC_TAG and imports.election_state == ElectionStates.TOKEN_VALID:
#     #     return

#     # Does the state exist in enum?
#     if new_state not in [ ElectionStates.ELECTIONS_NOT_STARTED,ElectionStates.WAITING_FOR_NFC_TAG,
#                         ElectionStates.TOKEN_VALID, ElectionStates.TOKEN_NOT_VALID, 
#                         ElectionStates.VOTE_SUCCESS, ElectionStates.VOTE_ERROR ]:
#         print('Invalid state - ' + str(new_state))
#         raise HTTPException(status_code=400, detail='Invalid state - ' + str(new_state))

#     # Download config from gateway if election just started
#     if new_state == ElectionStates.WAITING_FOR_NFC_TAG and imports.election_state == ElectionStates.ELECTIONS_NOT_STARTED:
#         await receive_config_from_gateway()

#     print("Changed state to:", new_state)

#     imports.election_state = new_state

#     await send_current_election_state_to_frontend()
