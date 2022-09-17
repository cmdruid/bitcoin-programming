import json, requests, uuid
from .hash   import hash160
from .helper import decode_address

class RpcSocket:
    ''' Basic implementation of a JSON-RPC interface. '''
    def __init__(self, opt):
        url  = opt.get('url', '127.0.0.1')
        port = opt.get('port', 18443)

        self.fullUrl  = f'http://{url}:{port}/'
        self.username = opt.get('username', 'bitcoin')
        self.password = opt.get('password', 'password')
        self.wallet   = opt.get('wallet', None)
        self.initFlag = False

    def init(self):
        ''' Initialize the RPC object. '''
        if self.wallet:
            self.loadWallet()
            self.fullUrl += f'wallet/{self.wallet}'
        

    def call(self, method, args = []):
        ''' Make an RPC call using the 
            specified method and arguments.
        '''
        # Make sure to initialize the RPC object first.
        if not self.initFlag:
            self.initFlag = True
            self.init()
        
        # Format the arguments before the call.
        args = args if type(args) is list else [ args ]

        # Construct the body of the reuqest.
        body = json.dumps({
            "jsonrpc": "1.0",
            "id": uuid.uuid4().urn.split(':')[-1],
            "method": method,
            "params": args
        })
        
        # Make the request to the server.
        response = requests.post(
            self.fullUrl,
            auth=(self.username, self.password),
            data=body
        )
        
        # If the response code is not 200, fail here.
        if response.status_code != 200:
            raise Exception(f'Response failed with error: {response.status_code}')
        
        data = response.json()
        
        # If the data includes an error message, fail here.
        if data['error']:
            if data['error']['code'] == -1:
                raise Exception(f'RPC command {method} failed with syntax error. Please check your arguments.')
            else:
                err_msg = data["error"]["message"]
                raise Exception(f'RPC command {method} failed with error: {err_msg}')
        
        return data['result']

    def check(self):
        res = self.call('getblockchaininfo')
        return 'chain' in res


    def isWalletLoaded(self):
        wallets = self.call('listwallets')
        return self.wallet in wallets


    def isWalletExists(self):
        wallets = self.call('listwalletdir')
        return [ w['name'] for w in wallets if w['name'] == self.wallet ]


    def loadWallet(self):
        if self.isWalletLoaded():
            return True
        if not self.isWalletExists():
            raise f'Wallet "{self.wallet}" does not exist!'

        result = self.call('loadwallet', [ self.wallet ])

        if result['warning'] or result['name'] != self.wallet:
            raise 'Wallet failed to load cleanly: {}'.format(result['warning'])
        
        return True

    def get_utxo(self, idx):
        utxos = self.call('listunspent')
        if len(utxos) <= idx:
          raise Exception('You are requesting an index out of range!')
        address = utxos[idx]['address']
        encoded_key = self.call('dumpprivkey', address)
        public_key  = self.call('getaddressinfo', address)['pubkey']
        pubkey_hash = hash160(public_key).hex()

        return {
            'address': address,
            'priv_key': decode_address(encoded_key),
            'pub_key': public_key,
            'pubkey_hash': pubkey_hash,
            'redeem_script': f'1976a914{pubkey_hash}88ac',
            'txid': utxos[idx]['txid'],
            'vout': utxos[idx]['vout'],
            'value': int(utxos[idx]['amount'] * 100000000)
        }

    def get_recv(self, address=None):
        if address is None:
            address = self.call('getnewaddress')
        encoded_key = self.call('dumpprivkey', address)
        public_key  = self.call('getaddressinfo', address)['pubkey']
        pubkey_hash = hash160(public_key).hex()
        return {
            'address': address,
            'priv_key': decode_address(encoded_key),
            'pub_key': public_key,
            'pubkey_hash': pubkey_hash,
            'redeem_script': f'1976a914{pubkey_hash}88ac',
        }
