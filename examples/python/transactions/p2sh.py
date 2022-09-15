"""
Example of a Pay-to-Script-Hash (P2SH) transaction.

P2SH is next in the evolution of Bitcoin transactions. Instead of 
locking the transaction to the hash of a public key, we lock it to 
the hash of a Bitcoin Script program.

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

from sys import path

path.append( '.' )
path.append( '..' )

from lib.hash import hash160
from lib.encoder import encode_tx, encode_script
from lib.helper import decode_address, hash_script, get_txid

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

## This is the hex-encoded data that we will present to unlock the output.
script_code = encode_script(script_words, prepend_len=False).hex()

## This is the hash of the script. The output will be locked to this script hash.
script_hash = hash_script(script_words)

## The initial spending transaction. This tx spends a previous utxo,
## and commits the funds to our P2SH script hash.

locking_tx = encode_tx({
    'version': 1,
    'vin': [{
        'txid':
        '477ce8cc20d20d74877692cfba7bb2eadcfb9dd802e7d9418b439d024eb62598',
        'vout': 0,
        'script_sig': [],
        'sequence': 0xFFFFFFFF
    }],
    'vout': [{
        'value': funding_value - 1000,
        'script_pubkey': ['OP_HASH160', script_hash, 'OP_EQUAL']
    }],
    'locktime': 0
})

## Since we have the complete transaction, we can calculate the transaction ID.
locking_txid = get_txid(locking_tx)

## Replace this with your own address. You can use the 'getnewaddress'
## command. Bech32 formatted addresses are provided by default, but you 
## can generate an older Base58 address by specifying:
## 'getnewaddress -address_type legacy'
recipient_address = 'mfh8XHh2oPi15imgxh7xsKd4XGhEcHevCG' 

## We decode the address into the actual pubkey hash.
pubkey_hash = decode_address(recipient_address)

## This transaction demonstrates how to spend the previous P2SH transaction.
## We provide the un-hashed public key, and the un-hashed code of the script.
## As no signature is being verified in the script itself, we do not have to
## sign this transaction before broadcasting it to the network.
spending_tx = encode_tx({
    'version': 1,
    'vin': [{
        'txid': funding_txid,
        'vout': 0,
        'script_sig': [ secret_bytes, script_code ],
        'sequence': 0xFFFFFFFF
    }],
    'vout': [{
        'value': funding_value - 2000,
        'script_pubkey': ['OP_DUP', 'OP_HASH160', pubkey_hash, 'OP_EQUALVERIFY', 'OP_CHECKSIG']
    }],
    'locktime': 0
})

def p2sh_example():
    print(f'''
# Pay-to-Script-Hash Example

Locking Txid:
{locking_txid}

Script Encoded:
{script_code}

Script Hash:
{script_hash}

Secret Bytes:
{secret_bytes}

Secret Hash:
{secret_hash}

Locking Tx:
{locking_tx}

Spending Tx:
{spending_tx}

''')
