__author__ = 'magnus'

import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

json_key = json.load(open('ITGS-test-01071b9eba81.json'))
scope = ['https://spreadsheets.google.com/feeds']
credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
gc = gspread.authorize(credentials)

wks = gc.open("data_2").sheet1

row = 2
UID = 0000
Sign_io = "True"
Date = "12/12/15"
Time = "23:22"
FName = "Magnus"
LName = "Christensen"

wks.update_cell(row, 1, UID)
wks.update_cell(row, 2, Sign_io)
wks.update_cell(row, 3, Date)
wks.update_cell(row, 4, Time)
wks.update_cell(row, 5, FName)
wks.update_cell(row, 6, LName)