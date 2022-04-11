import qrcode
from fpdf import FPDF
from PIL import Image
from escpos.printer import Network
from pdf2image import convert_from_path


class BaseTicket(object):
    """ Base ticket class for saving vote data and preprocess text """
    voting_data = {}

    def __init__(self, data: dict) -> None:
        """ 
        Constructor for saving vote data

        Keyword arguments:
        data -- Dictionary of data, which contains whole vote

         """
        self.voting_data = data['vote']
        self.voting_data_token = data

    def print_ticket(self, path: str): 
        """ Method for creating PDF file from vote """

        
        images = convert_from_path(path)

        for i in range(len(images)):
            images[i].save('ticket.jpg', 'JPEG')

        printer = Network("192.168.192.168")
        printer.image('ticket.jpg')
        printer.cut()

    def preprocessText(self, candidates: list, max_line_len: int) -> str:
        """
        Method for preprocessing text before priting into PDF.
        Text have to be manully cut with '-' to be in readable form.

        Keyword arguments:
        candidates -- List of candidates that will be printed
        max_line_len -- Maximal length of row which will be printed

        """
        string_final = ""

        if type(candidates) == list:
            for i in candidates:
                string_final += i
                string_final += '\n'
        else:
            string_final = candidates

        counter = 0
        string_final_two = ""
        for i in string_final:
            if i == '\n':
                counter = 0
                string_final_two += i
                continue
            else:
                if counter == max_line_len:
                    counter = 0
                    string_final_two += '-\n'
                    string_final_two += i
                else:
                    counter += 1
                    string_final_two += i

        return string_final_two
