/** Creating a Raw Transaction **
 * Example of creating and sending a raw transaction using json-rpc.
 * This example uses the native fetch built-into Node v18. If you use
 * an earlier version of node, you may need to install the 'node-fetch'
 * package from npm via the command 'npm install -g node-fetch'
 */

import rpc from '../lib/rpc.mjs'

// Specify the name of the existing wallet you wish to use.
const walletName = 'regtest'

// List the unspent transaction outputs (UTXOs) available for you to use.
const unspent = await rpc('listunspent', [], { wallet: walletName })

// Specify the TXID and output for the tranasction you wish to use for funds.
const txInputs  = [
  {
    'txid': '279fee58e7f8dba8ca4aaa59a2a1bd700865122780823b3feb9ecf4a3d3ce855',
    'vout': 0,
  }
]

// Specify a recipient address (as the keyname), and the amount you wish to send.
// Make sure to leave at least a 0.00001 difference as a minimum transaction fee.

const txOutputs = [
  { 
    ['bcrt1qmzgpdmwmyxsywejl0q7sueqy225qhhh3du4hwv']: 24.9999
  },
  { 
    ['bcrt1qtas77fv3wypuf4llnmpfjg8nxal6z8qfpgzlqa']: 24.9999
  }
]

/** NOTE
 * Technically there is no minimum fee in the Bitcoin protocol, however in order to
 * combat spam, most node software (including bitcoin-core) requires that some type of
 * minimum fee is set on transactions. This is known as the 'minimum relay fee', and
 * you can inspect this minimum fee yourself using the RPC command 'getnetworkinfo'.
 * 
 * Nodes do not collect on these fees, only the miner which includes the tx in their block.
 * Remember that any positive balance between inputs/outputs is given as a fee to the miners.
 */

// Create a raw transaction template.
const unsignedHex = await rpc('createrawtransaction', [ txInputs, txOutputs ])

console.log('Unsigned Hex:', unsignedHex, '\n')

// Sign the transaction with your wallet (which has access to the UTXOs used for funds)
const { hex: signedHex } = await rpc('signrawtransactionwithwallet', unsignedHex, { wallet: walletName })

console.log('Signed Hex:', signedHex, '\n')

// Let's decode the signed transaction and take a look.
const decodedJson = await rpc('decoderawtransaction', signedHex)

console.log('Decoded tx:', decodedJson, '\n')

// Uncomment and send the tranasction when you're ready!
//const txid = await rpc('sendrawtransaction', signedHex, { wallet: walletName })
//const entry = await rpc('getmempoolentry', txid)
//console.log('Mempool entry:', entry)

// Mine a block to confirm the transaction.
//await rpc('generatetoaddress', [ 1, 'bcrt1qh4eclxq9etatk5aycncdev8h6w9m8l366hq3l2'])