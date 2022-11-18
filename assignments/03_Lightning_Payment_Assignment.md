# Assignment 03 - Lightning Payment

The purpose of this assignment is to demonstrate that you can start a lightning node, open a channel with another peer, send a payment, and close the channel.

## Requirements

* A summary of your work in setting up a lightning channel, making an HTLC payment, then closing the channel. If you used a script to open the channel, or make a payment, please include that as well.

* Please provide the following information:
  - The transaction ID of the open channel transaction.
  - The encoded bolt11 invoice of the payment (starts with lntb).
  - The transaction ID the the close channel transaction.

This payment should take place on the Bitcoin Testnet network. It should be publicly viewable on a Blockchain explorer, such as [mempool.space](https://mempool.space/testnet).

## Examples

You will find some examples of how to start a lightning node in the `lnd-demo` folder. Feel free to use any software implementation of Lightning, such as LND, Core Lightning, Eclair, etc.

**Neutrino Workbench**  
A docker workbench environment, pre-configured for running LND in neutrino mode.  
https://github.com/cmdruid/neutrino-workbench

**Sauron Workbench**  
A docker workbench environment, pre-configured for running Core Lightning using Blockstream API.  
https://github.com/cmdruid/saurons-workbench


## Resources

**Lightning Network Daemon (LND)**  
https://github.com/lightningnetwork/lnd

**Core Lightning (CLN)**  
https://github.com/ElementsProject/lightning

**Eclair (Scala Lightning Node)**  
https://github.com/ACINQ/eclair

**Polar: One-click Lightning Network**  
https://github.com/jamaljsr/polar

**Bitcoin Testnet Faucet**  
https://bitcoinfaucet.uo1.net

**Mempool.space Testnet**  
https://mempool.space/testnet

## Question / Issues

If you have any questions, or run into any issues, please feel free to a question in **#homework-chat** on the [class Discord](https://discord.gg/kCvWQxXuwv)
