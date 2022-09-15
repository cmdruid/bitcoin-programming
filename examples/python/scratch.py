#!/usr/bin/env python3

from sys import path
from secp256k1 import PrivateKey

path.append('.')

from lib.encoder import encode_tx, encode_sighash
from lib.helper import convert_to_wif, encode_address
from lib.hash import hash160, hash256

## Based on the 'P2SH-P2WPKH' test example for BIP-143:
# https://github.com/bitcoin/bips/blob/master/bip-0143.mediawiki

test_tx = {
  'version': 1,
  'vin': [
    {
      'txid': '77541aeb3c4dac9260b68f74f44c973081a9d4cb2ebe8038b2d70faa201b6bdb',
      'vout': 1,
      'script_sig': [],
      'sequence': 0xfffffffe
    },
  ],
  'vout': [
    {
      'value': 199996600,
      'script_pubkey': ['OP_DUP', 'OP_HASH160', 'a457b684d7f0d539a46a45bbc043f35b59d0d963', 'OP_EQUALVERIFY', 'OP_CHECKSIG']
    },
    {
      'value': 800000000,
      'script_pubkey': ['OP_DUP', 'OP_HASH160', 'fd270b1ee6abcaea97fea7ad0402e8bd8ad6d77c', 'OP_EQUALVERIFY', 'OP_CHECKSIG']
    }
  ],
  'locktime': 1170
}

test_raw = '0100000001db6b1b20aa0fd7b23880be2ecbd4a98130974cf4748fb66092ac4d3ceb1a54770100000000feffffff02b8b4eb0b000000001976a914a457b684d7f0d539a46a45bbc043f35b59d0d96388ac0008af2f000000001976a914fd270b1ee6abcaea97fea7ad0402e8bd8ad6d77c88ac92040000'

raw_tx = encode_tx(test_tx)

print(f'encoder test pass: {raw_tx == test_raw}')

pubkey_hash = '79091972186c449eb1ded22b78e40d009bdf0089'
redeem_script = f'1976a914{pubkey_hash}88ac'
sighash = encode_sighash(test_tx, 0, 1000000000, redeem_script=redeem_script)

test_sighash = '64f3b0f4dd2bb3aa1ce8566d220cc74dda9df97d8490cc81d89d735c92e59fb6'

print(f'sighash encoder test pass: {sighash == test_sighash}')

key = 'eb696a065ef48a2192da5b28b694f87544b30fae8327c4510137a922f32c6dcf'

privkey = PrivateKey(bytes(bytearray.fromhex(key)), raw=True)
sig_raw = privkey.ecdsa_sign(bytes(bytearray.fromhex(sighash)), raw=True)
signature = privkey.ecdsa_serialize(sig_raw).hex() + '01'

test_sig = '3044022047ac8e878352d3ebbde1c94ce3a10d057c24175747116f8288e5d794d12d482f0220217f36a485cae903c713331d877c1f64677e3622ad4010726870540656fe9dcb01'

print(f'signature test pass: {signature == test_sig}')
