
"""
watch path

http://ginstrom.com/scribbles/2012/05/10/continuous-integration-in-python-using-watchdog/
http://brunorocha.org/python/watching-a-directory-for-file-changes-with-python.html

"""

import sys
import time

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler,FileSystemEventHandler

import logging
import logging.config

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s>%(levelname)s:%(name)s: %(message)s '
                    '(%(filename)s:%(lineno)d)',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'rotate_file': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'watch.log',
            'encoding': 'utf8',
            'maxBytes': 100000,
            'backupCount': 1,
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'rotate_file'],
            'level': 'DEBUG',
        },
    }
}

logging.config.dictConfig(LOGGING)


class EventHandler(FileSystemEventHandler):
    """
    ['event_type', 'is_directory', 'key', 'src_path']
    """
     
    def on_created(self, event):
        """ test """
        #print(dir(event))
        if not event.is_directory:
            #print(event.key)
            print(event.event_type)
            print(event.src_path)
        
        print("=="*20)        
        
        
    def on_moved(self, event):
        #print(event)
        #print("-2-")
        pass
        
    def on_modified(self, event):
        """ test """
        #observer.unschedule(watch)
        #unschedule_finished.set() #?
        """
        print(event.is_directory)
        #print(event.key)
        print(event.event_type)
        print(event.src_path)
        
        print("=="*20)
        print("-3-")
        """
        pass

def main():
    """ main """
    """
    logging.basicConfig(level=logging.INFO,
                        
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    """
    path = '../data'
    
    event_handler = EventHandler()
    #event_handler = LoggingEventHandler()
    
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