#!/usr/bin/env python3

"""
Example of using OP_RETURN to commit data to the blockchain.
"""

import os, sys

sys.path.append(os.path.dirname(__file__).split('/transactions')[0])

from lib.hash import hash256
from lib.sign import sign_tx
from lib.encoder import encode_tx, encode_script
from lib.helper import decode_address, hash_script, get_txid
from lib.rpc import RpcSocket

## Replace this with your own bech32 address.
send_address = 'bcrt1qgl0gmk0ljucd90m0qa42qstaakl9lkdnhdxzq9'
change_address = 'bcrt1q6clg0q407cw39s55w90uevtxhccaqujsjkf456'

## We decode the address into the witness version and program script.
send_version, program = decode_address(send_address)
change_version, program = decode_address(change_address)

## Setup our RPC socket.
rpc = RpcSocket({ 'wallet': 'regtest' })
utxo = rpc.get_utxo(0)

## The initial spending transaction. This tx spends a previous utxo,
## and commits the funds to our P2WPKH transaction.

locking_tx = {
    'version': 1,
    'vin': [{
        'txid': utxo['txid'],
        'vout': utxo['vout'],
        'script_sig': [],
        'sequence': 0xFFFFFFFF
    }],
    'vout': [
        {
            'value': 10000,
            'script_pubkey': decode_address(send_address)
        },
        {
            'value': utxo['value'] - 10000 - 1000,
            'script_pubkey': decode_address(change_address)
        },
        {
            'value': 100,
            'script_pubkey': [ 'OP_RETURN', 'superisatestnet'.encode('utf8') ]
        }
    ],
    'locktime': 0
}

locking_hex  = encode_tx(locking_tx)
locking_txid = hash256(bytes.fromhex(locking_hex))[::-1].hex()

signature = sign_tx(
  locking_tx,
  utxo['vout'],
  utxo['value'],
  utxo['pubkey_hash'],
  utxo['priv_key']
)

locking_tx['vin'][0]['witness'] = [ signature, utxo['pub_key'] ]

## Since we have the complete transaction, we can calculate the transaction ID.
print('\nTxid:\n' + locking_txid)
print('\nHex:\n' + encode_tx(locking_tx))