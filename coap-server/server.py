#!/usr/bin/env python3

import datetime
import logging
import requests
import sqlite3
import asyncio

import aiocoap
import aiocoap.resource as resource
from aiocoap import Message
from aiocoap.numbers.contentformat import ContentFormat # - https://github.com/chrysn/aiocoap/blob/master/aiocoap/numbers/contentformat.py 

# Member Model
from MemberModel import Member

global db
global logger

# logging setup
logging.basicConfig(
    format="[%(levelname)s] %(asctime)s - %(name)s: %(message)s",
    level=logging.DEBUG) # level values: ( logging.INFO | )
logging.getLogger("asyncio").setLevel(logging.WARNING)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

class MemberEndpoint(resource.Resource):
    def __init__(self):
        super().__init__()
        self.webapp_host = "172.26.0.2"
        self.webapp_port = "8000"

    # /member Resource Description in .well-known/core
    def get_link_description(self):
        return dict(**super().get_link_description(),ct="0", obs="0", title="Member Resource") # Publish additional data in .well-known/core


    async def render_get(self, request):
        logging.getLogger("coap-server").debug("GET payload: %s" % repr(request.payload))
        url = "http://" + self.webapp_host + ":" + self.webapp_port + "/api/member"
        parameters = {'card_id' : request.payload.decode(encoding='UTF-8')}
        response = requests.get(url=url, params=parameters)
        if response.status_code == 200:
            payload = response.json()[0]
        else:
            payload = "STATUS CODE DIFFERENT FROM 200".encode('UTF-8')
        
        return aiocoap.Message(code=aiocoap.CONTENT, payload=str(payload).encode(encoding='UTF-8'))

    async def render_post(self, request):
        logging.getLogger("coap-server").debug("POST payload: %s" % repr(request.payload))
        coap_payload = request.payload
        path = "/api/coap/observe"
        url = "http://" + self.webapp_host + ":" + self.webapp_port + path

        headers = {
            "Memfault-Project-Key": "PROVA",
            "Content-Type": "application/octet-stream",
        }

        response = requests.post(url, data=coap_payload, headers=headers)
        logging.getLogger("coap-server").debug("HTTPs response: %s" % response.status_code)
        logging.getLogger("coap-server").debug("HTTPs response content: %s" % response.content)

        return aiocoap.Message(code=aiocoap.CONTENT, payload=response.content)


class WelcomeMember(resource.Resource):
    representations = {
            ContentFormat.TEXT: b"Sample Member",
            ContentFormat.LINKFORMAT: b"</member>",
            # ad-hoc for application/xhtml+xml;charset=utf-8
            ContentFormat(65000):
                b'<html xmlns="http://www.w3.org/1999/xhtml">'
                b'<head><title>aiocoap demo</title></head>'
                b'<body><h1>Welcome to the aiocoap demo server!</h1>'
                b'<ul><li><a href="time">Current time</a></li>'
                b'<li><a href="whoami">Report my network address</a></li>'
                b'</ul></body></html>',
            }
    
    default_representation = ContentFormat.TEXT

    def __init__(self):
        super().__init__()
        self.set_content(b"Init Member\n")
    
    def get_link_description(self):
        # Publish additional data in .well-known/core
        return dict(**super().get_link_description(), title="Log member entrance")

    def set_content(self, content):
        self.content = content
    
    def check_authorization(self, card_id):
        ''' SQLite Query'''
        member = Member.get_member(card_id=card_id)
        return member['authorized']

    
    async def render_get(self, request):
        print(type(request))
        #self.check_authorization(member_id=1)

        cf = self.default_representation if request.opt.accept is None else request.opt.accept
        
        try:
            return aiocoap.Message(payload=self.representations[cf], content_format=cf)
        except KeyError:
            raise aiocoap.error.UnsupportedContentFormat
        
    async def render_post(self, request):
        payload = request.payload.decode('utf-8')
        card_id = payload.strip()

        member = Member.get_member(card_id=card_id)
        if member:
            member = member.pop().to_json()
            if member['authorized']:
                access_granted = "Access Granted"
            else:
                access_granted = "Access Denied"
        else:
            raise Exception('Member not found')
        
        response = aiocoap.Message(payload=access_granted.encode('utf-8'))
        return response
        
    async def render_put(self, request):
        print('PUT payload: %s' % request.payload)
        self.set_content(request.payload)
        return aiocoap.Message(code=aiocoap.CHANGED, payload=self.content)

class BlockResource(resource.Resource):
    """Example resource which supports the GET and PUT methods. It sends large
    responses, which trigger blockwise transfer."""

    def __init__(self):
        super().__init__()
        self.set_content(b"This is the resource's default content. It is padded "
                b"with numbers to be large enough to trigger blockwise "
                b"transfer.\n")

    def set_content(self, content):
        self.content = content
        while len(self.content) <= 1024:
            self.content = self.content + b"0123456789\n"

    async def render_get(self, request):
        return aiocoap.Message(payload=self.content)

    async def render_put(self, request):
        print('PUT payload: %s' % request.payload)
        self.set_content(request.payload)
        return aiocoap.Message(code=aiocoap.CHANGED, payload=self.content)

    
class UnauthorizedAccess(resource.ObservableResource):
    representations = {
        ContentFormat.TEXT: b"2024-01-01 00:00:00,AABBCCDD,False",
        ContentFormat.JSON: b"{'entrance_date':'2024-01-01 00:00:00','full_name':'Sample Member','card_id':'AABBCCDD','authorized':'False'}"
    }

    contents = {
        ContentFormat.JSON: None
    }

    default_representation = ContentFormat.TEXT
    
    def __init__(self):
        super().__init__()
        self.set_content("2024-01-01 00:00:00,Sample Member,AABBCCDD,False".encode('utf-8'))
        self.observers = []
        self.handle = None

    def set_content(self, content):
        ''' content must be a 'bytes' type'''
        self.content = content
        # Set JSON
        r = eval( self.representations[ContentFormat.JSON].decode(encoding='utf-8') )
        c = content.decode(encoding='utf-8').split(',')
        self.contents[ContentFormat.JSON] = str( dict( zip(r.keys(),c) ) ).encode('utf-8')
        # Set TEXT
        self.contents[ContentFormat.TEXT] = self.content
        

    def notify(self):
        self.updated_state()
        #self.reschedule()

    def reschedule(self):
        self.handle = asyncio.get_event_loop().call_later(5, self.notify)

    def update_observation_count(self, count):
        if count and self.handle is None:
            print("Starting the clock")
            self.reschedule()
        if count == 0 and self.handle:
            print("Stopping the clock")
            self.handle.cancel()
            self.handle = None

    async def render_get(self, request):
        cf = self.default_representation if request.opt.accept is None else request.opt.accept
        #payload = self.content
        #return aiocoap.Message(code=aiocoap.CONTENT, payload=payload)
        try:
            return aiocoap.Message(code=aiocoap.CONTENT, payload=self.contents[cf], content_format=cf)
        except KeyError:
            raise aiocoap.error.UnsupportedContentFormat
    
    async def render_post(self, request):
        return aiocoap.Message(code=aiocoap.CHANGED)
    
    async def render_put(self, request):
        self.set_content(request.payload)
        self.notify()
        return aiocoap.Message(code=aiocoap.CHANGED, payload=self.content)
    
    async def render_delete(self, request):
        if not self.observers:
            return Message(code=aiocoap.DELETED)
        else:
            return Message(code=aiocoap.FORBIDDEN, payload=b"Cannot delete while observers are active")
    
    # !!! Check this function
    # def add_observation(self, request, server):
    #     self.observers.append((request, server))
    #     server.add_observation(request, self)

    # def notify_observers(self):
    #     for request, server in self.observers:
    #         response = Message(code=aiocoap.CONTENT, payload=self.content)
    #         server.send_response(request, response)

class TimeResource(resource.ObservableResource):
    """Example resource that can be observed. The `notify` method keeps
    scheduling itself, and calles `update_state` to trigger sending
    notifications."""

    def __init__(self):
        super().__init__()

        self.handle = None

    def notify(self):
        self.updated_state()
        self.reschedule()

    def reschedule(self):
        self.handle = asyncio.get_event_loop().call_later(5, self.notify)

    def update_observation_count(self, count):
        if count and self.handle is None:
            print("Starting the clock")
            self.reschedule()
        if count == 0 and self.handle:
            print("Stopping the clock")
            self.handle.cancel()
            self.handle = None

    async def render_get(self, request):
        payload = datetime.datetime.now().\
                strftime("%Y-%m-%d %H:%M").encode('ascii')
        return aiocoap.Message(payload=payload)

class WhoAmI(resource.Resource):
    async def render_get(self, request):
        text = ["Used protocol: %s." % request.remote.scheme]

        text.append("Request came from %s." % request.remote.hostinfo)
        text.append("The server address used %s." % request.remote.hostinfo_local)

        claims = list(request.remote.authenticated_claims)
        if claims:
            text.append("Authenticated claims of the client: %s." % ", ".join(repr(c) for c in claims))
        else:
            text.append("No claims authenticated.")

        return aiocoap.Message(content_format=0,
                payload="\n".join(text).encode('utf8'))

async def main():
    # Resource tree creation
    root = resource.Site()

    root.add_resource(
        ['.well-known', 'core'], resource.WKCResource(root.get_resources_as_linkheader)
    )
    #root.add_resource([], Welcome())
    root.add_resource(['time'], TimeResource())
    root.add_resource(['other', 'block'], BlockResource())
    root.add_resource(['whoami'], WhoAmI())

    
    root.add_resource(['other','member'], WelcomeMember())
    root.add_resource(['unauthorized'], UnauthorizedAccess())
    root.add_resource(['member'], MemberEndpoint())

    await aiocoap.Context.create_server_context(root, bind=('0.0.0.0', 5683)) # https://aiocoap.readthedocs.io/en/latest/module/aiocoap.html#aiocoap.Context.create_server_context
    
    logging.getLogger('coap-server').debug("CoAP server listening to port 5683")
    await asyncio.get_running_loop().create_future() # Run forever

if __name__ == "__main__":    
    db = sqlite3.connect(
        './universome.sqlite',
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    db.row_factory = sqlite3.Row
    
    asyncio.run(main(), debug=True)
