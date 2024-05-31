import os
import time
import serial     
import datetime
import logging
import asyncio
from aiocoap import *

logging.basicConfig(level=logging.INFO)

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
    ser = serial.Serial(
        port='/dev/pts/2',
        baudrate = 9600,
        rtscts=True,
        dsrdtr=True
        # parity=serial.PARITY_NONE,
        # stopbits=serial.STOPBITS_ONE,
        # bytesize=serial.EIGHTBITS,
        # timeout=1
    )
    counter=0
    while 1:
        now=datetime.datetime.now()
        y=now.strftime("%S")
        x=ser.readline()
        print(x,y)
        asyncio.run(main())