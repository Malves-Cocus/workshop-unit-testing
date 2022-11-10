__all__ = [
    "api"
]

import functools
from datetime import timedelta
from json import loads

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
