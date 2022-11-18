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

## Our secret code.
secretcode = 'superisatestnet'.encode('utf8')

## Setup our RPC socket connection.
rpc = RpcSocket({ 'wallet': 'regtest' })

## Select the first utxo we have available.
utxo = rpc.get_utxo(0)

## Generate some new addresses.
send_address   = rpc.call('getnewaddress')
change_address = rpc.call('getnewaddress')

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
            'value': 0,
            'script_pubkey': [ 'OP_RETURN', secretcode ]
        }
    ],
    'locktime': 0
}

## Encode our transaction, then hash it to get the txid.
locking_hex  = encode_tx(locking_tx)
locking_txid = hash256(bytes.fromhex(locking_hex))[::-1].hex()

## Sign our transaction.
signature = sign_tx(
  locking_tx,
  utxo['vout'],
  utxo['value'],
  utxo['pubkey_hash'],
  utxo['priv_key']
)

## Append our signature and public key to the witness field.
locking_tx['vin'][0]['witness'] = [ signature, utxo['pub_key'] ]

## Here is our completed transaction.
print('\nTxid:\n' + locking_txid)
print('\nHex:\n' + encode_tx(locking_tx))
