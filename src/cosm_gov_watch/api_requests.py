import json
import requests


def request_governance(api_url, version):
    if version == "v1beta1":
        request_url = f"{api_url}/cosmos/gov/v1beta1/proposals?pagination.reverse=true"
    else:
        request_url = f"{api_url}/cosmos/gov/v1/proposals?pagination.reverse=true"
    try:
        api_response = requests.get(request_url)
        json_response = json.loads(api_response.text)
    except (requests.exceptions.ConnectionError,
            requests.exceptions.ConnectTimeout,
            json.decoder.JSONDecodeError):
        api_response = {}
        api_response['error'] = 'API connection failure'
        json_response = api_response

    return json_response
