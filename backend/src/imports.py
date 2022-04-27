import os
import socketio

from enum import Enum
from fastapi import Body, FastAPI, status, HTTPException, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from fastapi_socketio import SocketManager
from fastapi_utils.tasks import repeat_every

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from electiersa import electiersa

app = FastAPI(root_path=os.environ['ROOT_PATH'])
app.mount("/public", StaticFiles(directory="src/public"), name="public")

class ElectionStates(object):
    ELECTIONS_NOT_STARTED = 'elections_not_started'     # Elections are disabled
    WAITING_FOR_NFC_TAG = 'waiting_for_scan'            # Elections are enabled and waiting for NFC tag to be scanned
    TOKEN_VALID = 'token_valid'                         # NFC tag was scanned and is valid - user is currently choosing their vote
    TOKEN_NOT_VALID = 'token_not_valid'                 # NFC tag was scanned, but is not valid
    VOTE_SUCCESS = 'vote_success'                       # (Only if TOKEN_VALID) Vote was successfully casted to the gateway
    VOTE_ERROR = 'vote_error'                           # (Only if TOKEN_VALID) There was an error sending the vote to gateway

election_state = ElectionStates.ELECTIONS_NOT_STARTED

vt_id = None
__validated_token = "valid"
registered_printer = False

sio = socketio.AsyncClient(
    reconnection=True,
    reconnection_attempts=3,
    logger=True,
    engineio_logger=True
)

def get_validated_token() -> str:
    """ Getter for validated token """

    return __validated_token


def set_validated_token(token) -> None:
    """
    Setter for validated token

    Keyword arguments:
    token -- validated token that voter used in NFC reader

    """

    __validated_token = token
