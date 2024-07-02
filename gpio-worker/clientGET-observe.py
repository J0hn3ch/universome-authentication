#!/usr/bin/env python3

# SPDX-FileCopyrightText: Christian Amsüss and the aiocoap contributors
#
# SPDX-License-Identifier: MIT

"""This is a usage example of aiocoap that demonstrates how to implement a
simple client. See the "Usage Examples" section in the aiocoap documentation
for some more information."""

import logging
import asyncio
from aiocoap import *

logging.basicConfig(level=logging.INFO)


async def entranceObserverClient():
    protocol = await Context.create_client_context()

    request = Message(code=GET, uri="coap://localhost:5683/time", observe=0)

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
    await asyncio.sleep(50)


if __name__ == "__main__":
    asyncio.run(entranceObserverClient())
