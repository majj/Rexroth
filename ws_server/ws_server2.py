
#get torque data and send it to browser by websockets

import time
import asyncio
import datetime
import random
import websockets

import ast

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler #LoggingEventHandler,

import threading

import queue

q1 = queue.Queue()

q2 = queue.Queue()

import json


class EventHandler(FileSystemEventHandler):
    """
    handler for file create event
    ['event_type', 'is_directory', 'key', 'src_path']
    """
    
    #def __init__(self):
    #    pass
     
    def on_created(self, event):
        """ test """
        #print(dir(event))
        if not event.is_directory:
            #print(event.key)
            #print(event.event_type)
            print(event.src_path)
            
            file_path = event.src_path
            
            with open(file_path, 'r') as fh:
                
                data = fh.read()
                
                d = ast.literal_eval(data)
                v = d['tightening steps'][2]['angle threshold']['act']
                print(v)
                q1.put({"angle act":v})
                
            
            
            q1.put({"path":file_path})
        
        print("=="*20)        
        
        
    def on_moved(self, event):
        pass
        
    def on_modified(self, event):
        
        pass
        
def timer():
    
    """
    thread, timer for browser
    """
    
    while True:
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        
        q1.put({"now":now})
        
        time.sleep(3)
        
def watcher():
    
    """
    thread, read torque data
    """
    
    path = '../data'
    
    event_handler = EventHandler()
    
    observer = Observer()

    observer.schedule(event_handler, path, recursive=True)

    observer.start()    
        
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()   
        
    observer.join()        
    



def opc_ua_client():
    """
    thread, opc ua client.
    
    """
    try:
        while True:
            msg = q2.get()
            
            print("opc client")
            
            print(msg)
            
            time.sleep(1)
    except KeyboardInterrupt:
        pass    

connected = set()


async def handler(websocket, path):
    
    """
    websockets handler
    
    """
    
    connected.add(websocket)
    
    try:
        
        while True:
            
            data = q1.get()        
            
            print(data)
            
            print(connected)
            print(">>>")
            
            try:
                
                await websocket.send(json.dumps(data))  
                ack = await websocket.recv()
                q2.put(ack)
                print(ack)
               
            except Exception as ex:
                connected.remove(websocket)
                print(ex)

    finally:
            # Unregister.
            print("remove")
            connected.remove(websocket)
    
    print('hhh')
    
def main():
    
    """
    
    
    """
    
    t1 = threading.Thread(target=timer)
    t1.start()
    
    t2 = threading.Thread(target=watcher)
    t2.start()    
    
    t3 = threading.Thread(target=opc_ua_client)
    t3.start()     
    
    start_server = websockets.serve(handler, '127.0.0.1', 5678)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    
    main()
    
