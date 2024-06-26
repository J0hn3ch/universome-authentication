from flask import Blueprint, make_response, request, jsonify
import asyncio
from aiocoap import *
from aiocoap import numbers

coap_api = Blueprint('coap_api', __name__, url_prefix='/api/coap')

async def main_coap():
    print("Function main Coap")
    protocol = await Context.create_client_context()
    msg = Message(code=numbers.codes.GET, uri="coap://172.26.0.20:5683/member")
    response = await protocol.request(msg).response
    print(response.payload.decode("utf-8"))
    return response

@coap_api.route('/member')
async def coap_api_root():
    print("GET printed")
    response = await asyncio.ensure_future(main_coap())
    print("Response: ", response, type(response))
    return make_response("OK", 202)
