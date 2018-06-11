# -*- coding: utf-8 -*-

"""

"""

import ast
import datetime
import time

import zmq

port = 62260
port1 = 62261

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler #LoggingEventHandler,


class EventHandler(FileSystemEventHandler):
    """
    handler for file create event
    ['event_type', 'is_directory', 'key', 'src_path']
    """
    
    def __init__(self,socket):
        
        #context = zmq.Context()
        #print("Connecting to server...")
        
        #self.socket = context.socket(zmq.PUSH)
        
        #self.socket.connect ("tcp://localhost:%s" % port1)
        
        self.socket = socket

        #self.socket.send ("Hello")
        #  Get the reply.
        #message = self.socket.recv()    
    
     
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
                
                #reading_queue.put({"angle act":v})
                #data = msgpack.packb()
                self.socket.send_json ({"angle act":v})
                #message = self.socket.recv()  
            
            #reading_queue.put({"path":file_path})
            #data = msgpack.packb({"path":file_path})
            
            
            #message = self.socket.recv()  
            self.socket.send_json ({"path":file_path})
        
        print("=="*20)        
        
        
    def on_moved(self, event):
        pass
        
    def on_modified(self, event):
        
        pass
        
        
def new_file_watcher(path):    
    """    
    thread, read torque data
    watch FTP folder and get new file creation event.
    """
    
    context = zmq.Context()
    print("Connecting to server...")
    
    socket = context.socket(zmq.PUSH)
    
    socket.connect ("tcp://localhost:%s" % port1)    
    
    
    event_handler = EventHandler(socket)
    
    observer = Observer()

    observer.schedule(event_handler, path, recursive=True)

    observer.start()    
        
    try:
        while True:
            
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            
            socket.send_json({"now":now})
            
            #reading_queue.put({"now":now})            
            
            time.sleep(3)
    except KeyboardInterrupt:
        observer.stop()   
        
    observer.join() 