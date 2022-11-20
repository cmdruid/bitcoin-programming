from hashlib import sha256
from .encoder import encode_script
from .base58 import base58_address, decode_base58
from .bech32 import encode, decode
from .format import get_bytes
from .hash import hash256, hash160


def hash_script(script, fmt='hash160'):
    ''' Provides the hash for a Bitcoin script program.
    '''
    encoded = encode_script(script, prepend_len=False)
    if fmt == 'hash160':
        return hash160(encoded).hex()
    elif fmt == 'sha256':
        return sha256(encoded).hexdigest()
    else:
        raise Exception(f'Unknown format: {fmt}')


def get_txid(hex):
    ''' Calulates the ID for a completed transaction.
    '''
    tx_hash = hash256(bytes.fromhex(hex))
    return tx_hash[::-1].hex()


def encode_address(string, fmt='bech32', hrp='bcrt', ver=0):
    ''' Encodes a Bitcoin address or key into a given format. 
    '''
    raw = get_bytes(string)
    if fmt == 'bech32':
        return encode(hrp, ver, raw)
    if fmt == 'base58':
        return base58_address(raw)
    raise Exception(f'Unknown format: {fmt}')


def decode_address(address):
    ''' Decodes a Bitcoin address or key into hex format.
    '''
    if address[0] in [1, 2, 3, 'm', 'n', 'M', 'N']:
        return decode_base58(address, size=25).hex()
    if address[0] in ['c', 'L', 'K']:
        decoded = decode_base58(address, size=38)
        return decoded[0:32].hex()
    elif address[0:2] in ['bc', 'tb']:
        hrp, _ = address.split('1', 1)
        ver, prog = decode(hrp, address)
        prog = b''.join([ x.to_bytes(1, 'little') for x in prog ]).hex()
        return [ ver, prog ]
    else:
        raise Exception(f'Unknown format: {address}')


def convert_to_wif(key, testnet=True):
    ver = 0x80 if not testnet else 0xEF
    raw = get_bytes(key + '01')
    return base58_address(raw, ver=ver)
