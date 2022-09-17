## This example requires secp256k1 package.
# pip3 install secp256k1
# https://https://pypi.org/project/secp256k1
from secp256k1 import PrivateKey

from .encoder  import encode_sighash

def sign_tx(tx_data, txin_idx, txin_val, script, key, **kwargs):
    ''' Sign an unspent transaction's output (utxo) 
        over to the input of a new transaction.
    '''
    sighash = kwargs.get('sighash', 'ALL')
    anypay  = kwargs.get('anypay', False)

    # Parse the redeem script for the transaction.
    if type(script) == str and len(script) == 40:
        script = f'76a914{script}88ac'

    # Convert the private key into a signing key.
    sign_key = PrivateKey(bytes.fromhex(key), raw=True)

    # Calculate a message digest for us to sign.
    msg_digest = encode_sighash(tx_data, txin_idx, txin_val, script, **kwargs)

    ## Sign the message digest.
    sig_bytes = sign_key.ecdsa_sign(bytes.fromhex(msg_digest), raw=True)
    signature = sign_key.ecdsa_serialize(sig_bytes).hex() + '01'

    return signature