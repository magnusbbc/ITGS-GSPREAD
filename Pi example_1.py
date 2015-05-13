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
UID = "0000"
loop = 0
Sign_io = "True"
Date = "error"
Time = "error"
FName = "error"
LName = "error"
check_value = 1
input_var = 0
input_list = {}
with open('data_1.csv', 'rb') as f:
        reader = csv.reader(f)
        row_count = sum(1 for row in reader)

#setup var for RFID
continue_reading = True

#Setup for output
GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT) #GREEN LED
GPIO.setup(13, GPIO.OUT) #RED LED
GPIO.setup(15, GPIO.OUT) #Buzzer

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()
print "Ctrl+C to stop capture"
wks2 = gc.open("data_2").sheet1
# This loop keeps checking for chips. If one is near it will get the UID and authenticate
print ("Welcome to GEMS AMERICAN ACADEMY RFID Staff sign in/out system!\n")
while True:
    input_var = input("0.Initiate Reading\n1.Add User\n2.Delete User\n3.End Program\n4.Documentation\n5.About\nEnter Value:")
    if input_var == 0:
        print "Ctrl+C to stop capture"
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

                # save UID

                UID_check = str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
                loop = 1
                check_value = 1
                #Authenticate and log
                while loop ==1:
                    with open('data_1.csv', 'rb') as f:
                        reader = csv.reader(f)
                        reader = list(reader)
                        check = reader[check_value][0]
                    print check
                    if check == UID_check:
                        GPIO.output(11, True)
                        GPIO.output(15, True)
                        with open('data_1.csv', 'rb') as f:
                            reader = csv.reader(f)
                            for i in range(check_value+1):
                                values_list = reader.next()
                        values_list.pop(0)
                        values_list.insert(1, Sign_io)
                        values_list.insert(2, time.strftime("%d/%m/%Y"))
                        values_list.insert(3, time.strftime("%I:%M:%S"))
                        wks2.append_row(values_list)
                        time.sleep(1)
                        GPIO.output(11, False)
                        GPIO.output(15, False)
                        loop = 0
                    elif check_value == row_count-1:
                        print "Card ID does not exists"
                        GPIO.output(13, True)
                        time.sleep(1)
                        GPIO.output(13, False)
                        loop = 0
                    check_value += 1
    elif input_var == 1:
        #TODO: READ CARD ID
        input_list[0] = raw_input("Enter Card number:")
        input_list[1] = 1000+(row_count - 1)
        input_list[2] = raw_input("Enter First Name:")
        input_list[3] = raw_input("Enter Last Name:")
        c = csv.writer(open("data_1.csv", "a"), lineterminator='\n')
        c.writerow([input_list[0],input_list[1],input_list[2],input_list[3]])

    elif input_var == 2:
        #TODO
        print ("todo")
    elif input_var == 3:
        break
    elif input_var == 4:
        #TODO
        print("TODO")
    elif input_var == 5:
        print ("RFAA\nMade by Magnus Bogh Borregaard Christensen\nVersion: 0.7")

    else:
        print ("Incorrect Value, must be between 0 and 3!")
GPIO.cleanup()