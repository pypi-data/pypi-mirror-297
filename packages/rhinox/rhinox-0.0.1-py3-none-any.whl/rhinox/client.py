from rhinox.models.menu import Menu
from rhinox.urls import get_url_base
from rhinox.endpoints.menu import get_menu

class Rhinox:
    def __init__(self, *, tkn: str, is_production: bool = True, verify: bool = True):
        self._tkn: str = tkn
        self.is_production: bool = is_production
        self.url_base: str = get_url_base(is_production=is_production)
        self.verify: bool = verify

    @property
    def tkn(self) -> str:
        return self._tkn

    def get_menu(self, *, sucursal_id: str) -> Menu:
        r = get_menu(sucursal_id=sucursal_id, tkn=self.tkn, url_base=self.url_base, verify=self.verify)
        if r.status_code != 200:
            raise Exception("Controlar status_code!=200 para la obtención del menu.")
        return Menu(**r.json())
        