"""
Example of a Pay-to-Witness-Script-Hash using basic addition.
"""

from sys import path

path.append('.')
path.append('..')

from lib.encoder import encode_tx, encode_script
from lib.helper import decode_address, get_txid, hash_script

## Update this information to use one of your existing unspent 
## transaction outputs (utxo). See 'listunspents' for more info.
funding_txid = 'e365d909ca5793144122bf381af83210d1a9256aa3a5ac20eba8019aa1a66cd1'
funding_vout = 0
funding_value = 2500000000

## Here is the script that we will be using.
script_words = [
    'OP_IF',
    'OP_HASH160',
    'e81bfa71da56f187cce1319ee773dabf56988e95',
    'OP_EQUAL',
    'OP_ELSE',
    'OP_HASH160',
    '0f79cd7e22364ff5ed1c6c381f60b0a53d84be19',
    'OP_EQUAL',
    'OP_ENDIF'
]

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
receive_address = 'bcrt1q66tuvf7tnv3sdj83c3y4wveuqnf8s5rplx3klq'

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
        'witness': [ 'ab' * 32, '00', witness_script ]
    }],
    'vout': [{
        'value': funding_value - 2000,
        'script_pubkey': [ witness_version, pubkey_hash ]
    }],
    'locktime':0
})

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
