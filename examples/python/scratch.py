#!/usr/bin/env python3

import os, sys

sys.path.append(os.path.dirname(__file__).split('/transactions')[0])

from lib.helper import encode_address, decode_address
from lib.rpc import RpcSocket

## Setup our RPC socket.
rpc = RpcSocket({ 'wallet': 'regtest' })
assert rpc.check()

## First, we will lookup an existing utxo,
## and use that to fund our transaction.
# utxo = rpc.get_recv(fmt='base58')

# print(utxo)
# print(decode_address(utxo['address']))
# print(encode_address(utxo['pubkey_hash'], fmt='base58'))

## First, we will lookup an existing utxo,
## and use that to fund our transaction.
utxo = rpc.get_recv()

print(utxo)
print(decode_address(utxo['address']))
print(encode_address(utxo['pubkey_hash']))