# SingularityCoin
This is the cryptocurrency I'm working on

# Formatting
Use default `black` installation.

# Running

## Generating Keys
Generate RSA Key pairs for genesis and set the path for them using the config keys `genesis_public_key_path` and `genesis_private_key_path`.
A node needs only the genesis public key. You use the private key to make a genesis transaction.

Wallet keys file name format is `{wallet_name}_PrivateKey.pem` and `{wallet_name}_PublicKey.pem` and reads from the folder specified by `wallet_keys_folder`.
By default, it generates new keys and writes them to those files. Wallets belonging to nodes have the `wallet_name` as `#` and it always generates new keys.

## Running a node
Project Root Folder is `BlockChain`
First you have to start the origin node, and then other nodes. Otherwise, child nodes will not connect to the origin.

Run with command: `python3 -m BlockChain.Application <ipaddr> <port> <apiport> <origin_ipaddr> <origin_port> [publickeypath] [privatekeypath]`