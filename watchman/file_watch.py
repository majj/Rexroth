
"""
watch path
"""

import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler,FileSystemEventHandler

class EventHandler(FileSystemEventHandler):
    """
    ['event_type', 'is_directory', 'key', 'src_path']
    """
     
    def on_created(self, event):
        """ test """
        print(dir(event))
        
    def on_moved(self, event):
        print(event)
        
    def on_modified(self, event):
        """ test """
        #observer.unschedule(watch)
        #unschedule_finished.set() #?
        print(event.is_directory)
        #print(event.key)
        print(event.event_type)
        print(event.src_path)
        
        print("=="*20)

def main():
    """ main """
    
    logging.basicConfig(level=logging.INFO,
                        
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
                        
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    #event_handler = EventHandler()
    event_handler = LoggingEventHandler()
    
    observer = Observer()
    
    observer.schedule(event_handler, path, recursive=True)
    
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
            
    observer.join()
    
if __name__ == "__main__":
    main()