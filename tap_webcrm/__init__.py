import os
import sys
import json

import singer
from singer import utils

from tap_webcrm.client import WebCRM
from tap_webcrm.stream import discover


logger = singer.get_logger()

implemented_streams = {"opportunity, organisation", "person"}


def main():
    args = utils.parse_args(["config"])

    API_TOKEN = args.config.get("api_token") or os.environ.get("WEBCRM_API_TOKEN")
    if not API_TOKEN:
        raise ValueError(
            "required 'api_token' or envrionment 'WEBCRM_API_TOKEN' not found"
        )

    webcrm_client = WebCRM(API_TOKEN)

    stream_names = args.config.get("streams", list(implemented_streams))
    for stream_name in stream_names:
        if stream_name not in implemented_streams:
            raise ValueError(f"config.streams contains unknown stream: {stream_name}")

    if args.discover:
        streams = discover(stream_names)
        print(json.dumps(streams, sort_keys=True, indent="  "))
        return

    for person in webcrm_client.list_persons():
        print(person)
        break
    for opportunity in webcrm_client.list_opportunities():
        print(opportunity)
        break
    for org in webcrm_client.list_organisations():
        print(org)
        break


if __name__ == "__main__":
    main()
