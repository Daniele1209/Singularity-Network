# SingularityCoin
`Singularity Network` is my minimal implementation of a PoS based Blockchain, written in Python. This is my Bachelor Thesis project and it is available as an open source project on Github. It uses P2P communication in order to handle the decentralized aspect of the chain. The Lottery PoS system is done by using hash chaining and it has an API system for user communication - written using Flask

# Formatting
Use default `black` installation.

# Installing
Tools you need: [Poetry](https://python-poetry.org/), Python 3.9
After installing poetry run `poetry install`, and to install git hooks run command `pre-commit install`

# Running

## Generating Keys
Generate RSA Key pairs for genesis and set the path for them using the config keys `genesis_public_key_path` and `genesis_private_key_path`.
A node needs only the genesis public key. You use the private key to make a genesis transaction.

Wallet keys file name format is `{wallet_name}_PrivateKey.pem` and `{wallet_name}_PublicKey.pem` and reads from the folder specified by `wallet_keys_folder`.
By default, it generates new keys and writes them to those files. Wallets belonging to nodes have the `wallet_name` as `#` and it always generates new keys.
## Running a node
### Running a node from command line
Project Root Folder is `BlockChain`
First you have to start the origin node, and then other nodes. Otherwise, child nodes will not connect to the origin.

Run with command: `python3 -m BlockChain.Application <ipaddr> <port> <apiport> <origin_ipaddr> <origin_port> [publickeypath] [privatekeypath]`


### Running a node with docker
First you have to build the image yourself by using `docker build --tag <name>:<tag> .`.

By default, origin_ip is specified using an environment variable in the `Dockerfile`, and by default it connects to the localhost of the local machine.
This is specified using the name `host.docker.internal`. On linux when you use `docker run` you have to add the following option
`--add-host host.docker.internal:host-gateway`.  
The node ports and api ports by default are `10001` and `5000` respectively.
These options can be overridden in `settings.toml` or by specifying environment variables at build time or run time.
For more information check out https://www.dynaconf.com/envvars/.

You can run a node using `docker run -p host-port:5000 -p host-port:10001 -d <name>:<tag>`.  
You first have to start the origin node and then other subsequent nodes specifying other host ports that are not already bound.

## Running multiple nodes
### Running multiple nodes with docker-compose
Build docker image with `docker build --tag singularitycoin:latest .`
And then you can start the nodes with `docker compose up -d`. Only the origin node will be exposed on ports `10001` and `5000`.
The rest of the nodes are assigned random ports at the hosts, see the assigned ports using `docker ps`.
