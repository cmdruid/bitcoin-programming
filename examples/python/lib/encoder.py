from .codes import get_opcode


def encode_tx(obj, **kwargs):
    ''' Serialize a transaction into byte-code. '''

    version = obj.get('version', 1)
    inputs = obj.get('vin', [])
    outputs = obj.get('vout', [])
    locktime = obj.get('locktime', 0)

    # Check if witness data exists in inputs.
    has_witness = check_witness(inputs)

    # Encode the transaction version number.
    raw = encode_version(version)

    if has_witness:
        # If there is witness data present,
        # add the witness flag to transaction.
        raw += b'\x00\x01'

    # Encode the inputs and outputs.
    raw += encode_txin(inputs)
    raw += encode_txout(outputs)

    # If present, append witness data.
    for txin in inputs:
        if has_witness and 'witness' in txin:
            raw += encode_witness(txin['witness'])

    # Encode the locktime.
    raw += encode_locktime(locktime)

    return raw.hex()


def encode_version(version):
    ''' Encode the version field of a transaction. '''
    return version.to_bytes(4, 'little')


def encode_txin(inputs):
    ''' Encode each transaction input. '''
    raw = write_varint(len(inputs))
    for txin in inputs:
        raw += bytes.fromhex(txin['txid'])[::-1]
        raw += txin['vout'].to_bytes(4, 'little')
        raw += encode_script(txin['script_sig'])
        raw += txin['sequence'].to_bytes(4, 'little')
    return raw


def encode_txout(outputs):
    ''' Encode each transaction output. '''
    raw = write_varint(len(outputs))
    for txout in outputs:
        raw += txout['value'].to_bytes(8, 'little')
        raw += encode_script(txout['script_pubkey'])
    return raw


def check_witness(inputs):
    for txin in inputs:
        if 'witness' in txin:
            return True
    return False


def encode_witness(witness):
    ''' Encode the witness data for a transaction. '''
    if type(witness) == list:
        length = len(witness).to_bytes(1, 'little')
        return length + encode_script(witness, prepend_len=False)
    if type(witness) == str:
        return bytes.fromhex(witness)
    if type(witness) == bytes:
        return witness
    raise Exception(f'Invalid data type: "{witness}" = {type(witness)}')


def encode_locktime(locktime):
    ''' Encoder for the locktime field of a transaction. '''
    return locktime.to_bytes(4, 'little')


def encode_script(script, prepend_len=True):
    ''' Encode a provided script into raw bytes,
        and return it as a raw byte-string.
    '''
    raw = b''
    if type(script) == list:
        # If the script is a list,
        # iterate through the words.
        for word in script:
            # Adjust word formatting if needed.
            word = format_word(word)
            if type(word) != int:
               # Append current word as a variable.
                raw += word_size(word)
                raw += word         
            else:
                # Append current word as an opcode.
                raw += word.to_bytes(1, 'little')
    elif type(script) == str:
        # If the script is already a hex string, return bytes.
        raw = bytes.fromhex(script)
    else:
        raise Exception(f'Invalid script format: {type(script)}')
    if prepend_len:
        # Prepend total length of bytes as a varint.
        raw = write_varint(len(raw)) + raw
    return raw


def format_word(word):
    ''' We are type-checking the variable, 
        and adjusting the format if needed. 
    '''
    if type(word) == str:
        if 'OP_' in word:
            return get_opcode(word)
        return bytes.fromhex(word)
    elif type(word) in [int, bytes]:
        return word
    else:
      raise Exception(f'Invalid word type: "{word}" = {type(word)}')


def word_size(word):
  ''' Get the length of a word, and return
     its varint size in byte-string format. 
  '''
  MAX_SIZE = 0x208
  word_size = len(word)
  if word_size <= 0x4b:
      # Encode the current word size.
      return word_size.to_bytes(1, 'little')
  elif 0x4b < word_size < 0x100:
      # Encode the word size as a varint byte.
      op_datapush1 = int(0x4c).to_bytes(1, 'little')
      return op_datapush1 + word_size.to_bytes(1, 'little')
  elif 0x100 <= word_size <= MAX_SIZE:
      # Encode the word size as two varint bytes.
      op_datapush2 = int(0x4d).to_bytes(1, 'little')
      return op_datapush2 + word_size.to_bytes(2, 'little')
  else:
      raise ValueError(
        f'Word "{word}" is too large: {word_size} > {MAX_SIZE} bytes.'
      )


def write_varint(num):
    ''' Write a variable integer in byte format. '''
    if num < 0xfd:
        return bytes([num])
    elif num < 0x10000:
        return b'\xfd' + num.to_bytes(2, 'little')
    elif num < 0x100000000:
        return b'\xfe' + num.to_bytes(4, 'little')
    elif num < 0x10000000000000000:
        return b'\xff' + num.to_bytes(8, 'little')
    else:
        raise ValueError(f'Int too large: {num}')
