from cosm_gov_watch.api_requests import request_governance
from config_loader.load_config import load_chains
from prettytable import PrettyTable
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os
import json
import requests
import ssl
import certifi
from colorama import Fore, Style
import time
import schedule

ssl_context = ssl.create_default_context(cafile=certifi.where())

def api():
    SLACK_CHANNEL=os.environ.get("SLACK_CHANNEL")
    client = WebClient(token=os.environ.get("SLACK_TOKEN"), ssl=ssl_context)
    chains = load_chains()
    for chain in chains["chains"]:
        print(f"info: extract proposals for chain: {chain}")
        governance = request_governance(chain["api"], chain["version"])
        if chain["version"] == "v1beta1":
            try:
                for proposal in governance['proposals']:
                    if proposal['status'] == "PROPOSAL_STATUS_VOTING_PERIOD":
                        client.chat_postMessage(channel="#" + SLACK_CHANNEL, text=chain["name"]+ "  " +\
                                                proposal['proposal_id']+ "  " +proposal['content']['@type'].rsplit('.', 1)[-1]+"  "+proposal['content']['title'][:60]+"  "+\
                                                proposal['status']+ "  " +chain["proposal_link"]+proposal['proposal_id'])
            except KeyError as e:
                client.chat_postMessage(channel="#" + SLACK_CHANNEL, text=f"""
==========
{chain["name"].upper()} API error - check api endpoint
==========""")

        else:
            try:
                for proposal in governance['proposals']:
                    if proposal['status'] == "PROPOSAL_STATUS_VOTING_PERIOD":
                        client.chat_postMessage(channel="#" + SLACK_CHANNEL, text=chain["name"] + "  " + \
                                                                                  proposal['id'] + "  " +
                                                                                  proposal['messages'][0]['@type'].rsplit('.', 1)[-1] + "  " +
                                                                                  proposal['title'] + "  " + \
                                                                                  proposal['status'] + "  " + chain["proposal_link"] + proposal['id'])
            except KeyError as e:
                client.chat_postMessage(channel="#" + SLACK_CHANNEL, text=f"""
==========
{chain["name"].upper()}  API error - check api endpoint
==========""")

time_period = int(os.environ.get("SLACK_PERIOD"))
schedule.every(time_period).minutes.do(api)

def main():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()
