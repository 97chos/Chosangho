import gspread
from oauth2client.service_account import ServiceAccountCredentials

SCOPE = [
'https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive',
]

JSON_FILE_NAME = 'webautomation-274506-aef19b1b646f.json'

CREDENTIAL = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILE_NAME, SCOPE)
GC = gspread.authorize(CREDENTIAL)

TESTCASE_CARD_URL = "https://docs.google.com/spreadsheets/d/1lMDVL9ip_nZqtcKKQzVwuMRNMxj6upAvYrZ_6fh8X5Y"