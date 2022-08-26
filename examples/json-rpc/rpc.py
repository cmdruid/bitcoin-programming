## https://requests.readthedocs.io
import json, requests

def json_rpc(method, **params):

  print(params)

  username = 'bitcoin'
  password = 'password'
  fullUrl  = 'http://127.0.0.1:18443'

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

result = json_rpc('getblockchaininfo')

print(result)