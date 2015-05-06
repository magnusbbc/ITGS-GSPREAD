__author__ = 'magnus'

import json
import gspread
import time
from oauth2client.client import SignedJwtAssertionCredentials

json_key = json.load(open('ITGS-test-01071b9eba81.json'))
scope = ['https://spreadsheets.google.com/feeds']
credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
gc = gspread.authorize(credentials)

wks1 = gc.open("data_1").sheet1
wks2 = gc.open("data_2").sheet1

row = 2
CARD_ID = "F9122"
UID = "0000"
Sign_io = "True"
Date = "error"
Time = "error"
FName = "error"
LName = "error"
check_value = 1

while True:

    check = wks1.cell(check_value, 1).value
    print check
    if check == CARD_ID:
        values_list = wks1.row_values (check_value)
        values_list.pop(0)
        values_list.insert(1, Sign_io)
        values_list.insert(2, time.strftime("%d/%m/%Y"))
        values_list.insert(3, time.strftime("%I:%M:%S"))
        wks2.append_row(values_list)
        break
    elif not check:
        print "Card ID does not exists"
        break
    check_value += 1




#wks2.resize(1)

