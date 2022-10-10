## Setup our RPC socket.
fee = 1000
rpc = RpcSocket({ 'wallet': 'regtest' })
assert rpc.check()