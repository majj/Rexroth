
import logging
import json

import psycopg2
import falcon

log = logging.getLogger('api')

class PgResource(object):
    """
    call PostgreSQL function
    """
    
    def __init__(self, config):        
        """
        
        require: install pgbouncer for connection pool
        
        """
        
        self.config = config
        log.debug(config)
        
        self.connect()
    
    def connect(self):
        self.conn = psycopg2.connect(self.config['dsn'])
        
        self.cur = self.conn.cursor()
        
    def reconnect(self):
        """
        reconnect pg
        """
        
        self.connect()
    
    
    def on_get(self, req, resp):        
        """Handles GET requests"""
        
        t = req.get_param('t')
        
        func = req.get_param('func')

        param = {'t':t}        
        
        sql = """select %s('%s') as %s""" %(func, json.dumps(param), func)
        
        log.debug(sql)
        
        data = {'error':None}
        
        try:
            self.cur.execute(sql)
            
            data = self.cur.fetchone()
       
        except Exception as ex:
            
            data = {'error':str(ex)}
            
        finally:
            
            self.conn.commit()
        
        resp.status = falcon.HTTP_200  # This is the default status
        #resp.body = ('falcon' + req.path + ' ; ' + str(data) )
        log.debug("%s,%s,%s" %(req.host, req.path, sql))
        resp.json = {"data": data, "path":req.path, "sql":sql }
        
    def on_post(self, req, resp):
        """
        
        """