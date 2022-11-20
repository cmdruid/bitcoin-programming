# Assignment 03 - Lightning Payment

The purpose of this assignment is to demonstrate that you can start a lightning node, open a channel with another peer, send a payment, and close the channel.

## Requirements

* The transaction ID of the open channel transaction.
* The encoded bolt11 invoice of the payment (starts with lntb).
* The transaction ID the the close channel transaction.
* If you used a script to open the channel, or make a payment, please include that as well.

The channel and payment should take place on the Bitcoin Testnet network. It should be publicly viewable on a Blockchain explorer, such as [mempool.space](https://mempool.space/testnet).

You can view an example homework submission in the `examples` folder located [here](examples/03-ln-payment-assignment/README.md).

## Setting up a Lightning Channel

You will find an example demo of how to lightning channel in the `contrib/lnd-demo` folder [located here](../contrib/lnd-demo/README.md). Make sure to read about how to reconfigure the demo for using testnet.

## Funding a Channel

Since we cannot generate our own blocks (and coins) on testnet, you will need to send funds to your lightning nodes using a faucet. You will want about 25,000-50,000 satoshis on each of your lightning nodes in order to setup a channel and send payments back and forth. FYI 0.0005 of a bitcoin = 50k satoshis.

You can find a popular testnet faucet here:  

**Bitcoin Testnet Facuet**  
https://bitcoinfaucet.uo1.net  

If you have any issues using the faucet and need some funds for testnet, please reach out on the Discord. I have private funds available on request.

## Project Templates

In addition to the channel demo found in the `contrib` folder, you can try using the docker workbench templates below.

**Neutrino Workbench**  
A docker workbench environment, pre-configured for running LND in neutrino mode.  
https://github.com/cmdruid/neutrino-workbench

**Sauron Workbench**  
A docker workbench environment, pre-configured for running Core Lightning using Blockstream API.  
https://github.com/cmdruid/saurons-workbench

## More Resources

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
