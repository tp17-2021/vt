from fpdf import FPDF
import qrcode
from PIL import Image

from src.PDF_creator.BaseTicket import BaseTicket


class PresidentTicket(BaseTicket):
    """ Class for ticket from vote with President candidate """

    def __init__(self, data: dict) -> None:
        """ 
        Constructor for saving vote data

        Keyword arguments:
        data -- Dictionary of data, which contains whole vote

         """
        super().__init__(data)


    def Create_pdf(self):
        """ Method for creating PDF file from vote """

        if 'src' in os.listdir():
            os.chdir("src/PDF_creator")

        pdf = FPDF('P', 'mm', (80, 50))
        pdf.set_auto_page_break(True, margin=5.0)
        pdf.add_page()

        pdf.add_font('slovak', '', "Calibri Regular.ttf", uni=True)
        pdf.add_font('slovakBold', '', "Calibri Bold.TTF", uni=True)

        pdf.set_font('slovak', '', 9)
        pdf.multi_cell(0, 0, self.voting_data['title'], align='L')

        pdf.set_xy(3, 15)
        pdf.set_font('slovakBold', '', 9)
        pdf.write(5, 'Kandidát:')

        pdf.set_xy(3, 20)
        pdf.set_font('slovak', "", 9)
        candidate_str = BaseTicket.preprocessText(
            self,
            self.voting_data['candidate'],
            21
        )
        pdf.multi_cell(0, 5, candidate_str)

        pdf.set_xy(45, 6)

        data_str = str(self.voting_data)
        img = qrcode.make(data_str)
        img.save("Temp/sample.png")
        pdf.image("Temp/sample.png", w=35, h=33)
        pdf.accept_page_break()

        pdf.output('PresidentTIcket.pdf', 'F')

        self.print_ticket('NationalPrincipalTIcket.pdf')
