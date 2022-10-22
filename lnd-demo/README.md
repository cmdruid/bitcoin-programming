# LND Software Demo
Basic demo of the LND software.

## Startup up LND
```bash
## Starting LND from scratch (with bitcoind running in regtest)
./lnd --bitcoin.active --bitcoin.regtest --bitcoin.node=bitcoind

## Starting LND from a configuration file.
./lnd --configfile=lnd.conf

## Using LNCLI on an alternative network and data path.
./lncli --network regtest --macaroonpath /PATH/TO/ADMIN/MACAROON getinfo

## Get macaroon hex
cat /PATH/TO/MACAROON | xxd -ps -u -c 1000
```

## Setting up two LND instances.
```bash
# Start Alice node.
./alice/lnd --configfile=lnd.conf
# Setup wallet for Alice
./alice/lcli create
# Get a funding address for Alice.
./alice/lcli newaddress p2wkh # Fund this address using Bitcoin Core.

# Start Alice node.
./bob/lnd --configfile=lnd.conf
# Setup wallet for Alice
./bob/lcli create
# Get a funding address for Alice.
./bob/lcli newaddress p2wkh # Fund this address using Bitcoin Core.
```

## Opening a channel.
```bash
# Get pubkey identity of Bob's node.
./bob/lcli getinfo
# Have Alice peer with Bob.
./alice/lcli connect bob_pubkey@localhost:9737 # Bob's IP:Port
# Have Alice open a channel with Bob.
./alice/lcli openchannel --node_key=<bob_pubkey> --local_amt=1000000
# Mine a few blocks to confirm the channel transaction.
./bitcoin-cli generatetoaddress 6 <any_payment_address>
```

## Sending a payment to Bob.
```bash
# Have Bob generate an invoice.
./bob/lcli addinvoice --amt=10000
# Have Alice pay the invoice.
./alice/lcli sendpayment --pay_req=<encoded_invoice>
# Check Alice channel balance.
./alice/lcli channelbalance
# Check Bob channel balance.
./bob/lcli channelbalance
```

## Resources
**LND Documentation**  
https://github.com/lightningnetwork/lnd/blob/master/docs/INSTALL.md

**LND Sample Configuration File**  
https://github.com/lightningnetwork/lnd/blob/master/sample-lnd.conf

**Demo transaction between two nodes (docker)**  
https://github.com/lightningnetwork/lnd/tree/master/docker

