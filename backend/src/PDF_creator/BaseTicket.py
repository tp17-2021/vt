import qrcode
from fpdf import FPDF
from PIL import Image

class BaseTicket(object):
    """ Base ticket class for saving vote data and preprocess text """
    voting_data = {}

    def __init__ (self,data: dict) -> None:
        """ 
        Constructor for saving vote data
        
        Keyword arguments:
        data -- Dictionary of data, which contains whole vote

         """
        self.voting_data = data

    def preprocessText (self,candidates: list,max_line_len: int) -> None:
        """
        Method for preprocessing text before priting into PDF.
        Text have to be manully cut with '-' to be in readable form.

        Keyword arguments:
        candidates -- List of candidates that will be printed
        max_line_len -- Maximal length of row which will be printed
        
        """
        string_final =""

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
