from hashlib import sha256
from .ripemd import ripemd160
from .format import get_bytes

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