import re
from datetime import datetime
from os import path


class Parser:
    TOKEN_DRUG_RIGHT_PRESSES = 1
    TOKEN_DRUG_LEFT_PRESSES = 2
    TOKEN_NON_DRUG_RIGHT_PRESSES = 3
    TOKEN_NON_DRUG_LEFT_PRESSES = 4

    def __init__(self, file, date_format):

        if not path.isfile(file):
            raise Exception(f'Cannot process: {file}, it is not a file!')

        self.file = file
        self.subject = None
        self.drug_right_presses = []
        self.drug_left_presses = []
        self.non_drug_right_presses = []
        self.non_drug_left_presses = []

        try:
            date_str = str(path.basename(path.normpath(self.file)).split('_')[0])
            self.date = datetime.strptime(date_str, date_format)
        except Exception:
            raise

    @property
    def data(self):
        return {'subject': self.subject,
                'date': self.date,
                'drug_right_presses': self.drug_right_presses,
                'drug_left_presses': self.drug_left_presses,
                'non_drug_right_presses': self.non_drug_right_presses,
                'non_drug_left_presses': self.non_drug_left_presses}

    def parse(self):
        print(f'Parsing file: {self.file}')

        current_token = None

        with open(self.file, 'r') as f:
            for line in f:

                # we may or may not use this, depending on tokens
                maybe_val = self.extract_int(line)

                # extract subject
                if re.match('^subject:', line, re.I):
                    if maybe_val is not None:
                        self.subject = maybe_val
                    continue

                # extract date
                if re.match('^date:', line, re.I):
                    # TODO
                    continue

                # set token for DRP
                if re.match('^drugrightpresses', line, re.I):
                    current_token = Parser.TOKEN_DRUG_RIGHT_PRESSES
                    continue

                # set token for DLP
                if re.match('^drugleftpresses', line, re.I):
                    current_token = Parser.TOKEN_DRUG_LEFT_PRESSES
                    continue

                # set token for NDRP
                if re.match('^nondrugrightpresses', line, re.I):
                    current_token = Parser.TOKEN_NON_DRUG_RIGHT_PRESSES
                    continue

                # set token for NDLP
                if re.match('^nondrugleftpresses', line, re.I):
                    current_token = Parser.TOKEN_NON_DRUG_LEFT_PRESSES
                    continue

                # check for end
                if re.match('^binneddrugrightpresses', line, re.I):
                    break

                # gather data, if a token is active
                if current_token == Parser.TOKEN_DRUG_RIGHT_PRESSES:
                    if maybe_val is not None:
                        self.drug_right_presses.append(maybe_val)
                    continue
                elif current_token == Parser.TOKEN_DRUG_LEFT_PRESSES:
                    if maybe_val is not None:
                        self.drug_left_presses.append(maybe_val)
                    continue
                elif current_token == Parser.TOKEN_NON_DRUG_RIGHT_PRESSES:
                    if maybe_val is not None:
                        self.non_drug_right_presses.append(maybe_val)
                    continue
                elif current_token == Parser.TOKEN_NON_DRUG_LEFT_PRESSES:
                    if maybe_val is not None:
                        self.non_drug_left_presses.append(maybe_val)
                    continue

        print('Done parsing file')

    # noinspection PyMethodMayBeStatic
    def extract_int(self, string):
        # noinspection PyBroadException
        try:
            return int(re.search(r'\d+', string).group())
        except Exception:
            return None
