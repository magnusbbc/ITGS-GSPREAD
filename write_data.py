__author__ = 'magnus'

import json
import gspread
import time
import csv
from oauth2client.client import SignedJwtAssertionCredentials

json_key = json.load(open('ITGS-test-01071b9eba81.json'))
scope = ['https://spreadsheets.google.com/feeds']
credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
gc = gspread.authorize(credentials)

wks2 = gc.open("data_2").sheet1




CARD_ID = "F9122"
UID = "0000"
Sign_io = "True"
Date = "error"
Time = "error"
FName = "error"
LName = "error"
check_value = 1

with open('data_1.csv', 'rb') as f:
        reader = csv.reader(f)
        row_count = sum(1 for row in reader)

while True:
    with open('data_1.csv', 'rb') as f:
        reader = csv.reader(f)
        reader = list(reader)
        check = reader[check_value][0]
    print check
    if check == CARD_ID:
        with open('data_1.csv', 'rb') as f:
            reader = csv.reader(f)
            for i in range(check_value+1):
                values_list = reader.next()
        values_list.pop(0)
        values_list.insert(1, Sign_io)
        values_list.insert(2, time.strftime("%d/%m/%Y"))
        values_list.insert(3, time.strftime("%I:%M:%S"))
        wks2.append_row(values_list)
        break
    elif check_value == row_count-1:
        print "Card ID does not exists"
        break
    check_value += 1




wks2.resize(1)

