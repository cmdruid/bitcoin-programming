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

from lib.encoder import encode_tx
from lib.helper import decode_address

## Update this information to use one of your existing unspent 
## transaction outputs (utxo). See 'listunspents' for more info.
funding_txid = '8251512dde40cc88818a49ca5c7719d1a8918305b4fb0b247d04bf4b8f9606d9'
funding_vout = 0
funding_value = 5000000000

## Replace this with your own address. You can use the 'getnewaddress'
## command. Bech32 formatted addresses are provided by default, but you 
## can generate an older Base58 address by specifying:
## 'getnewaddress -address_type legacy'
recipient_address = 'mfh8XHh2oPi15imgxh7xsKd4XGhEcHevCG' 

## We decode the address into the actual pubkey hash.
pubkey_hash = decode_address(recipient_address)

## The spending transaction. We are including a basic P2PKH script in 
## the script_pubkey field. This script can later be unlocked by a new 
## transaction input which provides the correct public key and signature.
spending_tx = encode_tx({
    'version': 1,
    'vin': [{
        'txid': funding_txid,
        'vout': funding_vout,
        'script_sig': [],
        'sequence': 0xFFFFFFFF
    }],
    'vout': [{
        'value': funding_value,
        'script_pubkey': ['OP_DUP', 'OP_HASH160', pubkey_hash, 'OP_EQUALVERIFY', 'OP_CHECKSIG']
    }],
    'locktime': 0
})

def p2pkh_example():
    print(f'''
# Pay-to-Pubkey-Hash Example

Recipient Address:
{recipient_address}

Pubkey Hash:
{pubkey_hash}

Spending Tx:
{spending_tx}
''')