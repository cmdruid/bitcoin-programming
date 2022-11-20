# bitcoin-programming

An educational repository on programming with the Bitcoin protocol. 

## Main Index

Below is an overview of the directories in this repository.

```sh
/assignments  # Here you will find a list of issued homework assignments, 
              # with examples on how to submit them.

/contrib      # A repository of code examples and demos that you can 
              # reference (and use!) when making your own projects.

/papers       # Contains a repository of notable papers to read,
              # in regards to Bitcoin.

/resources    # Contains a large repository of links that covers many 
              # different subject categories.

/slides       # Contains presentation slides for you to reference,
              # in both .ods and .pdf format.
```

# Class Assignments

Below is an overview of assignmets that are due by the end of the semester.

| Assignment                                                         | Example                                                 | Short description                                                                               |
| ------------------------------------------------------------------ | ------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| 01 - [Bitcoin Transaction](./01_Bitcoin_Transaction_Assignment.md) | [Link](examples/01-bitcoin-tx-assignment/README.md)     | Send a Bitcoin transaction to another address, using the Testnet blockchain.                    |
| 02 - [Bitcoin Script](./02_Bitcoin_Script_Assignment.md)           | [Link](examples/02-bitcoin-script-assignment/README.md) | Create a Bitcoin Script (using ScriptWiz) that evaluates to True.                               |
| 03 - [Lightning Payment](./03_Lightning_Payment_Assignment.md)     | [Link](examples/03-ln-payment-assignment/README.md)     | Open a Lightning Channel between two nodes, send a payment, then close the channel (on testnet) |
| 04 - [Final Hackathon Project](./04_Final_Hackathon_Project.md)    |                                                         | Create a project that uses Bitcoin and/or Lightning in some form (and have fun!)                |


## Resource Links

There is a large collection of links and resources available, organized by category. Feel free to navigate through them using the table below.

| Category                                              | Short description                                                                           |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| [Main (start here)](resources/main.md)                | Introduction to the Bitcoin protocol.                                                       |
| [Repositories](resources/repos.md)                    | Links to the repositories of important Bitcoin projects.                                    |
| [Runninng a Node](resources/run-a-node.md)            | Many useful links on how to run your own Bitcoin node.                                      |
| [Using the RPC Interface](resources/rpc-interface.md) | Info and guides on how to use Bitcoin's RPC interface.                                      |
| [Block Explorers](resources/block-explorers.md)       | List of explorers for viewing transaction history on the blockchain.                        |
| [Chain Statistics](resources/block-stats.md)          | Fun and interesting statistics regarding the blockchain.                                    |
| [External APIs](resources/external-apis.md)           | External APIs that you can use to interact with the blockchain.                             |
| [Cryptography Demos](resources/crypto-demos.md)       | Useful demos and examples of cryptography that Bitcoin uses.                                |
| [Programming Libraries](resources/libraries.md)       | Programming libraries that simplify programming on Bitcoin.                                 |
| [Books and Lectures](resources/books-and-vids.md)     | Important books and lectures that teach programming on Bitcoin.                             |
| [News & Discussion](resources/news-sources.md)        | Places to read and catch up on the latest news in Bitcoin development.                      |
| [Misc. Links](resources/other.md)                     | Repository for miscellaneous links regarding Bitcoin.                                       |

## Project Templates

There are a number of pre-configured docker environments available for you use in your projects. Please check them out below.

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

## Contributions

Feel free to contribute by sending a pull request!

## Questions / Issues

If you see any errors or other issues within this repository and would like to see a correction, please feel free to submit an issue or pull request. If you have any questions, or would otherwise like to get into contact with me, please feel free to submit an issue asking your question, or message me directly on github.
