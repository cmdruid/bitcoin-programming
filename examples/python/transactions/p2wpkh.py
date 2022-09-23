#!/usr/bin/env python3

"""
Example of a Pay-to-Witness-Pubkey-Hash (P2WPKH) transaction.

Pay-to-Witness is a new convention that brings major upgrades to 
Bitcoin Script:

 - The "script_sig" field has been depreciated, and instead the burden 
   of storing script code has been moved to the end of the transaction.
   (called the "witness data")
   
 - Locking scripts are now preceeded with a version number, meaning that
   the script parsing engine can be upgraded to future versions.

 - The previously-disabled "sequence" field has been revived, and can now
   be used to signal certain new features (RBF, OP_CHECKSEQUENCEVERIFY).
 
 - Malleability of the transaction Id has been fixed, meaning we can now 
   reliably sign a funding transaction and utilize it off-chain, without 
   worrying about the funding transaction diverging from the signature.

 - Locking scripts are now encoded in the Bech32 address format, which
   provides superier readability and error-detection.

This moves the storage of the script program itself to the transaction 
inputs, rather than the outputs. Bitcoin nodes need to store a list of 
unspent transaction outputs (utxo set, or chainstate) in order to quickly 
validate all new transactions which spend them, so moving the burden of
program scripts (which take up the majority of a transaction) away from
the chainstate helps with scalability.

In order to unlock a P2SH transaction, the spending transaction will 
have to provide any arguments to the script, plus the script itself.
This input script will be hashed and checked against the hash stored
in the output's locking script. If the hashes match, then the input
script will be executed with the provided arguments.

Specify a funding utxo, then use your wallet to 
sign and broadcast the transaction. This will transfer control of the 
funds to the script hash.

You can generate a block in order to commit this transaction 
to the blockchain (if you are using regtest).

To unlock and spend the script back to one of our recipient addresses,
we will create a second transaction. Since we are not checking signatures
within our script, this second transaction does not need to be signed.

(it is dangerous to lock real coins to a script that doesn't check for signatures)
"""

import os, sys

sys.path.append(os.path.dirname(__file__).split('/transactions')[0])

from lib.encoder import encode_tx, encode_script
from lib.helper  import decode_address, hash_script, get_txid
from lib.sign    import sign_tx
from lib.rpc     import RpcSocket

## Setup our RPC socket.
rpc = RpcSocket({ 'wallet': 'regtest' })
assert rpc.check()

## First, we will lookup an existing utxo,
## and use that to fund our transaction.
utxo = rpc.get_utxo(0)

## We will also grab a new receiving address,
## and lock the funds to this address.
recv = rpc.get_recv()

## We decode the address into the witness version and program script.
version, pubkey_hash = decode_address(recv['address'])

print(f'Witness Version: {version}')
print(f'Witness Program: {pubkey_hash}')

## The initial spending transaction. This tx spends a previous utxo,
## and commits the funds to our P2WPKH transaction.

new_tx = {
    'version': 1,
    'vin': [{
        'txid': utxo['txid'],
        'vout': utxo['vout'],
        'script_sig': [],
        'sequence': 0xFFFFFFFF
    }],
    'vout': [{
        'value': utxo['value'] - 1000,
        'script_pubkey': [ version, pubkey_hash ]
    }],
    'locktime':0
}

## Since we have the complete transaction, we can calculate the transaction ID.
new_hex  = encode_tx(new_tx)
new_txid = get_txid(new_hex)

## Sign the transaction using our key-pair from the utxo.
redeem_script = f'76a914{pubkey_hash}88ac'
signature = sign_tx(
  new_tx, 
  0,
  utxo['value'], 
  redeem_script,
  utxo['priv_key']
)

## Add the signature and public key to the transaction.
new_tx['vin'][0]['witness'] = [ signature, utxo['pub_key'] ]

## Since we have the complete transaction, we can calculate the transaction ID.
print('\nTxid:\n' + new_txid)
print('\nHex:\n' + encode_tx(new_tx))