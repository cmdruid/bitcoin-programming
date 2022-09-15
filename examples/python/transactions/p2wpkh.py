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

from sys import path

path.append( '.' )
path.append( '..' )

from lib.encoder import encode_tx, encode_script
from lib.helper import decode_address, hash_script, get_txid

## Replace this with your own bech32 address.
address = 'bcrt1qgl0gmk0ljucd90m0qa42qstaakl9lkdnhdxzq9'

## We decode the address into the witness version and program script.
version, program = decode_address(address)

print(f'Witness Version: {version}')
print(f'Witness Program: {program}')

## The initial spending transaction. This tx spends a previous utxo,
## and commits the funds to our P2WPKH transaction.

p2wpkh = encode_tx({
    'version':
    1,
    'vin': [{
        'txid':
        '58fe5e0ee8eb2ecba77ff16576651b38acfa3972891e08f8e71bc9246a46f6af',
        'vout': 0,
        'script_sig': [],
        'sequence': 0xFFFFFFFF
    }],
    'vout': [{
        'value': 2499999000,
        'script_pubkey': [ version, program ]
    }],
    'locktime':
    0
})

## Since we have the complete transaction, we can calculate the transaction ID.
txid = get_txid(p2wpkh)

print('\nTxid:\n' + txid)
print('\nHex:\n' + p2wpkh)