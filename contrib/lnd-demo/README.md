# LND Software Demo
Basic demo of the LND software.

## Setting up Bitcoin Core.
Make sure your bitcoin.conf includes the following configurations:

```conf
## Add these configurations.

chain=regtest # or whichever chain you wish to use.
server=1
daemon=1
zmqpubrawblock=tcp://127.0.0.1:28332
zmqpubrawtx=tcp://127.0.0.1:28333
```

Once configured, startup bitcoin core, either using `bitcoind` for a background process, or `bitcoin-qt` for the user application.

## Setting up two LND instances.
```bash
# Start Alice node.
./alice/lnd --configfile=lnd.conf
# Setup wallet for Alice
./alice/alice-cli create
# Get a funding address for Alice.
./alice/alice-cli newaddress p2wkh # Fund this address using Bitcoin Core.

# Start Bob node.
./bob/lnd --configfile=lnd.conf
# Setup wallet for Alice
./bob/bob-cli create
# Get a funding address for Bob.
./bob/bob-cli newaddress p2wkh # Fund this address using Bitcoin Core.
```

## Opening a channel.
```bash
# Get pubkey identity of Bob's node.
./bob/bob-cli getinfo
# Have Alice peer with Bob.
./alice/alice-cli connect bob_pubkey@localhost:9737 # Bob's IP:PeerPort
# Have Alice open a channel with Bob.
./alice/alice-cli openchannel --node_key=<bob_pubkey> --local_amt=1000000
# Mine a few blocks to confirm the channel transaction.
./bitcoin-cli generatetoaddress 6 <any_payment_address>
```

## Sending a payment to Bob.
```bash
# Have Bob generate an invoice.
./bob/bob-cli addinvoice --amt=10000
# Have Alice pay the invoice.
./alice/alice-cli sendpayment --pay_req=<encoded_invoice>
# Check Alice channel balance.
./alice/alice-cli channelbalance
# Check Bob channel balance.
./bob/bob-cli channelbalance
```

## Running this demo on other networks (like Testnet)

The above examples and configurations are for connecting to the regtest network. If you would like to run this demo on the testnet network (or mainnet), then you will need to update the following configurations.

```sh
## In bitcoin.conf
chain=test
## In alice/lnd.conf and bob/lnd.conf
bitcoin.network=testnet
```

## Resources
**LND Documentation**  
https://github.com/lightningnetwork/lnd/blob/master/docs/INSTALL.md

**LND Sample Configuration File**  
https://github.com/lightningnetwork/lnd/blob/master/sample-lnd.conf

**Demo transaction between two nodes (docker)**  
https://github.com/lightningnetwork/lnd/tree/master/docker

**Docker Containers**  
https://www.docker.com

**Polar**  
One-click Bitcoin Lightning networks.  
https://lightningpolar.com
