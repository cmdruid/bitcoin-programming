""" Creating a Raw Transaction
  Example of creating and sending a raw transaction using json-rpc.
  This example uses the native fetch built-into Node v18. If you use
  an earlier version of node, you may need to install the 'node-fetch'
  package from npm via the command 'npm install -g node-fetch'
"""

## Append local pylib to path.
from sys import path
path.append('../pylib')

from rpc import rpc
import json

response = rpc('getblockchaininfo')

print(json.dumps(response, indent=2))