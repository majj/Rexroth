# -*- coding: utf-8 -*-

"""

"""

import time

import zmq

port = 62260
port1 = 62261


class OPC_UA_Client(object):
    
    def __init__(self):
        
        context = zmq.Context()
        self.socket = context.socket(zmq.PAIR)
        self.socket.bind("tcp://*:%s" % port)

    def write(self, url):
        """
        thread, opc ua client.
        
        """
        try:
            while True:
                #msg = writing_queue.get()
                
                msg = self.socket.recv_json()
                
                
                print("opc client - write value here")
                
                print(msg)
                
                #self.socket.send_json({"got":"T"})
                
                time.sleep(1)
        except KeyboardInterrupt:
            pass    
