#!/usr/bin/env -S node --experimental-modules --no-warnings --trace-uncaught

import { webcrypto as crypto } from 'crypto'
import { fileURLToPath } from 'url';

// Unpack arguments from the current process.
const [ nodepath, sourcepath, method, ...params ] = process.argv

// Check if this script is being executed from shell.
const filepath = fileURLToPath(import.meta.url)
const isExecutedFromShell = Boolean(sourcepath === filepath)

if (isExecutedFromShell) {
  if (!method) {
    // If method is blank, show help text and exit.
    const filename = sourcepath.split('/')[-1]
    console.log(
      `Usage: ./${filename} [ METHOD ] [ PARAMS ]\n\n` +
      'Basic implementation of using json-rpc with node.js\n\n' +
      `Example: ./${filename} getblockchaininfo`
    )
    process.exit(0)
  } else {
    // Else, print our results.
    const result = await rpc(method, params)
    console.log('Result:', result)
  }
}

export default async function rpc(method, args = [], config = {}) {
  /** Send a JSON-RPC call to the configured server. */

  const user = config.user   || 'bitcoin',    // RPC-Auth Username
        pass = config.pass   || 'password',   // RPC-Auth Password
        url  = config.url    || '127.0.0.1',  // URL to your Bitcoin node.
        port = config.port   || 18443         // Port to your RPC interface.

  let wallet = config.wallet || ''            // Name of wallet to use.

  // Random identifer for our request.
  const requestId = crypto.randomUUID()

  // Authorization string for our request.
  const authString = Buffer.from(user + ':' + pass).toString('base64')

  // Make sure our args are in an array.
  args = (Array.isArray(args)) ? args : [ args ]

  try {
  
    if (wallet) {
      // If a wallet is specified, ensure that the wallet file
      // exists and is loaded, then configure the url endpoint.
      await loadWallet(wallet)
      wallet = 'wallet/' + wallet
    }

    // Confgigure our request object.
    const request = {
      method: 'POST',
      headers: {
        'Authorization': 'Basic ' + authString,
        'content-type': 'application/json'
      },
      body: JSON.stringify({
        "jsonrpc": "1.0",
        "id": requestId,
        "method": method,
        "params": args
      })
    }

    // Fetch a response from our node.
    const response = await fetch(`http://${url}:${port}/${wallet}`, request)

    // If the response fails, throw an error.
    if (!response.ok && !response.json) {
      throw `Request for '${method}' failed with status ${response.status}: ${response.statusText}`
    }

    // Convert our response to json.
    const { result, error } = await response.json()

    // If the RPC call has an error, unpack and throw the error.
    if (error) {
      const { code, message } = error
      if (code === -1) {
        throw `RPC command ${method} failed with syntax error. Please check your arguments.`
      } else { throw `RPC command ${method} failed with error: ${message}` }
    }

    return result

  } catch(err) { throw err }
}

async function isWalletLoaded(walletName) {
  /** Check if the specified wallet is loaded
   *  within the bitcoin-core node.
   * */
  return rpc('listwallets')
    .then((wallets) => wallets && wallets.includes(walletName))
}

async function isWalletExists(walletName) {
  /** Check if the specified wallet exists within 
   *  the host filesystem for bitcoin-core.
   * */
  return rpc('listwalletdir')
    .then(({ wallets }) => wallets.find(el => el.name === walletName))
}

async function loadWallet(walletName) {
  /** Ensure that the specified wallet is loaded for 
   *  the bitcoin-core node and available to access.
   * */

  if (await isWalletLoaded(walletName)) {
    // If wallet is already loaded, return.
    return true
  }

  if (!(await isWalletExists(walletName))) {
    // If wallet does not exist, throw error.
    throw 'Wallet file does not exist!'
  }

  return rpc('loadwallet', [ walletName ])
    .then(({ name, warning }) => {
      if (warning || name !== walletName) {
        // If there was a problem with loading, throw error.
        throw `Wallet failed to load cleanly: ${warning}`
      }
      return true
    })
}
