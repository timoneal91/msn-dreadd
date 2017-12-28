import xlsxwriter
import os
import re
from datetime import datetime
from os import path

from app.parser import Parser
from app.writer import Writer


class App:
    DATE_FORMAT = '%Y%m%d'

    def __init__(self, root_directory):
        if not path.isdir(root_directory):
            raise Exception(f'Cannot open {root_directory}, it does not exist!')

        self.root = root_directory
        self.target_subdirectories = []
        self.files_to_process = []
        self.raw_data = []

    # noinspection PyBroadException
    def run(self):

        print('Collecting files to process')

        self.populate_files_to_process()

        print('Processing collected files')

        for file in self.files_to_process:

            # noinspection PyBroadException
            try:
                p = Parser(file, App.DATE_FORMAT)
                p.parse()

                # accumulate the data
                self.raw_data.append(p.data)

            except Exception as ex:
                print(f'Failed to parse: {ex}')

        print('Grouping data by subject')

        grouped_data = {}

        for data in sorted(self.raw_data, key=lambda k: k['date']):
            subject = data['subject']
            if subject not in grouped_data:
                grouped_data[subject] = []

            grouped_data[subject].append(data)

        # create the output location
        output_location = 'msn-dreadd-output_{}'.format(datetime.now().strftime('%Y%m%d-%H%M%S'))

        output_abs_path = path.join(self.root, output_location)

        os.makedirs(output_abs_path)

        print(f'Exporting data to:\n{output_abs_path}')

        for key, val in grouped_data.items():
            xlsx_file = 'subject_{}.xlsx'.format(key)
            xlsx_abs_path = path.join(output_abs_path, xlsx_file)

            try:
                Writer(xlsx_abs_path, val).write()

                print(f'Exported subject data to: {xlsx_abs_path}')
            except Exception as ex:
                print(f'Failed to write: {ex}')

        print('Processing complete!')

    def populate_files_to_process(self):

        print(self.root)

        # from the root, we want to work in directories named like '20170501' (YearMonthDay)
        for sub in [path.join(self.root, s) for s in os.listdir(self.root) if self.is_valid_root_subdirectory(s)]:

            # we only want to work on dirs
            if not path.isdir(sub):
                continue

            print(f'\t> {sub}')

            # sub directories, each for a subject
            for sub2 in [path.join(sub, s2)
                         for s2 in os.listdir(sub)
                         if re.match(r'singlesubjects_', s2, re.I)]:

                # we only want to work on dirs
                if not path.isdir(sub2):
                    continue

                print(f'\t\t> {sub2}')

                for item in [path.join(sub2, i)
                             for i in os.listdir(sub2)
                             if re.compile(r'collected$', re.I).search(i) is not None]:
                    print(f'\t\t\t> {item}')

                    self.files_to_process.append(item)

    # noinspection PyMethodMayBeStatic
    def is_valid_root_subdirectory(self, name):
        """
        This is used to make sure a root directory's sub directory is named as a date
        """
        # noinspection PyBroadException
        try:
            _ = datetime.strptime(name, App.DATE_FORMAT)
            return True
        except ValueError:
            return False
