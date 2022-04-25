import os
import json
import pytest
import asyncio
import uvicorn
import requests
from requests_async import ASGISession
from httpx import AsyncClient
import requests_mock

from fastapi.testclient import TestClient
from unittest import mock

from src.PDF_creator.NationalTicket import NationalTicket
from src.utils import transform_vote_to_print

with mock.patch.dict(os.environ, os.environ):
    from src.main import app

@pytest.fixture
def client ():
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def mock_get_config(mocker):
    future = asyncio.Future()
    mocker.patch(
        'src.vote_transformer' + '.get_config', return_value=future)
    return 


@pytest.mark.asyncio
async def test_default():
    assert 1 == 1


@pytest.mark.asyncio
async def test_create_pdf():
    vote = {
        'token': 'valid',
        'vote': {
            'title': 'Voľby do národnej rady',
            'candidates': ['4. Peter Pčolinskýyyyyyyyyyyyyyyyyyyyyyyyy', '6. Adriana Pčolinská'],
            'party': 'SME RODINA'}
    }
    
    ticket_class = NationalTicket(vote)
    ticket_class.create_pdf()

    assert 'NewTicket.pdf' in os.listdir('tests')


@pytest.mark.asyncio
async def test_cut_lines_to_max_length():
    vote = {
        'token': 'valid',
        'vote': {
            'title': 'Voľby do národnej rady',
            'candidates': ['4. Peter Pčolinskýyyyyyyyyyyyyyyyyyyyyyyyy', '6. Adriana Pčolinská'],
            'party': 'SME RODINA'}
    }
    
    ticket_class = NationalTicket(vote)
    candidates_str = ticket_class.preprocessText(vote['vote']['candidates'],25)

    counter = 0
    for character in candidates_str:
        if character == '\n':
            if counter > 26:
                assert False
            else:
                counter = 0
        else:
            counter += 1


@pytest.mark.asyncio
async def test_create_vote_from_config(client):
    vote = {'party_id': 0, 'candidate_ids': [4, 3, 2, 1]}

    vote_to_print = {
        'title': 'Voľby do národnej rady',
         'candidates': ['2. Andrej Trnovec', '3. Marián Kňažko', '4. Richard Burkovský', '5. Miroslav Faktor'],
          'party': 'Slovenská ľudová strana Andreja Hlinku'
    }

    res = await transform_vote_to_print(vote)

    assert res == vote_to_print
