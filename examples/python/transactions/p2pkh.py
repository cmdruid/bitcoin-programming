#!/usr/bin/env python3

"""
Example of a Pay-to-Pubkey-Hash (P2PKH) transaction.

P2PKH is the most common type of transaction that is used 
on the Bitcoin payment network.

We will construct a transaction that is locked to the hash
of a public key. In order to unlock the tranasction, a user
will have to provide the un-hashed public key, along with a
digital signature which shares that same public key.

Specify a funding utxo and recipient address, then use your
wallet to sign and broadcast the transaction. This will transfer 
control of the funds to the pubkey hash that is encoded within 
the recipient address. 

You can generate a block in order to commit this transaction 
to the blockchain (if you are using regtest).
"""

from sys import path

sys.path.append(os.path.dirname(__file__).split('/transactions')[0])

from lib.encoder import encode_tx
from lib.helper import decode_address
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

## We decode the address to get the actual hash.
pubkey_hash = decode_address(recv['address'])

## The spending transaction. We are including a basic P2PKH script in 
## the script_pubkey field. This script can later be unlocked by a new 
## transaction input which provides the correct public key and signature.
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
        'script_pubkey': ['OP_DUP', 'OP_HASH160', pubkey_hash, 'OP_EQUALVERIFY', 'OP_CHECKSIG']
    }],
    'locktime': 0
}

## Encode the transaction into raw hex,
## and calculate the transaction ID
locking_hex  = encode_tx(locking_tx)
locking_txid = hash256(bytes.fromhex(locking_hex))[::-1].hex()

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
locking_tx['vin'][0]['witness'] = [ signature, utxo['pub_key'] ]

print(f'''
# Pay-to-Pubkey-Hash Example

Recipient Address:
{recipient_address}

Pubkey Hash:
{pubkey_hash}

Spending Tx:
{spending_tx}
''')