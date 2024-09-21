import requests
from requests import Response

from rhinox.headers import get_header
from rhinox.urls import url_get_menu

def get_menu(*, sucursal_id: int, tkn: str, url_base: str, verify: bool) -> Response:
    url = url_get_menu(url_base=url_base, sucursal_id=sucursal_id)
    return requests.get(url, headers=get_header(tkn=tkn), verify=verify)
