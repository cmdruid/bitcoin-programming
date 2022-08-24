## https://requests.readthedocs.io
import json, requests

def json_rpc(method, config={}, **params):

  username = config.username if 'username' in config else 'bitcoin'
  password = config.password if 'password' in config else 'password'
  fullUrl  = config.fullUrl  if 'fullUrl'  in config else 'http://127.0.0.1:18443'

  body = json.dumps({
    "jsonrpc": "1.0", 
    "id":"test", 
    "method": str(method), 
    "params": [ p for p in params ]
  })

  r = requests.post(
    fullUrl, 
    auth=(username, password),
    data=body
  )

  return r.json()
