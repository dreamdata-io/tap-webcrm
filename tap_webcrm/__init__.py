import os

from tap_webcrm.client import WebCRM

API_TOKEN = os.environ["WEBCRM_API_TOKEN"]

webcrm_client = WebCRM(API_TOKEN)


def main():
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
