__author__ = 'magnus'

import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

json_key = json.load(open('ITGS-test-01071b9eba81.json'))
scope = ['https://spreadsheets.google.com/feeds']
credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
gc = gspread.authorize(credentials)

wks = gc.open("data_1").sheet1
wks.update_acell('B8', "please make it works")