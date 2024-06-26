import asyncio
import aiocoap

class CoapController:
    storage = []  # class level field

    def __init__(self, name):
        self.name = name  # instance level field

    async def do_work(self):
        """just add some digits to class level field"""
        print("Hello")
