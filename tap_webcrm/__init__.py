import os

import singer
from singer import utils

from tap_webcrm.client import WebCRM


logger = singer.get_logger()


def main():
    args = utils.parse_args(["config"])

    API_TOKEN = args.config.get("api_token") or os.environ.get("WEBCRM_API_TOKEN")
    if not API_TOKEN:
        raise ValueError(
            "required 'api_token' or envrionment 'WEBCRM_API_TOKEN' not found"
        )

    webcrm_client = WebCRM(API_TOKEN)

    webcrm_client = WebCRM(API_TOKEN)

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
