# Final Assignment - Hackathon Project

The purpose of this assignment is to build something cool!

You may submit this project on your own, or as a team.

## Requirements

* A `README.md` which documents your project. This README should contain the following:

  - A summary introduction to your project.
  - Detailed instructions on how to setup your demo.
  - Detailed instructions on how to use your demo.
  - Reference links to any notable resources used to build your project.

* A `SLIDES.pdf` presentation (5-10 slides), in PDF format. Your presentation should cover:

  - What does your project do?  
  - What is the motivation for selecting your project?  
  - What problem are you trying to solve, if any?  
  - What ideas are you trying to explore?  
  - What is the biggest challenge you faced with your project?  

* The source code to your project! Please try to comment your code as much as possible.

## Project Ideas

Here are some project ideas that you can try to tackle. Your project can be simple or ambitious! As long as you deliver on the above criteria, and document your attempt to produce a minimum viable product (MVP).

 - A simple website that collects / monitors data from the blockchain and presents it in a useful or beautiful or useful way (like mempool.space).

 - A puzzle-based transaction that can be redeemed by solving the puzzle.

 - An API that offers useful webhooks / features for coordinating transactions.
   (such as coinjoins or multi-sig)

 - A website for publishing / tracking transactions that store data on the blockchain.
   (using OP_RETURN to publish data)

 - A web portal / API for making payments that use zero-knowledge proofs.
   https://en.bitcoin.it/wiki/Zero_Knowledge_Contingent_Payment

## FAQ

> What if I can't get my project demo working in time?

No problem! As long as you deliver commented code, along with a presentation and documentation, that will complete the assignment. Use your presentation to address the issues that you encountered when trying to complete the project.

> Help! I can't get an environment working!

We have put together some useful docker-based templates to get your project going! See the resource links below.

> I don't have any peers to connect with!

Not a problem! I have put together a cluster of bitcoin and lightning nodes for you to peer with during development. See the resource links below.

> I am stuck / having a hard time with something, can you help?

Yes! Please use the *Bitcoin Engineers* discord server to ask questions and schedule tutoring. Pleb Lab will be open during the week for co-working and tutoring, simply make a request in the discord server!

> When is our project due?

All homework, plus the final project is due by the final class at the end of the semester (December 12th). If you forsee any issues with meeting this deadline, please reach out to us on the discord server.

## Project Templates

**Satoshi Workbench**  
A docker workbench environment, pre-configured for running bitcoind.  
https://github.com/cmdruid/satoshi-workbench

**Neutrino Workbench**  
A docker workbench environment, pre-configured for running LND in neutrino mode.  
https://github.com/cmdruid/neutrino-workbench

**Sauron Workbench**  
A docker workbench environment, pre-configured for running Core Lightning using Blockstream API.  
https://github.com/cmdruid/saurons-workbench

**Regtest Workbench**  
Spin up a multi-node environent plus a full suite of development tools. Prototype and deploy your next project with lightning speed!  
https://github.com/cmdruid/regtest-workbench

## Demo Server

There is a public-facing server with Bitcoin and Lightning nodes available for you to peer with.

```sh
# Bitcoin Node
addnode http://158.69.210.216:18333 add

# Lightning Node
lncli connect 158.69.210.216:19735          # LND.
lightning-cli connect 158.69.210.216:19737  # Core Lightning.
```

## Hosting Bitcoin on a Server

If you would like to setup a light-weight Bitcoin Core node running on minimal hardware (like a cheap VPS), try using the following configuration:

```conf
## Main Config
server = 1

## Optimization
prune           = 2000  ## Prune the blockchain size to 2GB max.
blocksonly      = 1     ## Disables the mempool entirely.
dbcache         = 50    ## Limit the space used for the database cache.
maxorphantx     = 10    ## Limit the number of orphan transactions stored.
maxmempool      = 100   ## Limit the size of your local mempool.
maxsigcachesize = 4     ## Limit the space used for the signature cache.
maxconnections  = 32    ## Limit the number of connections to your node.

## Network Config
# banscore = 1
blockfilterindex = 1    ## Support light-clients that request block data.
peerblockfilters = 1    ## Support light-clients that request block data.

## ZMQ Config
zmqpubrawblock = tcp://0.0.0.0:28332
zmqpubrawtx    = tcp://0.0.0.0:28333
```

## Resources

**LND API Documentation**  
https://api.lightning.community

**Polar: One-click Lightning Network**  
https://github.com/jamaljsr/polar

**Bitcoin Testnet Faucet**  
https://bitcoinfaucet.uo1.net

**Mempool.space Testnet**  
https://mempool.space/testnet

## Question / Issues

If you have any questions, or run into any issues, please feel free to a question in **#homework-chat** on the [class Discord](https://discord.gg/kCvWQxXuwv)
