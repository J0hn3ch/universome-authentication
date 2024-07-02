import asyncio
from aiocoap import *

async def entranceObserverClient():
    protocol = await Context.create_client_context()

    request = Message(code=GET, uri="coap://172.26.0.20:5683/unauthorized", observe=0)
    request.opt.accept = ContentFormat(ContentFormat.JSON)
    pr = protocol.request(request)

    r = await pr.response
    print("First response: %s\n%r" % (r, r.payload))

    i = 0
    async for r in pr.observation:
        print("Next result: %s\n%r" % (r, r.payload))
        i = i + 1
        if i == 10:
            pr.observation.cancel()
            break

    print("Loop ended, sticking around")
    await asyncio.sleep(5)

class CoapController:
    storage = []  # class level field

    def __init__(self, name):
        self.name = name  # instance level field

    async def do_work(self):
        """just add some digits to class level field"""
        print("Hello")
