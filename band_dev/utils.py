import random
import base32_crockford as base64


def make_readable_id(id: int) -> str:
    return base64.encode(id, checksum=True).lower()


def decode_readable_id(readable_id: str) -> tuple[bool, int | None]:
    try:
        decoded_id = base64.decode(readable_id.upper(), checksum=True)
        return True, decoded_id
    except (base64.DecodeError, ValueError):
        return False, None


def flatten_querydict(querydict) -> dict:
    return {k: querydict.get(k) for k in querydict}
