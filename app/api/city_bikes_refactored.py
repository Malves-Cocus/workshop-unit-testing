__all__ = [
    "CityBikes"
]

import typing

import requests

from util import api


class CityBikes:
    BASE_URL = "http://api.citybik.es/"

    @api(host=BASE_URL, endpoint="v2/networks?fields=id,location.country")
    def networks(self, url: str):
        return requests.get(url=url)

    @api(host=BASE_URL, endpoint="v2/networks/{network_id}")
    def network(self, url: str, *, by_id: typing.AnyStr):
        return requests.get(url=url.format(network_id=by_id))
