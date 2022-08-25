#!/usr/bin/env python

from pylib.rpc import json_rpc

## Specify an unspent transaction output to spend.
utxo_txid = "61f3b7016bf1ecc3987b8805207e79362e4de8026682e149107999b779426e3a"
utxo_vout = "1"

## Specify a recipient.
recipient = ""

result = json_rpc('getblockchaininfo')

print(result)

