import json, requests, uuid

def rpc(method, args = [], **kwargs):
  username = kwargs.get('username', 'bitcoin')
  password = kwargs.get('password', 'password')
  wallet   = kwargs.get('wallet', '')

  url  = kwargs.get('url', '127.0.0.1')
  port = kwargs.get('port', 18443)
  args = args if type(args) is list else [ args ]

  if wallet:
    loadWallet(wallet)
    wallet = 'wallet/' + wallet

  body = json.dumps({
    "jsonrpc": "1.0",
    "id": uuid.uuid4().urn.split(':')[-1],
    "method": method,
    "params": args
  })

  response = requests.post(
    'http://{}:{}/{}'.format(url, port, wallet),
    auth=(username, password),
    data=body
  )

  data = response.json()

  if data['error']:
    if data['error']['code'] == -1:
      raise Exception('RPC command {} failed with syntax error. Please check your arguments.'.format(method))
    else:
      raise Exception('RPC command {} failed with error: {}'.format(method, data['error']['message']))

  return data['result']


def isWalletLoaded(walletName):
  wallets = rpc('listwallets')
  return walletName in wallets


def isWalletExists(walletName):
  wallets = rpc('listwalletdir')
  return [ w['name'] for w in wallets if w['name'] == walletName ]


def loadWallet(walletName):
  if isWalletLoaded(walletName):
    return True
  if not isWalletExists(walletName):
    raise 'Wallet "{}" does not exist!'.format(walletName)

  result = rpc('loadwallet', [ walletName ])

  if result['warning'] or result['name'] != walletName:
    raise 'Wallet failed to load cleanly: {}'.format(wallet['warning'])
  
  return True
