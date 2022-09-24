#!/usr/bin/env python3

"""
Example of a Pay-to-Script-Hash (P2SH) transaction.

P2SH is next in the evolution of Bitcoin transactions. Instead of 
locking the transaction to the hash of a public key, we lock it to 
the hash of a Bitcoin Script program. This moves the storage of the 
script program itself to the transaction input.

"""

import os, sys

sys.path.append(os.path.dirname(__file__).split('/transactions')[0])

from lib.encoder import encode_tx, encode_script
from lib.helper  import encode_address, decode_address, hash_script
from lib.hash    import hash160, hash256
from lib.sign    import sign_tx
from lib.rpc     import RpcSocket

## Setup our RPC socket.
rpc = RpcSocket({ 'wallet': 'regtest' })
assert rpc.check()

## Get a utxo for Alice.
alice_utxo  = rpc.get_utxo(0)
fund_value = alice_utxo['value'] - 1000

## Get a payment address for Bob.
bob_funding_txout  = rpc.get_recv(fmt='base58')
bob_funding_hash   = decode_address(bob_funding_txout['address'])
bob_spending_txout = rpc.get_recv(fmt='base58')
bob_spending_hash  = decode_address(bob_spending_txout['address'])

## Convert the secret to bytes, then hash using hash160 function.
secret_message = 'superisatestnet'
secret_bytes   = secret_message.encode('utf8').hex()
secret_hash    = hash160(secret_bytes).hex()

## Here is the script we will be using.
lock_script_words = [
    'OP_HASH160', secret_hash, 'OP_EQUALVERIFY', 
    'OP_DUP', 'OP_HASH160', bob_funding_hash, 'OP_EQUALVERIFY',
    'OP_CHECKSIG'
]

## This is the hex-encoded data that we will present to unlock the output.
lock_script_code = encode_script(lock_script_words, prepend_len=False).hex()

## This is the hash of the script. The output will be locked to this script hash.
locking_script_hash = hash_script(lock_script_words)

funding_tx = {
    'version': 1,
    'vin': [{
        'txid': alice_utxo['txid'],
        'vout': alice_utxo['vout'],
        'script_sig': [],
        'sequence': 0xFFFFFFFF
    }],
    'vout': [{
        'value': fund_value,
        'script_pubkey': ['OP_HASH160', locking_script_hash, 'OP_EQUAL']
    }],
    'locktime': 0
}

## Since we have the complete transaction, we can calculate the transaction ID.
funding_txid = hash256(bytes.fromhex(encode_tx(funding_tx)))[::-1].hex()

## The redeem script is a basic Pay-to-Pubkey-Hash template.
utxo_redeem_script = f"76a914{alice_utxo['pubkey_hash']}88ac"

## We are signing Alice's UTXO using BIP143 standard.
alice_signature = sign_tx(
    funding_tx,             # The transaction.
    0,                      # The input being signed.
    alice_utxo['value'],    # The value of the utxo being spent.
    utxo_redeem_script,     # The redeem script to unlock the utxo. 
    alice_utxo['priv_key']  # The private key to the utxo pubkey hash.
)

## Include the arguments needed to unlock the redeem script.
funding_tx['vin'][0]['witness'] = [ alice_signature, alice_utxo['pub_key'] ]

spending_tx = {
    'version': 1,
    'vin': [{
        'txid': funding_txid,
        'vout': 0,
        'script_sig': [],
        'sequence': 0xFFFFFFFF
    }],
    'vout': [{
        'value': fund_value - 1000,
        'script_pubkey': ['OP_DUP', 'OP_HASH160', bob_spending_hash, 'OP_EQUALVERIFY', 'OP_CHECKSIG']
    }],
    'locktime': 0
}

## Since we have the complete transaction, we can calculate the transaction ID.
spending_txid = hash256(bytes.fromhex(encode_tx(spending_tx)))[::-1].hex()

## Bob is signging to release the funds.
bob_signature = sign_tx(
    spending_tx,                   # The transaction.
    0,                             # The input being signed.
    fund_value,                    # The value of the utxo being spent.
    lock_script_code,              # The redeem script to unlock the utxo. 
    bob_funding_txout['priv_key']  # The private key to the utxo pubkey hash.
)

spending_tx['vin'][0]['script_sig'] = [ 
    bob_signature, bob_funding_txout['pub_key'], secret_bytes, lock_script_code 
]

print(f'''
## Pay-to-Script-Hash Example ##

-- Funding Transaction Id --
{funding_txid}

-- Alice UTXO --
     Txid : {alice_utxo['txid']}
     Vout : {alice_utxo['vout']}
    Value : {alice_utxo['value']}
     Hash : {alice_utxo['pubkey_hash']}

-- Funding Address --
  Address : {encode_address(locking_script_hash)}
    Coins : {fund_value}

-- Funding Tx Hex --
{encode_tx(funding_tx)}

-- Redeem Transaction Id --
{funding_txid}

-- Redeem Tx Hex --
{encode_tx(spending_tx)}

''')
