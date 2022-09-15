"""
Example of a Pay-to-Witness-Script-Hash using basic addition.
"""

from lib.encoder import encode_tx, encode_script

from lib.helper import (
    decode_address, 
    get_txid, 
    hash160, 
    hash256,
    hash_script
)

## Update this information to use one of your existing unspent 
## transaction outputs (utxo). See 'listunspents' for more info.
funding_txid = 'ecd795120b5aa56ebd5ed6c8db7439b5e5e8fb3a6ba254cd702f8adabc9705e8'
funding_vout = 0
funding_value = 5000000000

## Here is the script that we will be using.
script_words = ['OP_ADD', 'OP_5', 'OP_EQUAL']

## This is the version number for the witness program 
## interpreter. We'll be sticking to version 0.
witness_version = 0

## We hash the above program, then provide a witness version
## along with a 256-bit hash. This will lock the transaction 
## output to accept the program script which matches the hash.
script_hash = hash_script(script_words, fmt='sha256')

## This is the hex-encoded script that we will present in order to 
## unlock and spend the output. It should decode to match the script hash.
witness_script = encode_script(script_words, prepend_len=False).hex()

## The initial locking transaction. This spends the utxo from our funding 
## transaction, and moves the funds to the utxo for our witness program.
locking_tx = encode_tx({
    'version': 1,
    'vin': [{
        'txid': funding_txid,
        'vout': funding_vout,
        'script_sig': [],
        'sequence': 0xFFFFFFFF
    }],
    'vout': [{
        'value': funding_value - 1000,
        'script_pubkey': [ witness_version, script_hash ]
    }],
    'locktime': 0
})

## Now that we have the complete transaction, 
## we can calculate the transaction ID.
locking_txid = get_txid(locking_tx)

## Replace this with your own bech32 address.
receive_address = 'bcrt1q3xgcc6wtxkzd5s80578cr9v94r7s5jstjl2kd2'

## Bech32 addresses will decode into a witness version and pubkey hash.
witness_version, pubkey_hash = decode_address(receive_address)

## Since our above program script does not check for signatures, you can 
## broadcast this transaction without providing a signature
spending_tx = encode_tx({
    'version': 1,
    'vin': [{
        'txid': locking_txid,
        'vout': 0,
        'script_sig': [],
        'sequence': 0xFFFFFFFF,
        'witness': [ '02', '03', witness_script ]
    }],
    'vout': [{
        'value': funding_value - 2000,
        'script_pubkey': [ witness_version, pubkey_hash ]
    }],
    'locktime':0
})

def addition_example():
    print(f'''
# Pay-to-Witness-Script-Hash Example using addition

Locking Txid:
{locking_txid}

Witness Script:
{witness_script}

Script Hash:
{script_hash}

Locking Tx:
{locking_tx}

Unlocking Tx:
{spending_tx}

''')