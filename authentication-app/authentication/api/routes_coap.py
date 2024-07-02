from flask import Blueprint, make_response, request, jsonify
import asyncio
from aiocoap import *
from aiocoap import numbers
from authentication.controller.CoapController import entranceObserverClient

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

@coap_api.route('/observe', methods=['GET','POST','PUT'])
def entrance_observer():
    if request.method == 'GET': # Request from CoAP Server
        print('[CoAP Server > Web App]: Request Test')
        asyncio.run(entranceObserverClient())
        return make_response("Resource Observed done!\n", 200)
    
    elif request.method == 'POST': # Request from CoAP Server
        print('[CoAP Server > Web App]: ', request.data)
        return make_response(str(request.data), 200)
    
    elif request.method == 'PUT': # Request from CoAP Server
        print('[CoAP Server > Web App]: ', request.args.get('message'))
        return make_response("CoAP to HTTP done\n", 200)
