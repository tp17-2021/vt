
class BaseTicket(object):
    """ Base ticket class for saving vote data and preprocessing text """
    voting_data = {}

    def __init__(self, data: dict) -> None:
        """ 
        Constructor for saving vote data

        Keyword arguments:
        data -- Dictionary of data, which contains whole vote

         """
        self.voting_data = data['vote']
        self.voting_data_token = data


    def preprocessText(self, candidates: list, max_line_len: int) -> str:
        """
        Method for preprocessing text before printing into PDF.
        Text have to be manually cut with '-' to be in readable form.

        Keyword arguments:
        candidates -- List of candidates that will be printed
        max_line_len -- Maximal length of row which will be printed

        """
        string_candidates = ""

        if type(candidates) == list:
            for i in candidates:
                string_candidates += i
                string_candidates += '\n'
        else:
            string_candidates = candidates

        counter = 0
        string_candidates_broken_lines = ""
        for i in string_candidates:
            if i == '\n':
                counter = 0
                string_candidates_broken_lines += i
                continue
            else:
                if counter == max_line_len:
                    counter = 0
                    string_candidates_broken_lines += '-\n'
                    string_candidates_broken_lines += i
                else:
                    counter += 1
                    string_candidates_broken_lines += i

        return string_candidates_broken_lines
