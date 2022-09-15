#!/usr/bin/env python3

from sys import path
from base64 import b64decode

path.append( '.' )
path.append( '..' )

## Requires libsecp256k1-0 package.
# https://github.com/ArcticTechnology/libsecp256k1-0
#from libsecp256k1_0 import 

from lib.hash import hash160
from lib.encoder import encode_tx, encode_script, encode_sighash
from lib.helper import encode_address, decode_address, hash_script, get_txid
from lib.rpc import rpc

WALLET_NAME = 'test'

## Update this information to use one of your existing unspent 
## transaction outputs (utxo). See 'listunspents' for more info.

## Get an unspent output from our utxo set.
utxo = rpc('listunspent', wallet=WALLET_NAME)[0]

## Use our wallet to fetch a legacy address and pubkey.
legacy_address = rpc('getnewaddress', ['-format', 'legacy'], wallet=WALLET_NAME)
address_info = rpc('getaddressinfo', legacy_address, wallet=WALLET_NAME)

pubkey = address_info['pubkey']
pubkey_hash = hash160(pubkey).hex()

## Convert utxo value to the correct amount in satoshis.
utxo_value = int(utxo['amount'] * 100000000)

## The initial spending transaction. This tx spends a previous utxo,
## and commits the funds to our P2WPKH transaction.

locking_tx = {
    'version':1,
    'vin': [{
        'txid': utxo['txid'],
        'vout': utxo['vout'],
        'script_sig': [],
        'sequence': 0xFFFFFFFF
    }],
    'vout': [{
        'value': utxo_value - 1000,
        'script_pubkey': [ 0, pubkey_hash ]
    }],
    'locktime':0
}

## Get raw hex of the transaction.
locking_raw = encode_tx(locking_tx)

## Since we have the complete transaction, we can calculate the transaction ID.
locking_txid = get_txid(locking_raw)

spending_tx = {
    'version':1,
    'vin': [{
        'txid': locking_txid,
        'vout': 0,
        'script_sig': [],
        'sequence': 0xFFFFFFFF,
    }],
    'vout': [{
        'value': utxo_value - 2000,
        'script_pubkey': [ 0, pubkey_hash ]
    }],
    'locktime':0
}

## Get a message digest of the transaction.
redeem_script = f'1976a914{pubkey_hash}88ac'
msg_digest = encode_sighash(spending_tx, 0, utxo_value - 1000, redeem_script=redeem_script)

## Get a signature of the digest using the address.
b64_sig = rpc('signmessage', [legacy_address, msg_digest], wallet=WALLET_NAME)
signature = b64decode(b64_sig).hex()

## Apply signature and public key to witness data
#spending_tx['vin'][0]['witness'] = [ signature, pubkey ]

## Get raw hex of the transaction.
spending_raw = encode_tx(spending_tx)

print(f'''
Locking Transaction ID:
{locking_txid}

Locking Transaction Hex:
{locking_raw}

Spending Transaction Hex:
{spending_raw}
''')