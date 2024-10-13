import openpyxl

file_path_excel = 'C:/Users/79200/PycharmProjects/Курсовая/data/operations.xlsx '


def read_excel():
    wb = openpyxl.load_workbook(file_path_excel)
    sheet = wb.active
    data_excel = []
    headers = [cell.value for cell in sheet[1]]
    for row in sheet.iter_rows(min_row=2, values_only=True):
        data_excel.append(dict(zip(headers, row)))
    return data_excel
