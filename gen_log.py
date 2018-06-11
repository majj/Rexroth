

import time
from logbook import Logger, RotatingFileHandler



handler = RotatingFileHandler('test.log', mode='a', encoding='utf-8', level=0, format_string=None, delay=False, max_size=2048, backup_count=5, filter=None, bubble=False)

handler.push_application()

log = Logger('My Awesome Logger')


i = 1

while True:
    
    i = i + 1
    log.debug("msg %d" %(i))
    
    time.sleep(0.5)