#RFID Imports
import RPi.GPIO as GPIO
import MFRC522
import signal

#logging imports
import json
import gspread
import time
import csv
from oauth2client.client import SignedJwtAssertionCredentials

#setup variables for logging
json_key = json.load(open('ITGS-test-01071b9eba81.json'))
scope = ['https://spreadsheets.google.com/feeds']
credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
gc = gspread.authorize(credentials)
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

#setup var for RFID
continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

wks2 = gc.open("data_2").sheet1
# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:

    # Scan for cards
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card detected"

    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        print "Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])

        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]

        #Authenticate and log
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