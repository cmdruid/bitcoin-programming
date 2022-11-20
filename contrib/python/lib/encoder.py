from .hash import hash256
from .codes import get_opcode, get_sigflag


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
        program = encode_script(witness[-1])
        raw = len(witness).to_bytes(1, 'little')
        for i in range(0, len(witness) - 1):
            word = format_word(witness[i])
            if word != b'\x00':
              raw += write_varint(len(word))
            raw += word
        return raw + program
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
            word = check_opcode(word)
            if type(word) == int:
                # Append word as an opcode.
                raw += word.to_bytes(1, 'little')
            else:
                # Append word as an argument.
                word = format_word(word)
                raw += word_size(word)
                raw += word
    elif type(script) == str:
        # If the script is already a hex string, return bytes.
        raw = bytes.fromhex(script)
    else:
        raise Exception(f'Invalid script format: {type(script)}')
    if prepend_len:
        # Prepend total length of bytes as a varint.
        raw = write_varint(len(raw)) + raw
    return raw

def hash_prevouts(inputs, anypay):
    ''' Combine all input prevout fields,
        then return a digest.
    '''
    if anypay:
        return b'0' * 32
    raw_prev = b''
    for txin in inputs:
        raw_prev += bytes.fromhex(txin['txid'])[::-1]
        raw_prev += txin['vout'].to_bytes(4, 'little')
    return hash256(raw_prev)


def hash_sequence(inputs, sighash, anypay):
    ''' Combine all input sequence fields, 
        then return a digest. 
    '''
    if anypay or sighash in [ 'SINGLE', 'NONE' ]:
        return b'0' * 32
    raw_seq = b''
    for txin in inputs:
        raw_seq += txin['sequence'].to_bytes(4, 'little')
    return hash256(raw_seq)


def hash_outputs(outputs, sighash, input_idx=None):
    ''' Combine all output fields,
        then return a digest.
    '''
    raw_out = b''
    if sighash == 'ALL':
        for txout in outputs:
            raw_out += txout['value'].to_bytes(8, 'little')
            raw_out += encode_script(txout['script_pubkey'])
        return hash256(raw_out)
    elif sighash == 'SINGLE' and type(input_idx) == int:
        if input_idx < len(outputs):
            txout = outputs[txin_idx]
            raw_out += txout['value'].to_bytes(8, 'little')
            raw_out += encode_script(txout['script_pubkey'])
        return hash256(raw_out)
    else:
        return b'0' * 32


def encode_sighash(obj, txin_idx, txin_value, script, **kwargs):
    ''' Generate the message digest that is used
        to sign a BIP143 Segwit transaction.
    '''
    version  = obj.get('version', 1)
    inputs   = obj.get('vin', [])
    outputs  = obj.get('vout', [])
    locktime = obj.get('locktime', 0)
    sighash  = kwargs.get('sighash', 'ALL')
    anypay   = kwargs.get('anypay', False)
    redeem_script = kwargs.get('redeem_script', None)

    # Encode the transaction version number.
    raw = encode_version(version)

    # Append a digest of the input 
    # prevouts and sequence fields.
    raw += hash_prevouts(inputs, anypay)
    raw += hash_sequence(inputs, sighash, anypay)

    # Append all information for the
    # transaction that we are signing.
    txin = inputs[txin_idx]
    raw += bytes.fromhex(txin['txid'])[::-1]
    raw += txin['vout'].to_bytes(4, 'little')

    # Append the script being used to redeem the funds.
    if type(script) == str:
        raw_script = bytes.fromhex(script)
        raw += write_varint(len(raw_script)) + raw_script
    elif type(script) == list:
        raw += encode_script(script)
    else:
        raise Exception('There is no script to sign!')

    raw += txin_value.to_bytes(8, 'little')
    raw += txin['sequence'].to_bytes(4, 'little')

    # Append a digest of the outputs,
    # plus append the locktime.
    raw += hash_outputs(outputs, sighash, txin_idx)
    raw += encode_locktime(locktime)

    # Append the sighash flag.
    flag = get_sigflag(sighash)
    if anypay:
        flag += 0x80
    raw += flag.to_bytes(4, 'little')

    # Hash256 the raw string, then return the result.
    return hash256(raw).hex()

def check_opcode(word):
    ''' Check if word is an opcode, 
        and return the integer value.
    '''
    if type(word) == str:
        if 'OP_' in word:
            return get_opcode(word)
    return word

def format_word(word):
    ''' We are type-checking the variable, 
        and adjusting the format if needed. 
    '''
    word_type = type(word)
    if word_type == str:
        return bytes.fromhex(word)
    elif word_type == int:
        return word.to_bytes(1, 'little')
    elif word_type == bytes:
        return word
    else:
        raise Exception(f'Invalid word type: "{word}" = {word_type}')


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
