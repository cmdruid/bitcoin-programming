#!/usr/bin/env -S node --experimental-modules --no-warnings

async function bitcoinCli(method, ...args) {
  const user = 'bitcoin',
        pass = 'password',
          url = '127.0.0.1',
        port = 18443

  console.log('Arguments:', args)

  return fetch(`http://${url}:${port}`, {
    method: 'POST',
    headers: {
      'Authorization': 'Basic ' + btoa(user + ':' + pass),
      'content-type': 'application/json'
    },
    body: JSON.stringify({
      "jsonrpc": "1.0", 
      "id":"test", 
      "method": method, 
      "params": [ ...args ]
    })
  })
}

bitcoinCli('getblockchaininfo')
  .then(async (res) => {
    if (res.ok) {
      console.log(await res.json())
    } else {
      console.log('Request failed with status:', res.status)
    }
  })
