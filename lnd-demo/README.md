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
./alice/lcli newaddress p2wkh
# Start Alice node.
./bob/lnd --configfile=lnd.conf
# Setup wallet for Alice
./bob/lcli create
# Get a funding address for Alice.
./bob/lcli newaddress p2wkh
```

## Resources
**LND Documentation**  
https://github.com/lightningnetwork/lnd/blob/master/docs/INSTALL.md

**LND Sample Configuration File**  
https://github.com/lightningnetwork/lnd/blob/master/sample-lnd.conf