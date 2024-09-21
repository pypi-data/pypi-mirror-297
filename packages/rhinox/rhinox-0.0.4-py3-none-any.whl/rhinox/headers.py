def get_header(*, tkn: str) -> dict:
    return {"Authorization": tkn, "Content-Type": "application/json"}
