#!/usr/bin/env python3

from sys import path
from base64 import b64decode
import json

path.append( '.' )
path.append( '..' )

## Requires secp256k1 package.
# pip3 install secp256k1
# https://https://pypi.org/project/secp256k1
from secp256k1 import PrivateKey

from lib.hash import hash160
from lib.encoder import encode_tx, encode_script, encode_sighash
from lib.helper import encode_address, decode_address, hash_script, get_txid
from lib.rpc import rpc, check_rpc

opt = { 'wallet': 'regtest' }

## Check that our RPC connection is working.
assert check_rpc()

## Get an unspent output from our utxo set.
utxo_set = rpc('listunspent', **opt)
if not len(utxo_set):
    raise Exception('Your utxo set is empty! Try mining some blocks.')
utxo = utxo_set[0]
print(f'Using utxo:\n{json.dumps(utxo, indent=2)}')

## Decode the keypair from the utxo
encoded_key = rpc('dumpprivkey', utxo['address'], **opt)
private_key = decode_address(encoded_key)
public_key  = rpc('getaddressinfo', utxo['address'], **opt)['pubkey']
pubkey_hash = hash160(public_key).hex()

## Convert utxo value to the correct amount in satoshis.
tx_fee = 1000
utxo_value = int(utxo['amount'] * 100000000)

## The spending transaction. This tx spends a previous utxo,
## signed using our extrated private key.
spending_tx = {
    'version':1,
    'vin': [{
        'txid': utxo['txid'],
        'vout': utxo['vout'],
        'script_sig': [],
        'sequence': 0xFFFFFFFF
    }],
    'vout': [{
        'value': utxo_value - tx_fee,
        'script_pubkey': [ 0, pubkey_hash ]
    }],
    'locktime':0
}

## Convert the private key into a signing key.
sign_key = PrivateKey(bytes(bytearray.fromhex(private_key)), raw=True)

## Calculate a message digest for us to sign.
redeem_script = f'1976a914{pubkey_hash}88ac'
msg_digest = encode_sighash(spending_tx, 0, utxo_value, redeem_script=redeem_script)

## Sign the message digest.
sig_bytes = sign_key.ecdsa_sign(bytes(bytearray.fromhex(msg_digest)), raw=True)
signature = sign_key.ecdsa_serialize(sig_bytes).hex() + '01'

## Apply signature and public key to witness data
spending_tx['vin'][0]['witness'] = [ signature, public_key ]

## Get raw hex and id of the transaction.
spending_raw = encode_tx(spending_tx)
spending_txid = get_txid(spending_raw)

print(f'''
Private Key:
{private_key}

Public Key:
{public_key}

Signature:
{signature}

Transaction ID:
{spending_txid}

Transaction Hex:
{spending_raw}
''')