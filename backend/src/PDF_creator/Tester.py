from fpdf import FPDF
import qrcode
from PIL import Image

from BaseTicket import BaseTicket
from NationalTicket import NationalTicket
# from MunicipalTicket import MunicipalTicket
# from PresidentTicket import PresidentTicket


###########################################################################

data = {}
data['title'] = "Voľby do národnej rady"
data["party"] = "Smer - sociálna demokracia"
data["candidates"] = [
    '1. Marek Ceľuch',
    '2. Matúš Staš',
    '3. Lucia Janíková',
    '4. Lilbor Duda',
    '5. Denis Klenovič',
    '6. Timotej Králik',
    '7. Jaro Erdelyi',
    '8. Soňa Zwang',
    '9. Neviem Neviem',
    ]

o = NationalTicket(data)
o.create_pdf()


###########################################################################

# data = {}
# data['title'] = "Komunálne voľby 2024"
# data["candidate_head"] = "3. Matúš Vallo"
# data["candidates"] = [
#     '1. Marek Ceľuch',
#     '2. Matúš Staš',
#     '3. Lucia Janíková',
#     '4. Lilbor Duda',
#     '5. Denis Klenovič',
#     '6. Timotej Králik',
#     '7. Jaro Erdelyi',
#     '8. Soňa Zwang',
#     '9. Neviem Neviem',
#     ]


# o = MunicipalTicket(data)
# o.create_pdf()

###########################################################################

# data = {}
# data['title'] = "Prezidentské voľby 2024"
# data["candidate"] = "2. Zuzana Čaputová"

# o = PresidentTicket(data)
# o.Create_pdf()
