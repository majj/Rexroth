# -*- coding: utf-8 -*-

import json

import requests

url = "http://127.0.0.1:8000/"

def test_post():
    
    #url = "http://127.0.0.1:8000/"

    payload = {'key1': 'value1', 'key2': 'value2'}

    print(payload)

    ## JSON.stringify in js
    #r = requests.post(url, data=json.dumps(payload))
    
    r = requests.post(url, json=payload)
    
    print(r.status_code)
    
    print(r.headers)
    
    print(r.headers['Content-Type'])

    #print(r.text)
    
    print(r.json())
    
    print("=================")


def test_put():
    
    #url = "http://127.0.0.1:8000/"

    payload = {'key3': 'value3', 'key4': 'value4'}

    #print(payload)

    ## JSON.stringify in js
    #r = requests.post(url, data=json.dumps(payload))
    
    r = requests.put(url, json=payload)
    
    #print(r.status_code)
    
    #print(r.headers)
    
    print(r.headers['Content-Type'])

    #print(r.text)
    
    print(r.json())
    
    print("=================")
    
    
if __name__ == '__main__':
    
    test_post()
    test_put()