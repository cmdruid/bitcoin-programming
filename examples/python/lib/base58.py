from hashlib import sha256
from .hash import hash256

## Credit to Jimmy Song. Source:
## https://github.com/cmdruid/programmingbitcoin

ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def encode_base58(s):
    # determine how many 0 bytes (b'\x00') s starts with
    count = 0
    for c in s:
        if c == 0:
            count += 1
        else:
            break
    # convert to big endian integer
    num = int.from_bytes(s, 'big')
    prefix = '1' * count
    result = ''
    while num > 0:
        num, mod = divmod(num, 58)
        result = ALPHABET[mod] + result
    return prefix + result


def base58_address(s, ver=111):
    ## For a guide on which version to use, see:
    ## https://en.bitcoin.it/wiki/Base58Check_encoding
    prefix = ver.to_bytes(1, 'big')
    checksum = hash256(prefix + s)[:4]
    return encode_base58(prefix + s + checksum)


def decode_base58(s, size=25):
    num = 0
    for c in s:
        num *= 58
        num += ALPHABET.index(c)
    combined = num.to_bytes(size, byteorder='big')
    checksum = combined[-4:]
    if hash256(combined[:-4])[:4] != checksum:
        raise ValueError('bad address: {} {}'.format(
            checksum,
            hash256(combined[:-4])[:4]))
    return combined[1:-4]
