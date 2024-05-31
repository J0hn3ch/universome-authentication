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
    with serial.Serial(port='/dev/ttyS0', baudrate = 9600, rtscts=True, dsrdtr=True, timeout=1) as ser:
        pass

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
    
    #ser = serial.Serial(port='/dev/ttyS1', baudrate = 9600, rtscts=True, dsrdtr=True
        # parity=serial.PARITY_NONE,
        # stopbits=serial.STOPBITS_ONE,
        # bytesize=serial.EIGHTBITS,
        # timeout=1
    #)
    #counter=0
    url_request = "http://127.0.0.0:8000/api/member/1"
    par1 = "2"
    parameters = {'key1', par1}
    response = requests.get(url=url_request)
    member = response.json()[0]
    
    # 1. Listen for incoming Smart Card signal
    while True:
        time.sleep(1)
        now=datetime.datetime.now()
        y=now.strftime("%H:%M:%S") # https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes 
        print("\n====== Time: %s" % y)
        #x=ser.readline()
        #print(x,y)
        #asyncio.run(main())

        # 2. If the Serial line is inactive, do anything
        if response.status_code == 500:
            print("[Response Status Code 500]: Error in response")
        # 3. Else if the Serial il ready to transmit data (maybe some Smart Card info)..
        elif response.status_code == 200: # serial.available()
            # 3.1 Get this data
            # 3.2 Check this date if it corresponds to the type of Smart Card used by the company
            # 3.3 Send the Smart Card id to the server to get info about the member
            print("Member ID: %s, Full Name: %s, Card ID: %s" % (member['id'], member['full_name'], "AA:BB:CC"))
            print("Is authorized?  %s" % member['authorized'])

            # 3.4 Print AUTHORIZED if the member is authorized for the entrance
            if member['authorized']:
                print("Member %s is authorized to entrance" % member['full_name'])
                # 3.4.1 Send positive signal to Arduino if the member is authorized
            else: # 3.5 Print DENIED if the member is not authorized for the entrance
                print('Entrance DENIED! Member not authorized')
                # 3.5.1 Send negative signal to Arduino if the member is not authorized