import rpc from './lib/rpc.mjs'

const result = await rpc('getblockchaininfo')

console.log(result)