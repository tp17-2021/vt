from fpdf import FPDF
import qrcode
from PIL import Image
import os
import subprocess

from src.PDF_creator.BaseTicket import BaseTicket

class NationalTicket(BaseTicket):
    """ Class for ticket from vote to National concil """

    def __init__(self,data: dict) -> None:
        """ 
        Constructor for saving vote data
        
        Keyword arguments:
        data -- Dictionary of data, which contains whole vote

        """
        super().__init__(data)


    def create_pdf(self):
        """ Method for creating PDF file from vote """

        if 'src' in os.listdir():
            os.chdir("src/PDF_creator")

        pdf = FPDF('P', 'mm', (80, 100))
        pdf.add_page()


        pdf.add_font('slovak', '', "Calibri Regular.ttf", uni=True)
        pdf.add_font('slovakBold', '', "Calibri Bold.TTF", uni=True)

        pdf.set_font('slovak', '', 9)
        pdf.multi_cell(0,0,self.voting_data['title'],align='C')

        pdf.set_xy(0,10)
        pdf.set_font('slovakBold','',9)
        pdf.write(5,'Strana:')

        pdf.set_xy(0,15)
        pdf.set_font('slovak',"", 9)
        party_str = BaseTicket.preprocessText(
            self,
            self.voting_data['party'],
            45
        )
        pdf.multi_cell(0,3,party_str)

        pdf.set_xy(0,22)
        pdf.set_font('slovakBold','',9)
        pdf.write(5,'Kandidáti:')

        pdf.set_xy(0,27)
        pdf.set_font('slovak','', 9)
        candidates = BaseTicket.preprocessText(
            self,
            self.voting_data['candidates'],
            30
        )
        pdf.multi_cell(40, 5,candidates)

        pdf.set_xy(43,22)

        data_str = str(self.voting_data_token)
        img = qrcode.make(data_str)
        img.save("Temp/sample.png")
        pdf.image("Temp/sample.png",w=30,h=30)

        pdf.output('NewTicket.pdf', 'F')

        os.chdir('../..')
