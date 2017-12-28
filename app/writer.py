import xlsxwriter


class Writer:
    def __init__(self, path, data):
        self.path = path
        self.data = data

    def write(self):
        workbook = xlsxwriter.Workbook(self.path)

        # each iteration is a date
        for data in self.data:
            # noinspection PyUnusedLocal
            row = 0
            col = 0

            worksheet = workbook.add_worksheet(data['date'].strftime('%Y%m%d'))

            worksheet.write(0, 0, 'DrugRightPresses')
            worksheet.write(0, 1, 'DrugLeftPresses')
            worksheet.write(0, 2, 'NonDrugRightPresses')
            worksheet.write(0, 3, 'NonDrugLeftPresses')

            row = 1
            for item in data['drug_right_presses']:
                worksheet.write(row, col, item)
                row += 1

            row = 1
            col = 1
            for item in data['drug_left_presses']:
                worksheet.write(row, col, item)
                row += 1

            row = 1
            col = 2
            for item in data['non_drug_right_presses']:
                worksheet.write(row, col, item)
                row += 1

            row = 1
            col = 3
            for item in data['non_drug_left_presses']:
                worksheet.write(row, col, item)
                row += 1

        workbook.close()
