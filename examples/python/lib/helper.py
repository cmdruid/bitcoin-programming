from hashlib import sha256
from .ripemd import ripemd160
from .encoder import encode_script
from .base58 import base58_address, decode_base58
from .bech32 import encode, decode


def get_bytes(data):
    ''' Format input data and return as byte-string.
    '''
    if type(data) == int:
        return data.to_bytes(1, 'little')
    if type(data) == str:
        return bytes.fromhex(data)
    if type(data) == bytes:
        return data
    raise Exception(f'Unknown format: {type(data)}')


def hash256(data):
    ''' Performs a hash256 operation.
    '''
    data = get_bytes(data)
    return sha256(sha256(data).digest()).digest()


def hash160(data):
    ''' Performs a hash160 operation.
    '''
    data = get_bytes(data)
    return ripemd160(sha256(data).digest())


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


def encode_address(hash, fmt='bech32', hrp='bcrt', ver=0):
    ''' Encodes a Bitcoin address or key into a given format. 
    '''
    hash = get_bytes(hash)
    if fmt == 'bech32':
        return encode(hrp, ver, hash)
    if fmt == 'base58':
        return base58_address(hash)
    raise Exception(f'Unknown format: {fmt}')


def decode_address(address):
    ''' Decodes a Bitcoin address or key into hex format.
    '''
    if address[0] in [1, 2, 3, 'm', 'n', 'M', 'N']:
       return decode_base58(address).hex()
    elif address[0:2] in ['bc', 'tb']:
        hrp, _ = address.split('1', 1)
        ver, prog = decode(hrp, address)
        prog = b''.join([ x.to_bytes(1, 'little') for x in prog ]).hex()
        return [ ver, prog ]
    else:
        raise Exception(f'Unknown format: {address}')