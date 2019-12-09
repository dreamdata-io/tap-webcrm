import os
import sys
import json

import singer
from singer import utils

from tap_webcrm.client import WebCRM
import tap_webcrm.stream as stream
from tap_webcrm.discover import discover, do_discover


logger = singer.get_logger()


def main():
    args = utils.parse_args([])

    API_TOKEN = args.config.get("api_token") or os.environ.get("WEBCRM_API_TOKEN")
    if not API_TOKEN:
        raise ValueError(
            "required 'api_token' or envrionment 'WEBCRM_API_TOKEN' not found"
        )

    webcrm_client = WebCRM(API_TOKEN)

    streams = args.config.get("streams")
    state = args.state

    if args.discover:
        do_discover()
        return

    catalog = args.catalog
    state = args.state
    start_date = args.config.get("start_date")

    if not catalog:
        catalog = discover()
        selected_streams = catalog.streams
    else:
        selected_streams = catalog.get_selected_streams(state)

    for selected_stream in selected_streams:
        stream.process_stream(webcrm_client, selected_stream, state, start_date)


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
