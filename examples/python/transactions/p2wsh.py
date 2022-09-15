"""
Example of a Pay-to-Witness-Script-Hash transaction.

First, we will construct a transaction that is locked to
a script hash. We will keep the program script simple: 
evaluate that a secret pre-image matches a given hash.

Specify a funding utxo, then sign and broadcast the first 
transaction. This will transfer control of the funds to the 
new unspent output. You can generate a block in order to 
commit this transaction to your regtest blockchain.

Next, specify a receive address, then sign and broadcast the
second transaction. This will spend the previous transaction
by providing the pre-image of the secret message, along with
the program script.

The receive address for the second transaction should be
picked up by your wallet automatically, and listed as a new 
utxo under 'listunspent' once you generate another block.
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
funding_txid = '8251512dde40cc88818a49ca5c7719d1a8918305b4fb0b247d04bf4b8f9606d9'
funding_vout = 0
funding_value = 5000000000

## Replace this default preimage with your own secret.
secret_preimage = 'weareallsatoshi'

## Convert the secret to bytes, then hash using hash160 function.
secret_bytes = secret_preimage.encode('utf8').hex()
secret_hash = hash160(secret_bytes).hex()

## Here is the script that we will be using.
script_words = ['OP_HASH160', secret_hash, 'OP_EQUAL']

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
receive_address = 'bcrt1qgl0gmk0ljucd90m0qa42qstaakl9lkdnhdxzq9'

## Bech32 addresses will decode into a witness version and pubkey hash.
witness_version, pubkey_hash = decode_address(receive_address)

## This transaction will redeem the previous utxo by providing the secret 
## pre-image, plus the witness program. The funds are being locked to the
## pubkey hash from the above address. Once the transaction is confirmed,
## your wallet software should recognize this utxo as spendable.
##
## Since our above program script does not check for signatures, you can 
## broadcast this transaction without providing a signature
spending_tx = encode_tx({
    'version': 1,
    'vin': [{
        'txid': locking_txid,
        'vout': 0,
        'script_sig': [],
        'sequence': 0xFFFFFFFF,
        'witness': [ secret_bytes, witness_script ]
    }],
    'vout': [{
        'value': funding_value - 2000,
        'script_pubkey': [ witness_version, pubkey_hash ]
    }],
    'locktime':0
})

def p2wsh_example():
    print(f'''
# Pay-to-Witness-Script-Hash Example

Locking Txid:
{locking_txid}

Witness Script:
{witness_script}

Script Hash:
{script_hash}

Secret Bytes:
{secret_bytes}

Secret Hash:
{secret_hash}

Locking Tx:
{locking_tx}

Unlocking Tx:
{spending_tx}

''')
