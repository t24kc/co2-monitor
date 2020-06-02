from oauth2client.service_account import ServiceAccountCredentials

import gspread

SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

DEFAULT_SHEET_INDEX = 0


class SpreadSheet(object):
    def __init__(self, key_path, spread_sheet_id):
        self._key_path = key_path
        self._spread_sheet_id = spread_sheet_id

    def _get_client(self):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self._key_path, SCOPES
        )
        return gspread.authorize(credentials).open_by_key(self._spread_sheet_id)

    def get_label_value(self, label, index=DEFAULT_SHEET_INDEX):
        return self._get_client().get_worksheet(index).acell(label).value

    def set_label_value(self, label, value, index=DEFAULT_SHEET_INDEX):
        self._get_client().get_worksheet(index).update_acell(label, value)

    def col_values(self, col, index=DEFAULT_SHEET_INDEX):
        try:
            return self._get_client().get_worksheet(index).col_values(col)
        except Exception as e:
            print(e)
            pass

    def get_all_values(self, index=DEFAULT_SHEET_INDEX):
        try:
            return self._get_client().get_worksheet(index).get_all_values()
        except Exception as e:
            print(e)
            pass

    def append_row(self, values, index=DEFAULT_SHEET_INDEX):
        try:
            self._get_client().get_worksheet(index).append_row(values)
        except Exception as e:
            print(e)
            pass
