import os
import qrcode

from fpdf import FPDF

from src.PDF_creator.BaseTicket import BaseTicket

class MunicipalTicket(BaseTicket):
    """ Class for ticket from vote to Municipal local concil """

    def __init__(self, data: dict) -> None:
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
        pdf.multi_cell(0, 0, self.voting_data['title'], align='C')

        pdf.set_xy(3, 15)
        pdf.set_font('slovakBold', '', 9)
        pdf.write(5, 'Kandidát:')

        pdf.set_xy(3, 20)
        pdf.set_font('slovak', "", 9)
        head_candidate_str = BaseTicket.preprocessText(
            self,
            self.voting_data['candidate_head'],
            21
        )
        pdf.multi_cell(0, 5, head_candidate_str)

        pdf.set_xy(43, 15)
        pdf.set_font('slovakBold', '', 9)
        pdf.write(5, 'Poslanci:')

        pdf.set_xy(43, 20)
        pdf.set_font('slovak', '', 9)
        candidates = BaseTicket.preprocessText(
            self,
            self.voting_data['candidates'],
            21
        )
        pdf.multi_cell(35, 5, candidates)

        pdf.set_xy(2, 27)

        data_str = str(self.voting_data)
        img = qrcode.make(data_str)
        img.save("Temp/sample.jpg")
        pdf.image("Temp/sample.png", w=35, h=35)

        pdf.output('MinucipalTicket.jpg', 'F')

        self.print_ticket('MinucipalTicket.pdf')
