import json
import os
import subprocess
import time
from electiersa import electiersa

from src.PDF_creator.NationalTicket import NationalTicket

def encrypt_message(data: dict):
    """
        Method for encrypting data with our private key and gateways public key

        Keyword arguments:
        data -- encrypting data 
    """
    with open('/secret/private_key.txt', 'r') as f:
        my_private_key = f.read()

    with open('/idk_data/g_public_key.txt', 'r') as f:
        g_public_key = f.read()


    encrypted_data = electiersa.encrypt_vote(data, my_private_key, g_public_key)

    return encrypted_data

def get_config():
    """
        Method for getting config
    """
    os.chdir('/code/')

    with open(os.path.join(os.getcwd(), 'src/public/config.json'), 'rb') as f:
        data = json.load(f)

    return data


async def reg_printer():
    """
        Method for registrating printer before first printing.
    """
    os.system('rc-service cupsd restart')

    # without this it is not working
    time.sleep(2)

    os.system(f'lpadmin -p TM- -v socket://{os.environ["PRINTER_IP_ADDRESS"]}/TM- -P /code/printer_driver/ppd/tm-ba-thermal-rastertotmtr-203.ppd -E')


async def print_ticket_out():
    """
        Method for printing ticket out. FINALY <3
    """
    command = "lpr -o TmxPaperCut=CutPerPage -P TM- /code/src/PDF_creator/NewTicket.pdf"
    subprocess.run(command, shell=True, check=True)

async def prepare_printing_vote(vote: dict) -> None:
    """
    Method for creating pdf with vote before printing

    Keyword arguments:
    vote -- users vote in JSON format

    """

    try:
        ticket = NationalTicket(vote)
        ticket.create_pdf()

    except Exception as e:
        print('Print failed:', e)

async def transform_vote_to_print(vote: dict) -> dict:
    """
    Method creating human readable vote from raw coded vote from VT.

    Keyword arguments:
    vote -- users vote in JSON format

    """

    data = get_config()
    
    res_dict = {}
    res_dict['title'] = "Voľby do národnej rady"
    res_dict["candidates"] = []
    res_dict["party"] = "---"

    for party in data["parties"]:
        if party["_id"] == vote["party_id"]:
            res_dict["party"] = party["name"]

            for candidate in party["candidates"]:
                if candidate["_id"] in vote["candidate_ids"]:
                    name = str(candidate["order"]) +". "+ candidate["first_name"] +" "+ candidate["last_name"]
                    res_dict["candidates"].append(name)


    return res_dict