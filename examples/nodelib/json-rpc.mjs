import { webcrypto as crypto } from 'crypto'

export default async function jsonRpc(method, args, wallet) {
  const user = 'bitcoin',
        pass = 'password',
        url  = '127.0.0.1',
        port = 18443,
        uuid = crypto.randomUUID()

  args = (Array.isArray(args))
    ? args
    : [ args ]

  wallet = (wallet)
    ? 'wallet/' + wallet
    : ''

  console.log('Arguments:', args)

  return fetch(`http://${url}:${port}/${wallet}`, {
    method: 'POST',
    headers: {
      'Authorization': 'Basic ' + btoa(user + ':' + pass),
      'content-type': 'application/json'
    },
    body: JSON.stringify({
      "jsonrpc": "1.0",
      "id": uuid,
      "method": method, 
      "params": args
    })
  })
  .then(res => res.json())
}
