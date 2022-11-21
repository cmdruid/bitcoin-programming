# LND Software Demo

This is a basic demo that demonstrates how to setup two lightning nodes using LND, connect them to your Bitcoin Core node, open a channel between them, and send a payment.

The demo requires that you already have Bitcoin Core installed and setup on your machine.

You may need to replace the `lnd` and `lncli` binaries with a version that is built for your operating system. To download these binaries for other operating systems, please visit the releases page [located here](https://github.com/lightningnetwork/lnd/releases/tag/v0.15.4-beta).

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

By default, this demo is configured to run in regtest mode, and connect to a Bitcoin core node that is installed in the default directory. If you run ainto any issues, and need to make further configurations to your LND nodes, please check out [this guide](https://github.com/lightningnetwork/lnd/blob/master/docs/INSTALL.md) for installing LND, and [this link](https://github.com/lightningnetwork/lnd/blob/master/sample-lnd.conf) for configuring the lnd.conf file.

```bash
# Start Alice node.
./alice: lnd --configfile=lnd.conf
# Setup wallet for Alice
./alice: alice-cli create
# Get a funding address for Alice.
./alice: alice-cli newaddress p2wkh
# If you ever need to unlock the wallet, use this.
./alice: alice-cli unlock

# Start Bob node.
./bob: lnd --configfile=lnd.conf
# Setup wallet for Bob
./bob: bob-cli create
# Get a funding address for Bob.
./bob: bob-cli newaddress p2wkh
# If you ever need to unlock the wallet, use this.
./bob: bob-cli unlock
```

## Opening a channel.
```bash
# Get pubkey identity of Bob's node.
./bob: bob-cli getinfo
# Have Alice peer with Bob.
./alice: alice-cli connect bob_pubkey@localhost:9737 # Bob's IP:PeerPort
# Have Alice open a channel with Bob.
./alice: alice-cli openchannel --node_key=<bob_pubkey> --local_amt=25000
# Mine a few blocks to confirm the channel transaction.
bitcoin-cli generatetoaddress 6 <any_payment_address>
```

## Sending a payment to Bob.
```bash
# Have Bob generate an invoice.
./bob: bob-cli addinvoice --amt=1000
# Have Alice pay the invoice.
./alice: alice-cli sendpayment --pay_req=<encoded_invoice>
# Check Alice channel balance.
./alice: alice-cli channelbalance
# Check Bob channel balance.
./bob: bob-cli channelbalance
```

## Running this demo on other networks (like Testnet)

The above examples and configurations are for connecting to the regtest network. If you would like to run this demo on the testnet network (or mainnet), then you will need to update the following configurations.

```sh
## In bitcoin.conf
chain=test

## In alice/lnd.conf and bob/lnd.conf:
#bitcoin.regtest=1
#bitcoind.rpccookie=~/.bitcoin/regtest/.cookie
bitcoin.testnet=1
bitcoind.rpccookie=~/.bitcoin/testnet3/.cookie

## In alice-cli and bob-cli:
NETWORK="testnet"
```

## Resources
**LND Documentation**  
https://github.com/lightningnetwork/lnd/blob/master/docs/INSTALL.md

**LND Releases**  
https://github.com/lightningnetwork/lnd/releases/tag/v0.15.4-beta

**LND Sample Configuration File**  
https://github.com/lightningnetwork/lnd/blob/master/sample-lnd.conf

**Demo transaction between two nodes (docker)**  
https://github.com/lightningnetwork/lnd/tree/master/docker

**Docker Containers**  
https://www.docker.com

**Polar**  
One-click Bitcoin Lightning networks.  
https://lightningpolar.com
