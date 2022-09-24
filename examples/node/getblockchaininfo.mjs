import jsonRpc from './nodelib/json-rpc.mjs'

const { result, error } = await jsonRpc('getblockchaininfo')

if (error) throw error

console.log(result)