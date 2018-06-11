# -*- coding: utf-8 -*-
"""

"""

import json

import zmq

port = 62260
port1 = 62261

## for client register
connected = set()

import websockets

async def ws_handler(websocket, path):
    
    """
    websockets handler
    
    """
    
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.connect("tcp://localhost:%s" % port)    
    
    context2 = zmq.Context()
    socket2 = context2.socket(zmq.PULL)
    socket2.bind("tcp://*:%s" % port1)
    #socket2.send("World from %s" % port)

    #message = socket2.recv()
    
    
    connected.add(websocket)
    
    try:
        
        while True:
            
            #data = reading_queue.get()
            data = socket2.recv_json()
            #data = msgpack.unpackb(data, raw=False)
            print(data)
            #socket2.send_string("ack")
            
            #print(connected)
            #print(">>>")
            
            try:
                
                await websocket.send(json.dumps(data))  
                ack = await websocket.recv()
                print("ack:%s"%(ack))
                #writing_queue.put(ack)
                #ack = msgpack.packb(ack)
                socket.send_json(ack)
                
                #socket.recv_json()
                #socket2.send(ack)
               
            except Exception as ex:
                ## unregister here
                print(connected)
                connected.remove(websocket)
                print(ex)

    finally:
            # Unregister.
            print("remove")
            connected.remove(websocket)
    
    print('hhh')
    
    
start_server = websockets.serve(ws_handler, '127.0.0.1', 5678)