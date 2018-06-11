

"""
api gatway

angular -- jsonrpc --> falcon --> pg --> plv8(coffeescript) --> json

"""

import sys
import ast
import logging
from logging.config import dictConfig
from logging.handlers import RotatingFileHandler

#from wsgiref import simple_server
from waitress import serve
import toml
import falcon
import falcon_jsonify

from api_pg import PgResource

# load app config file
with open('app.toml', encoding='utf-8') as conf_file:
    config = toml.loads(conf_file.read())

# load logging config file
with open(config['logging']['conf'], encoding='utf-8') as fh:
    LOGGING = ast.literal_eval(fh.read())    

dictConfig(LOGGING)

log = logging.getLogger('main')

def main():
        
    # falcon.API instances are callable WSGI apps
    #api = falcon.API()

    api = falcon.API(middleware=[
        falcon_jsonify.Middleware(help_messages=True),
    ])

    # Resources are represented by long-lived class instances
    pgclient = PgResource(config['db'])

    # things will handle all requests to the '/things' URL path
    api.add_route('/', pgclient)

    api.add_route('/q', pgclient)    
    
    #httpd = simple_server.make_server('127.0.0.1', 8000, api)
    log.info('start')
    #httpd.serve_forever()
    
    serve(api, host='0.0.0.0', port=8000, threads = 6, _quiet=True)
    
if __name__ == '__main__':
    
    main()