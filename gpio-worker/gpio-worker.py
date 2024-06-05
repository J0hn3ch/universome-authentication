import os
import threading
import time
import serial     
import datetime
import logging
import requests
import asyncio
from aiocoap import *

logging.basicConfig(level=logging.INFO)

'''
reading_event = threading.Thread.Event()
def reading(serial):
    while reading_event.is_set():
            raw_reading = serial.readline()
            print(raw_reading)

reading_thread = threading.Thread(target=reading, daemon=True)
'''
def serial_worker():
    # ser = serial.Serial(port='/dev/ttyS4', baudrate = 9600, rtscts=True, dsrdtr=True,
    #     parity=serial.PARITY_NONE,
    #     stopbits=serial.STOPBITS_ONE,
    #     bytesize=serial.EIGHTBITS,
    #     timeout=1
    # )
    #counter=0
    with serial.Serial(port='/dev/ttyACM0', baudrate = 9600, rtscts=True, dsrdtr=True, timeout=1) as ser:
        while True:
            print("\nSerial Device Info\n=================")
            #print("Serial Name: ", ser.name)
            print("Serial Port: ", ser.port)


            card = ser.readlines()
            if not card: # no lines read
                pass
            else:
                print("Smart card model: ", card[0])
                print("Card ID: ", card[1], type(card[1]))
                print("Card ID (UTF-8): ", card[1].decode(encoding='utf-8'))
                return card[1].decode(encoding='utf-8')
            
            time.sleep(1)

# ====== [ CoAP Client ] ======
def alert_unauthorized_access():
    # 1. Create CoAP Client
    # 2. Prepare the request
    # 3. Send a PUT request to observable resource for notice unauthorized access
    pass
    

async def main():
    protocol = await Context.create_client_context()
    request = Message(code=GET, uri='coap://localhost/time')
    try:
        response = await protocol.request(request).response
    except Exception as e:
        print("Failed to fetch resource")
        print(e)
    else:
        print("Result: %s\n%r" % (response.code, response.payload))

if __name__ == "__main__":

    # ====== [ HTTP Request ] ======
    url_request = "http://127.0.0.0:8000/api/member/"
    parameters = {'key1', 'par1'}
    
    # 1. Listen for incoming Smart Card signal
    while True:

        # ====== [ Time ] ======
        now=datetime.datetime.now()
        y=now.strftime("%H:%M:%S") # https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes 
        print("\n====== Time: %s" % y)
        #asyncio.run(main())

        card_id = serial_worker()
        response = requests.get(url=url_request + card_id)
        member = response.json()[0]
    

        # 2. If the Serial line is inactive, do anything
        if response.status_code == 500:
            print("[Response Status Code 500]: Error in response")
        # 3. Else if the Serial il ready to transmit data (maybe some Smart Card info)..
        elif response.status_code == 200: # serial.available()
            # 3.1 Get this data
            # 3.2 Check this date if it corresponds to the type of Smart Card used by the company
            # 3.3 Send the Smart Card id to the server to get info about the member
            print("\nMember Info\n=================")
            print("Member ID: %s, Full Name: %s, Card ID: %s" % (member['id'], member['full_name'], member['card_id']))
            print("Is authorized?  %s" % member['authorized'])

            # 3.4 Print AUTHORIZED if the member is authorized for the entrance
            if member['authorized']:
                print("Member %s is authorized to entrance" % member['full_name'])
                # 3.4.1 Send positive signal to Arduino if the member is authorized
            else: # 3.5 Print DENIED if the member is not authorized for the entrance
                print('Entrance DENIED! Member not authorized')
                # 3.5.1 Send negative signal to Arduino if the member is not authorized
        
        time.sleep(1)