import json

from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from cachetools import cached, TTLCache


class WebCRM:
    def __init__(self, api_token, **kwargs):
        self.__session = Session(**kwargs)
        self.__session.headers.update({"Accept": "application/json"})
        self.__session.mount(
            "https://",
            HTTPAdapter(
                max_retries=Retry(
                    total=5,
                    backoff_factor=5,
                    status_forcelist=[500, 502, 503, 504],
                    respect_retry_after_header=True,
                )
            ),
        )
        self.__api_token = api_token
        self.__token = None
        self.__refresh_token = None

    def list_persons(self):
        yield from self.__paginate("/Persons")

    def list_opportunities(self):
        yield from self.__paginate("/Opportunities")

    def list_organisations(self):
        yield from self.__paginate("/Organisations")

    def query_organisation(self, checkpoint=None):
        yield from self.__query(
            "organisation", "OrganisationUpdatedAt", checkpoint=checkpoint
        )

    def query_opportunity(self, checkpoint=None):
        yield from self.__query(
            "opportunity", "OpportunityUpdatedAt", checkpoint=checkpoint
        )

    def query_delivery(self, checkpoint=None):
        yield from self.__query("delivery", "DeliveryUpdatedAt", checkpoint=checkpoint)

    def query_person(self, checkpoint=None):
        yield from self.__query("person", "PersonUpdatedAt", checkpoint=checkpoint)

    def __query(self, table, updated_at_field, direction="ASC", checkpoint=None):
        if direction not in ["ASC", "DESC"]:
            raise ValueError("direction needs to be either 'ASC' or 'DESC'")
        script = f"SELECT * FROM {table} order by {updated_at_field} {direction}"
        # script = f"SELECT * FROM {table} t where t.PersonUpdatedAt > '2019-09-01T12:48:51' order by PersonUpdatedAt ASC"

        return self.__paginate("/Queries", params={"script": script})

    def __paginate(self, path, page_size=None, **kwargs):
        params = kwargs.pop("params", {})
        params["Page"] = 1
        params["Size"] = page_size or 500

        while True:
            items = self.request("GET", path, params=params, **kwargs)

            if not items:
                break

            for item in items:
                yield item

            params["Page"] += 1

    # TTL for the token is 3600 - set it to 3000 to make sure we don't end up
    # in a situation where it has run out by milliseconds
    @cached(cache=TTLCache(5, ttl=3000))
    def __get_token(self):
        if self.__refresh_token:
            resp = self.__request(
                "POST",
                "/Auth/ApiRefresh",
                files={"refreshToken": (None, self.__refresh_token)},
            )
        else:
            resp = self.__request(
                "POST", "/Auth/ApiLogin", files={"authCode": (None, self.__api_token)}
            )

        return resp["AccessToken"], resp["RefreshToken"]

    def request(self, method, path, **kwargs):

        self.__token, self.__refresh_token = self.__get_token()

        headers = kwargs.pop("headers", {})
        headers["Authorization"] = "Bearer " + self.__token

        return self.__request(method, path, headers=headers, **kwargs)

    def __request(self, method, path, **kwargs):
        resp = self.__session.request(method, "https://api.webcrm.com" + path, **kwargs)
        if resp:
            return resp.json()

        resp.raise_for_status()
