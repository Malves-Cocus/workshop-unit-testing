__all__ = [
    "CityBikes"
]

import typing
from datetime import timedelta
from json import loads

import requests


class CityBikes:
    BASE_URL = "http://api.citybik.es/"

    def networks(self):
        endpoint = "v2/networks?fields=id,location.country"
        try:
            response = requests.get(self.BASE_URL + endpoint)
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

    def network(self, by_id: typing.AnyStr):
        endpoint = "v2/networks/{network_id}"
        try:
            response = requests.get(self.BASE_URL + endpoint.format(network_id=by_id))
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
