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

## Resources
**LND Documentation**  
https://github.com/lightningnetwork/lnd/blob/master/docs/INSTALL.md

**LND Sample Configuration File**  
https://github.com/lightningnetwork/lnd/blob/master/sample-lnd.conf