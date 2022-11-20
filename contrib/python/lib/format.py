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