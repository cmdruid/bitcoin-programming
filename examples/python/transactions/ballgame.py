#!/usr/bin/env python3
import json, os, sys

sys.path.append(os.path.dirname(__file__).split('/transactions')[0])

from copy import deepcopy

from lib.hash       import hash160
from lib.signatures import sign_tx
from lib.encoder    import encode_tx, encode_script
from lib.helper     import hash_script, get_txid
from lib.rpc        import RpcSocket

## Setup our RPC socket.
fee = 1000
rpc = RpcSocket({ 'wallet': 'regtest' })
assert rpc.check()

## Get utxo data for each of our participants.
alice_utxo = rpc.get_utxo(0)
bob_utxo = rpc.get_utxo(1)

## Get receiving keys and addresses:
alice_recv = rpc.get_recv()
bob_recv   = rpc.get_recv()

## Configure the transaction fee.
tx_fee = 1000

## The locking script.
script_words = [
    'OP_IF',
    'OP_HASH160',
    'e81bfa71da56f187cce1319ee773dabf56988e95',
    'OP_EQUALVERIFY',
    alice_recv['pub_key'],
    'OP_CHECKSIG',
    'OP_ELSE',
    'OP_HASH160',
    '0f79cd7e22364ff5ed1c6c381f60b0a53d84be19',
    'OP_EQUALVERIFY',
    bob_recv['pub_key'],
    'OP_CHECKSIG',
    'OP_ENDIF'
]

## We hash the above program with a sha256. This will lock the
## output to accept the program script which matches the hash.
script_hash = hash_script(script_words, fmt='sha256')

## This is the hex-encoded script that we will present in order to 
## unlock and spend the output. It should decode to match the script hash.
witness_script = encode_script(script_words, prepend_len=False).hex()

## This is the total value of the locking script.
total_value = alice_utxo['value'] + bob_utxo['value'] - tx_fee

## The locking transaction. This tx spends the participant utxos.
locking_tx = {
    'version': 1,
    'vin': [
      {
        'txid': alice_utxo['txid'],
        'vout': alice_utxo['vout'],
        'script_sig': [],
        'sequence': 0xFFFFFFFF
      },
      {
        'txid': bob_utxo['txid'],
        'vout': bob_utxo['vout'],
        'script_sig': [],
        'sequence': 0xFFFFFFFF
      }
    ],
    'vout': [{
        'value': total_value,
        'script_pubkey': [ 0, script_hash ]
    }],
    'locktime':0
}

## Get txid for the locking script.
locking_raw  = encode_tx(locking_tx)
locking_txid = get_txid(locking_raw)

## Each participant signs the locking transaction.
alice_signature = sign_tx(
  locking_tx, 
  0, 
  alice_utxo['value'], 
  alice_utxo['pubkey_hash'], 
  alice_utxo['priv_key']
)

bob_signature = sign_tx(
  locking_tx, 
  1, 
  bob_utxo['value'], 
  bob_utxo['pubkey_hash'], 
  bob_utxo['priv_key']
)

## Add the signatures and pubkeys to the witness field.
locking_tx['vin'][0]['witness'] = [ alice_signature, alice_utxo['pub_key'] ]
locking_tx['vin'][1]['witness'] = [ bob_signature, bob_utxo['pub_key'] ]

print(f'''
Locking Tx:
{json.dumps(locking_tx, indent=2)}

Locking Txid:
{locking_txid}

Locking Tx Value:
{total_value}

Locking Tx Hex:
{encode_tx(locking_tx)}

Witness hash:
{script_hash}

Witness Program:
{witness_script}
''')

## Setup a redeem transaction.
redeem_tx = {
    'version': 1,
    'vin': [
      {
        'txid': locking_txid,
        'vout': 0,
        'script_sig': [],
        'sequence': 0xFFFFFFFF
      },
    ],
    'vout':[
        {
          'value': total_value - tx_fee,
          'script_pubkey': []
        },
    ]
}

## Configure redeem TX for Alice
alice_tx = deepcopy(redeem_tx)
alice_tx['vout'][0]['script_pubkey'] = [ 0, alice_recv['pubkey_hash'] ]
alice_sig = sign_tx(alice_tx, 0, total_value, witness_script, alice_recv['priv_key'])
alice_tx['vin'][0]['witness'] = [
  alice_sig,
  'ab' * 32, 
  '01', 
  witness_script
]

## Configure redeem TX for Bob.
bob_tx = deepcopy(redeem_tx)
bob_tx['vout'][0]['script_pubkey'] = [ 0, bob_recv['pubkey_hash'] ]
bob_sig = sign_tx(bob_tx, 0, total_value, witness_script, bob_recv['priv_key'])
bob_tx['vin'][0]['witness'] = [
  bob_sig,
  'ab' * 31 + 'ac', 
  '00', 
  witness_script
]

print(f'''
Alice's Redeem Tx:
{json.dumps(alice_tx, indent=2)}

Alice's Redeem Tx Hex:
{encode_tx(alice_tx)}

Bob's Redeem Tx:
{json.dumps(bob_tx, indent=2)}

Bob's Redeem Tx Hex:
{encode_tx(bob_tx)}
''')