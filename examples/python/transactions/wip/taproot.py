import json, os, sys

sys.path.append(os.path.dirname(__file__).split('/transactions/wip')[0])

from copy import deepcopy

from lib.hash     import hash160
from lib.sign     import sign_tx
from lib.encoder  import encode_tx, encode_script
from lib.helper   import hash_script, get_txid
from lib.rpc      import RpcSocket

