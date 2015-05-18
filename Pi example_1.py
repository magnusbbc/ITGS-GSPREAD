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
"""
json_key = json.load(open('ITGS-test-01071b9eba81.json'))
scope = ['https://spreadsheets.google.com/feeds']
credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
gc = gspread.authorize(credentials)
"""
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
looper = 1

#setup var for RFID
continue_reading = True

#Setup for output
GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT) #GREEN LED
GPIO.setup(13, GPIO.OUT) #RED LED
GPIO.setup(15, GPIO.OUT) #Buzzer

#setup for input
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Button 1/left
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Button 2/right
button1_state = True
button1_state = True
button = None #if "in" button2 has been selected, if "out" button one has been selected

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    global looper
    print "Ctrl+C captured, ending read."
    continue_reading = False
    looper = 0

#main function for reader and log system
def main_system(button):
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
                            f.close()
                        values_list.insert(1, button)
                        values_list.insert(2, time.strftime("%d/%m/%Y"))
                        values_list.insert(3, time.strftime("%I:%M:%S"))

                       # wks2.append_row(values_list)
                        d = csv.writer(open("buffer_writer.csv", "a"))
                        d.writerow([values_list[0],values_list[1],values_list[2],values_list[3],values_list[4],values_list[5]])
                        loop = 0
                        time.sleep(0.2)
                        GPIO.output(11, False)
                        GPIO.output(15, False)
                        button = None
                        return
                    elif check_value == row_count-1:
                        print "Card ID does not exists"
                        GPIO.output(13, True)
                        time.sleep(1)
                        GPIO.output(13, False)
                        loop = 0
                        button = None
                        return
                    check_value += 1
# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()
#wks2 = gc.open("data_2").sheet1
# This loop keeps checking for chips. If one is near it will get the UID and authenticate
print ("Welcome to GEMS AMERICAN ACADEMY RFID Staff sign in/out system!\n")
while True:
    input_var = input("0.Initiate Reading\n1.Add User\n2.Delete User\n3.End Program\n4.Documentation\n5.About\nEnter Value:")
    if input_var == 0:
        while looper == 1:
            if GPIO.input(7) == False:
                sign_IO = "out"
                continue_reading = True
                main_system(sign_IO)
            elif GPIO.input(12) == False:
                sign_IO = "in"
                continue_reading = True
                main_system(sign_IO)
    elif input_var == 1:
        #TODO READ CARD ID
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
        print ("TODO")
    elif input_var == 5:
        print ("RFAA\nMade by Magnus Bogh Borregaard Christensen\nVersion: 0.7")
    else:
        print ("Incorrect Value, must be between 0 and 3!")
GPIO.cleanup()
