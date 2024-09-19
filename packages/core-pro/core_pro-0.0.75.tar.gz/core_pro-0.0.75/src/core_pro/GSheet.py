import polars as pl
import pandas as pd
from colorama import Fore
from openpyxl.utils.cell import column_index_from_string, coordinate_from_string
from core_pro.config import GoogleAuthentication
from loguru import logger
import sys

logger.remove()
fmt = '<green>{time:HH:mm:ss}</green> | <level>{message}</level>'
logger.add(sys.stdout, colorize=True, format=fmt)


class Sheet(GoogleAuthentication):
    service_type = 'sheets'

    def __init__(self, gsheet_key):
        super().__init__(Sheet.service_type)
        self.gsheet_key = gsheet_key
        self.status = f'{Fore.LIGHTGREEN_EX}🐶 Sheet:{Fore.RESET}'

    def google_sheet_into_df(
            self,
            sheet_name: str,
            sheet_range: str,
            value_render_option: str = 'FORMATTED_VALUE',
            use_polars: bool = True,
    ) -> pl.DataFrame | pd.DataFrame:
        """
        Read google sheet and return a DataFrame
        :param use_polars: True, False
        :param value_render_option: default FORMATTED_VALUE, UNFORMATTED_VALUE, FORMULA
        :param sheet_name: google sheet name
        :param sheet_range: google sheet range
        :return: a DataFrame
        """
        range_update = f'{sheet_name}!{sheet_range}'
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.gsheet_key,
            range=range_update,
            valueRenderOption=value_render_option,
        ).execute()

        logger.info(f"{self.status} Loaded at {range_update}")
        if use_polars:
            max_length = max(len(v) for v in result['values'])
            padded_data = [v + [None] * (max_length - len(v)) for v in result['values'][1:]]
            return pl.DataFrame(padded_data, schema=result['values'][0], orient='row')
        else:
            return pd.DataFrame(result['values'][1:], columns=result['values'][0])

    def create_new_gsheet(self, title: str) -> str:
        """
        Create new google sheet
        :param title: title for new google sheet
        :return: None
        """

        spreadsheet = {
            'properties': {
                'title': title
            }
        }
        spreadsheet = self.service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()
        print(f"Spreadsheet ID: {spreadsheet.get('spreadsheetId')}")
        spreadsheet_id = spreadsheet.get('spreadsheetId')
        return spreadsheet_id

    def clear_gsheet(self, sheet_name: str, sheet_range: str):
        """
        Clear google sheet
        :param sheet_name: sheet name
        :param sheet_range: ex: "A:C"
        :return: None
        """

        name = f'{sheet_name}!{sheet_range}'
        self.service.spreadsheets().values().clear(spreadsheetId=self.gsheet_key, range=name, body={}).execute()

    def update_value_single_axis(
            self,
            value_input: str | list,
            sheet_name: str,
            sheet_range: str,
            COLUMNS_or_ROWS: str = 'ROWS',
            value_option: str = 'RAW'
    ):
        """
        Update google sheet value
        :param sheet_range: range update ex: 'A1'
        :param value_input: value need to update: [2, 3, 4] or [[2, 3, 4], [2, 3, 4]] if multi==True
        :param sheet_name: sheet name
        :param COLUMNS_or_ROWS: default by ROWS
        :param value_option: default = 'RAW', or 'USER_ENTERED' or INPUT_VALUE_OPTION_UNSPECIFIED
        :return: result
        """

        range_update = f"{sheet_name}!{sheet_range}"
        if isinstance(value_input, list):
            values = value_input
        else:
            values = [[value_input]]
        body = {
            'values': values,
            'majorDimension': COLUMNS_or_ROWS
        }
        self.service.spreadsheets().values().update(
            spreadsheetId=self.gsheet_key,
            range=range_update,
            valueInputOption=value_option,
            body=body
        ).execute()
        logger.info(f"{self.status} Update values at: {range_update}")

    def make_a_copy_sheet(self, sheet_id: str, dup_sheet_name: str):
        """
        Para:
        - spreadsheet_id: template_sheet
        - sheet_id: template_worksheet
        - dup_sheet_name: sheet to copy
        """

        duplicated_spreadsheet_body = {'destination_spreadsheet_id': dup_sheet_name}
        request = self.service.spreadsheets().sheets().copyTo(spreadsheetId=self.gsheet_key,
                                                              sheetId=sheet_id,
                                                              body=duplicated_spreadsheet_body)
        response = request.execute()
        return response

    def rename_worksheet(self, sheet_id: str, new_title: str):
        requests = {
            "updateSheetProperties": {
                "properties": {
                    "sheetId": sheet_id,
                    "title": new_title,
                },
                "fields": "title",
            }
        }
        body = {
            'requests': requests
        }
        self.service.spreadsheets().batchUpdate(spreadsheetId=self.gsheet_key, body=body).execute()

    def delete_worksheet(self, sheet_id: str):
        requests = {
            "deleteSheet": {
                "sheetId": sheet_id
            }
        }
        body = {
            'requests': requests
        }
        self.service.spreadsheets().batchUpdate(spreadsheetId=self.gsheet_key, body=body).execute()

    def get_worksheet_properties(self, sheet_name: str):
        spreadsheet = self.service.spreadsheets().get(spreadsheetId=self.gsheet_key).execute()
        lst_worksheet = list(filter(lambda x: x.get('properties').get('title') == sheet_name, spreadsheet['sheets']))
        if lst_worksheet:
            return lst_worksheet[0].get('properties')

    def format_title(self, ws_id: str, start: str):
        color_orange = hex_to_rgb('#ff6d01', 'sheets')
        pos_row = column_index_from_string(coordinate_from_string(start)[0]) - 1
        pos_col = coordinate_from_string(start)[1]
        my_range = {
            'sheetId': ws_id,
            'startRowIndex': pos_row,
            'endRowIndex': pos_row + 1,
            'startColumnIndex': pos_col - 1,
            'endColumnIndex': pos_col,
        }
        request = [
            {
                'repeatCell': {
                    'range': my_range,
                    'cell': {
                        'userEnteredFormat': {
                            'textFormat': {'foregroundColor': color_orange,
                                           'bold': True,
                                           'fontSize': 12,
                                           'fontFamily': 'Roboto'}
                        }
                    },
                    'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                }
            },
        ]
        body = {"requests": request}
        self.service.spreadsheets().batchUpdate(spreadsheetId=self.gsheet_key, body=body).execute()
        print(f'{self.status} Format title at {start}')

    def format_header(self, ws_id: str, start: str, num_col: int):
        color_grey = hex_to_rgb('#b7b7b7', 'sheets')
        pos_row = coordinate_from_string(start)[1] - 1
        pos_col = column_index_from_string(coordinate_from_string(start)[0]) - 1

        my_range = {
            'sheetId': ws_id,
            'startRowIndex': pos_row,
            'endRowIndex': pos_row + 1,
            'startColumnIndex': pos_col,
            'endColumnIndex': pos_col + num_col,
        }
        request = [
            {
                'repeatCell': {
                    'range': my_range,
                    'cell': {
                        'userEnteredFormat': {
                            'backgroundColor': color_grey,
                            'horizontalAlignment': 'CENTER',
                            'textFormat': {'bold': True,
                                           'fontFamily': 'Roboto'}
                        }
                    },
                    'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)'
                }
            },
        ]
        body = {"requests": request}
        self.service.spreadsheets().batchUpdate(spreadsheetId=self.gsheet_key, body=body).execute()
        print(f'{self.status} Format header at {start}')

    def frozen_view(self, ws_id: str, frozen_rows: int = 2):
        request = [
            {
                'updateSheetProperties': {
                    'properties': {
                        'sheetId': ws_id,
                        'gridProperties': {'frozenRowCount': frozen_rows}
                    },
                    'fields': 'gridProperties.frozenRowCount'
                }
            }
        ]
        body = {"requests": request}
        self.service.spreadsheets().batchUpdate(spreadsheetId=self.gsheet_key, body=body).execute()
        print(f'{self.status} Frozen views')


def hex_to_rgb(hex_code, mode='sheets'):
    hex_code = hex_code.lstrip('#')
    rgb = tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
    if mode == 'sheets':
        return {i: v / 255 for i, v in zip(['red', 'green', 'blue'], rgb)}
    else:
        return rgb
