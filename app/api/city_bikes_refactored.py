__all__ = [
    "CityBikes"
]

import functools
import typing
from datetime import timedelta
from json import loads

import requests
from requests import Response


def api(host: str, endpoint: str):
    def _wrapper(function):
        @functools.wraps(function)
        def _impl(self, *args, **kwargs):
            url = host + endpoint

            try:
                response: Response = function(self, url, *args, **kwargs)
                if response.ok:
                    return {
                        "data": loads(response.text),
                        "success": True,
                        "metadata": {
                            "endpoint": endpoint,
                            "elapsed_time": response.elapsed / timedelta(milliseconds=1),
                            "status_code": response.status_code
                        }
                    }

                error = response.text
            except Exception as e:
                error = F"{type(e).__name__}: {e}"

            return {
                "success": False,
                "metadata": {
                    "endpoint": endpoint,
                    "error": error
                }
            }

        return _impl

    return _wrapper


class CityBikes:
    BASE_URL = "http://api.citybik.es/"

    @api(host=BASE_URL, endpoint="v2/networks?fields=id,location.country")
    def networks(self, url: str):
        return requests.get(url)

    @api(host=BASE_URL, endpoint="v2/networks/{network_id}")
    def network(self, url: str, *, by_id: typing.AnyStr):
        return requests.get(url.format(network_id=by_id))
