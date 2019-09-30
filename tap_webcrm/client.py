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
        self.__token = api_token

    def list_persons(self):
        yield from self.__paginate("/Persons")

    def list_opportunities(self):
        yield from self.__paginate("/Opportunities")

    def list_organisations(self):
        yield from self.__paginate("/Organisations")

    def __paginate(self, path, page_size=100, **kwargs):
        page, size = 1, page_size or 100
        while True:
            items = self.request("GET", path, params={"Page": page, "Size": size})

            if not items:
                break

            for item in items:
                yield item

            page += 1

    # TTL for the token is 3600 - set it to 3000 to make sure we don't end up
    # in a situation where it has run out by milliseconds
    @cached(cache=TTLCache(1, ttl=3000))
    def __get_token(self, api_token):
        # circumvent the normal self.request that expects a token
        resp = self.__request(
            "POST", "/Auth/ApiLogin", files={"authCode": (None, api_token)}
        )

        return resp["AccessToken"]

    def request(self, method, path, **kwargs):

        token = self.__get_token(self.__token)

        headers = kwargs.pop("headers", {})
        headers["Authorization"] = "Bearer " + token

        return self.__request(method, path, headers=headers, **kwargs)

    def __request(self, method, path, **kwargs):
        resp = self.__session.request(method, "https://api.webcrm.com" + path, **kwargs)
        if resp:
            return resp.json()

        resp.raise_for_status()

