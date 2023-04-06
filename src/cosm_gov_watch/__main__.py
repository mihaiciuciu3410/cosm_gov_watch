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

proposals_table = PrettyTable()
proposals_table.title = f"Chain Proposals"
proposals_table.field_names = ["Chain", "ID", "Type", "Title", "Status"]
proposals_table.align = "l"
proposals_table.border = True


def api():
    SLACK_CHANNEL=os.environ.get("SLACK_CHANNEL")
    client = WebClient(token=os.environ.get("SLACK_TOKEN"), ssl=ssl_context)
    chains = load_chains()
    for chain in chains["chains"]:
        governance = request_governance(chain["api"], chain["version"])
        if chain["version"] == "v1beta1":
            try:
                for proposal in governance['proposals']:
                    if proposal['status'] == "PROPOSAL_STATUS_VOTING_PERIOD":
                        proposals_table.add_row([chain["name"],
                                                 proposal['proposal_id'],
                                                 proposal['content']['@type'].rsplit('.', 1)[-1],
                                                 proposal['content']['title'][:60],
                                                 proposal['status']])
                        client.chat_postMessage(channel="#" + SLACK_CHANNEL, text=chain["name"]+ "  " +\
                                                proposal['proposal_id']+ "  " +proposal['content']['@type'].rsplit('.', 1)[-1]+"  "+proposal['content']['title'][:60]+"  "+\
                                                proposal['status']+ "  " +chain["proposal_link"]+proposal['proposal_id'])
            except KeyError as e:
                check_endpoints = True
                proposals_table.add_row([chain["name"],
                                         "API error",
                                         "API error",
                                         "API error",
                                         "API error"])
                client.chat_postMessage(channel="#" + SLACK_CHANNEL, text=f"""
==========
{chain["name"].upper()} API error - check api endpoint
==========""")

        else:
            try:
                for proposal in governance['proposals']:
                    if proposal['status'] == "PROPOSAL_STATUS_VOTING_PERIOD":
                        proposals_table.add_row([chain["name"],
                                                 proposal['id'],
                                                 proposal['messages'][0]['content']['@type'].rsplit('.', 1)[-1],
                                                 proposal['messages'][0]['content']['title'][:60],
                                                 proposal['status']])

            except KeyError as e:
                check_endpoints = True
                proposals_table.add_row([chain["name"],
                                         "API error",
                                         "API error",
                                         "API error",
                                         "API error"])
                client.chat_postMessage(channel="#" + SLACK_CHANNEL, text=f"""
==========
{chain["name"].upper()}  API error - check api endpoint
==========""")


schedule.every(5).minutes.do(api)

def main():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()
