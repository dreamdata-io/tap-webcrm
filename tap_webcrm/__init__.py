import os
import sys
import json

import singer
from singer import utils

from tap_webcrm.client import WebCRM
from tap_webcrm.stream import discover, process_streams


logger = singer.get_logger()


def main():
    args = utils.parse_args([])

    API_TOKEN = args.config.get("api_token") or os.environ.get("WEBCRM_API_TOKEN")
    if not API_TOKEN:
        raise ValueError(
            "required 'api_token' or envrionment 'WEBCRM_API_TOKEN' not found"
        )

    webcrm_client = WebCRM(API_TOKEN)

    stream_names = args.config.get("streams")
    state = args.state

    if args.discover:
        streams = discover(stream_names)
        print(json.dumps(streams, sort_keys=True, indent="  "))
        return

    process_streams(webcrm_client, stream_names, state)


if __name__ == "__main__":
    API_TOKEN = os.environ["WEBCRM_API_TOKEN"]
    from client import WebCRM

    webcrm_client = WebCRM(API_TOKEN)
    for person in webcrm_client.query_organisation():
        print(person)
        break
    for item in webcrm_client.query_opportunity():
        print(item)
        break
    for item in webcrm_client.query_person():
        print(item)
        break
