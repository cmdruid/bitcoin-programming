import jsonRpc from '../nodelib/json-rpc.mjs'

const txid      = "524210773484f1008d13cc1981a2772a60349195d114723026883f1c8c209d65"
const vout      = 0
const recipient = "bcrt1q8gvqxpaqfqs2xrkh93lcwatvfjvxmkkt39k4dx" 
const amount    = 1.499

const txInputs  = [
  {
    "txid": txid,
    "vout": vout,
  }
]

const txOutputs = [
  {
    [recipient]: amount
  }
]

const { result: unsignedHex } = await jsonRpc('createrawtransaction', [ txInputs, txOutputs ])
const signedHex = await jsonRpc('signrawtransactionwithwallet', unsignedHex, 'legacy')

console.log(signedHex)

const { result: decodedJson } = await jsonRpc('decoderawtransaction', signedHex)

console.log(decodedJson)