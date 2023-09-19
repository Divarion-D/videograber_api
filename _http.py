"""configured session object with ddos protect detector"""
import warnings

from requests import Session, Response

DDOS_SERVICES = ("cloudflare", "ddos-guard")

# default user-agent for all project
USER_AGENT = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, " \
             "like Gecko) Chrome/94.0.4606.114 Mobile Safari/537.36 "

BASE_HEADERS_DICT = {"user-agent": USER_AGENT,
                     "x-requested-with": "XMLHttpRequest"}


__all__ = ('client', 'SessionM')


class SessionM(Session):
    # add custom timeout param https://github.com/psf/requests/issues/3070
    # https://stackoverflow.com/a/62044757
    def __init__(self, timeout=60):
        self.timeout = timeout
        super().__init__()

    def request(self, method, url, **kwargs):
        if "timeout" not in kwargs:
            kwargs["timeout"] = self.timeout
        return super().request(method, url, **kwargs)


def check_ddos_protect_hook(resp: Response, **kwargs):
    if resp.headers.get("Server") in DDOS_SERVICES \
            and resp.headers["Connection"] == 'close' \
            or resp.status_code == 403:

        warnings.warn(f"{resp.url} have ddos protect and return 403 code.",
                      category=RuntimeWarning,
                      stacklevel=2)


client = SessionM()
client.headers.update(BASE_HEADERS_DICT)
client.hooks["response"] = [check_ddos_protect_hook]