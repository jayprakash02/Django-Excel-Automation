from django.core.mail import send_mail
from django.template.loader import render_to_string
import threading

import pandas as pd

from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import Workbook
from openpyxl.styles import Alignment


class SpreadsheetSnippets(object):
    def __init__(self, data,service):
        self.data = data
        self.service = service
        threading.Thread.__init__(self)

    def create(self, title):
        service = self.service
        # [START sheets_create]
        spreadsheet = {
            'properties': {
                'title': title
            }
        }
        spreadsheet = service.spreadsheets().create(body=spreadsheet,
                                            fields='spreadsheetId').execute()
        # [END sheets_create]
        return spreadsheet.get('spreadsheetId')

    def run(self):
        pass

class ExcelGenLF(threading.Thread):

    def __init__(self, data):
        threading.Thread.__init__(self)
        self.data = data

    def run(self):
        df = pd.DataFrame(self.data)

        wb = Workbook()
        ws = wb.active

        for r in dataframe_to_rows(df, index=True, header=True):
            ws.append(r)

        ws.delete_cols(1)
        ws.merge_cells('A1:B1')
        ws.merge_cells('A3:B3')

        ws.merge_cells('C1:D1')
        ws.merge_cells('C3:D3')

        ws.merge_cells('E1:F1')
        ws.merge_cells('E3:F3')

        ws.merge_cells('G1:H1')
        ws.merge_cells('G3:H3')

        wb.save("pandas_openpyxl.xlsx")

class ExcelGenDQ(threading.Thread):

    def __init__(self, data):
        threading.Thread.__init__(self)
        self.data = data

    def run(self):
        df = pd.DataFrame(self.data)

        wb = Workbook()
        ws = wb.active

        for r in dataframe_to_rows(df, index=True, header=True):
            ws.append(r)

        ws.delete_cols(1)

        ws.merge_cells('C3:C8')
        

        wb.save("pandas_openpyxl.xlsx")


class EmailThread(threading.Thread):

    def __init__(self, data):
        threading.Thread.__init__(self)
        self.data = data

    def run(self):
        html_message = render_to_string(
            'html_message.html', {'data': self.data}
        )
        send_mail(
            subject=self.data['email_subject'], message=self.data['email_body'], from_email=None, recipient_list=[self.data['to_email']], html_message=html_message)


class Util:
    @staticmethod
    def send_email(data):
        EmailThread(data).start()

    @staticmethod
    def excel_gen_LF(data):
        ExcelGenLF(data).start()

    @staticmethod
    def excel_gen_DQ(data):
        ExcelGenDQ(data).start()
