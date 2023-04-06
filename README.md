# Cosmos Governance Watcher
Script pulls list of active proposals from chains enumerated in configuration file.
Governance proposals information is pulled via API endpoint.
Once information is collected script send details about proposal to a SLACK CHANNEL

## Requirements
 - Python 3.8 or newer

## Installation

A) Locally

1. Clone repository and create a Python virtual environment
```bash
$ git clone https://github.com/ChainTools-Tech/cosm_gov_watch
$ cd cosm_gov_watch
$ python -m venv ./venv
$ source venv/bin/activate
(venv) $
```

2. Install the requirements
```bash
(venv) $ python -m pip install -r requirements.txt
```

3. Install script
```bash
(venv) $ pip install -e .
```

B) using Dockerfile
create a .env file for ENV variables
build image
run docker container

## Configuration
List of chains to check along with endpoints is located in ```config_loader/chains.toml``` file. 
Each chain is described as example below:
```toml
[[chains]]
name = "axelar-mainnet"
displayname = "Axelar-Mainnet"
chain-id = "axelar-dojo-1"
rpc = "https://axelar-rpc.polkachu.com"
api = "https://axelar-api.polkachu.com"
version = "v1beta1"
proposal_link = "https://www.mintscan.io/axelar/proposals/"
```

In order to add another chain create new section and populate with appropriate information.
If some chains are not needed just remove chain section from configuration file.

## ENV Variables
```
SLACK_CHANNEL=slack channel name
SLACK_TOKEN=slack channel token
SLACK_PERIOD=the proposals will be send at every x minutes
```

## Usage
```bash
(venv) $ cosm_gov_watch              
