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

global handshake

'''
reading_event = threading.Thread.Event()
def reading(serial):
    while reading_event.is_set():
            raw_reading = serial.readline()
            print(raw_reading)

reading_thread = threading.Thread(target=reading, daemon=True)
'''
def serial_worker(debug=True):
    handshake = "" # variable used to establish to start reading output from Arduino
    
    # === SERIAL CONNECTION
    with serial.Serial(port='/dev/ttyACM0', 
                       baudrate=115200, rtscts=True, dsrdtr=True, 
                       parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, 
                       timeout=1.0,) as ser:
        
        print("\nSerial Device Info\n==================")
        #print("Serial Name: ", ser.name)
        print("Serial Port: ", ser.port)
        print("Serial Baudrate: ", ser.baudrate)
        
        time.sleep(1)
        #ser.reset_input_buffer()
        #ser.flush()
        print("[DEBUG] - Waiting for handshake.. ") if debug else None
        while True:
            #try:
            time.sleep(0.01)
            # ====== [ Serial Connection Handshake ] ======
            while not handshake: # Skip initialization printing
                time.sleep(0.01)
                if ser.in_waiting > 0:
                    message = ser.readline().decode(encoding='utf-8').rstrip()
                    if message == "H4NDSH4K3":
                        handshake = message
                        print("Serial connection established: ", handshake)
                else:
                    ser.write("Hello\n".encode('utf-8'))

            if ser.in_waiting > 0:
                raw_data = ser.readline()
                print("[DEBUG] - Raw data ", raw_data) if debug else None
                decoded_values = raw_data.decode(encoding='utf-8')
                data = [e.strip() for e in decoded_values.split(',')]
                print("[DEBUG] - Data: ", data, len(data)) if debug else None
                print("[DEBUG] - Smart card model: ", data[0]) if debug else None
                print("[DEBUG] - Card ID: ", data[1], type(data[1])) if debug else None
                
                return data[1]
                #ser.write( "somestring\n".encode('utf-8') )
                #while ser.in_waiting <= 0:
                #   time.sleep(0.01)
            else:
                pass

            time.sleep(1)
            #except KeyboardInterrupt:
            #    print("Close serial communication")
            
# ====== [ CoAP Client ] ======
async def alert_unauthorized_access(log):
    # 1. Create CoAP Client
    protocol = await Context.create_client_context()
    payload = log.encode('utf-8')
    # 2. Prepare the request
    request = Message(code=PUT, payload=payload, uri='coap://localhost/unauthorized')
    
    # 3. Send a PUT request to observable resource for notice unauthorized access
    try:
        response = await protocol.request(request).response
    except Exception as e:
        print("Failed to fetch resource")
        print(e)
    else:
        print("[CoAP Server response] - UNAUTHORIZED ACCESS AT: %s %r" % (response.code, response.payload.decode(encoding='utf-8')))

if __name__ == "__main__":

    # ====== [ HTTP Request ] ======
    url_request = "http://127.0.0.0:8000/api/member/"
    
    # 1. Listen for incoming Smart Card signal
    while True:
        # ====== [ Time ] ======
        now=datetime.datetime.now()
        y=now.strftime("%H:%M:%S") # https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes 
        print("\n====== Time: %s" % y)
        

        card_id = serial_worker()
        parameters = {'card_id' : card_id}
        response = requests.get(url=url_request, params=parameters)

        # 2. If the Serial line is inactive, do anything
        if response.status_code == 500:
            print("[Response Status Code 500]: Error in response")
        # 3. Else if the Serial il ready to transmit data (maybe some Smart Card info)..
        elif response.status_code == 404:
            print("[DEBUG] - " + str(response.json()))
        elif response.status_code == 200: # serial.available()
            # 3.1 Get this data
            member = response.json()[0]
            # 3.2 Check this date if it corresponds to the type of Smart Card used by the company
            # 3.3 Send the Smart Card id to the server to get info about the member
            print("\nWeb App HTTP Request\n====================")
            print("[DEBUG] - Member ID: %s, Full Name: %s, Card ID: %s, Authorized: %s" % (member['id'], member['full_name'], member['card_id'], member['authorized']))

            # 3.4 Print AUTHORIZED if the member is authorized for the entrance
            if member['authorized']:
                print("[DEBUG] - Member %s is authorized to entrance" % member['full_name'])
                # 3.4.1 Send positive signal to Arduino if the member is authorized
            else: # 3.5 Print DENIED if the member is not authorized for the entrance
                print('[DEBUG] - Entrance DENIED! Member not authorized')
                # 3.5.1 Send negative signal to Arduino if the member is not authorized
                # 3.5.2 Alert the CoAP Server
                timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                message = timestamp +"," + member['card_id'] + "," + str(member['authorized'])
                asyncio.run(alert_unauthorized_access(log=message))
        
        time.sleep(1)