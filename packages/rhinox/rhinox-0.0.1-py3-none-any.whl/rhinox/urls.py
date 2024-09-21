
def get_url_base(*, is_production: bool) -> str:
    if is_production:
        return "https://api.rhinox.io"
    return "https://api-dev.rhinox.io"

def url_get_menu(*, url_base: str, sucursal_id: str):
    return f"{url_base}/ecommerce/getRestauranteSucursalMenu/{sucursal_id}"
