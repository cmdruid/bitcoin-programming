# Assignment 01 - Bitcoin Transaction

The purpose of this assignment is to demonstrate that you can construct a valid bitcoin transaction, and broadcast it successfully on the Bitcoin Test Network.

## Requirements

* The txid of the transaction on the Bitcoin Testnet network. It should be publicly viewable on a blockchain explorer, such as [mempool.space](https://mempool.space/testnet).
* If you used a script or program to send the transaction, please include that as well.

You can view an example homework submission in the `examples` folder located [here](examples/01-bitcoin-tx-assignment/README.md).

## Running Bitcoin Core

If you need help setting up and configuring Bitcoin Core, check out the resources below.

 - [Building on Bitcoin Presentation (pdf)](../slides/building-on-bitcoin-core.pdf)
 - [Bitcoin Transactions Workshop (pdf)](../slides/bitcoin-transactions-workshop.pdf)
 - [Links to Running a Node](../resources/run-a-node.md)

## Switching to Testnet

If you are following an example or guide that configures Bitcoin Core to use the __regtest__ network, remember that you will have to update your configuration to use the __test__ network instead. This requires that you start bitcoin core with the `-testnet` flag, or update your `bitcoin.conf` to specify `testnet=1` or `chain=test`.

## Downloading the Testnet Blockchain

When you switch to testnet for the first time, you will have to download the full testnet blockchain. This will typically take a few hours on a fast internet connection.

If you are concerned with the size of the testnet blockchain, make sure to update your `bitcoin.conf` with the setting `prune=1000` in order to keep your blockain size limited to 1000mb size. This is recommended and will save you from storing the entire chain history.

If you would like to download the testnet blockchain as quickly as possible, you can downlaod an archived copy of the chain [at this link](https://mega.nz/file/DolRWSpa#gKEnSjWgVPgCWnipQ8Q20Pjd-yZiH4VeeHaupJ1iM24). Unzip the archive and place the `testnet3` folder within your main data folder for Bitcoin Core (this is usually the same location as your `bitcoin.conf` file).

## Project Templates

You can use the following project template to get a working Bitcoin Core node running within a docker container.

**Satoshi Workbench**  
A docker workbench environment, pre-configured for running bitcoind.  
https://github.com/cmdruid/satoshi-workbench

## More Resources

**Bitcoin Testnet Faucet**  
https://bitcoinfaucet.uo1.net

**Mempool.space Testnet**  
https://mempool.space/testnet

## Question / Issues

If you have any questions, or run into any issues, please feel free to a question in **#homework-chat** on the [class Discord](https://discord.gg/kCvWQxXuwv)
