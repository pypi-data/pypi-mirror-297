from libnftinema.common import get_client_key
from libnftinema.structs import ClientKey


def check_api_client_test(client_id: str) -> (bool, ClientKey | None):
    if client_id == "api_client_AoYznPzrHMMv4oR2vFjSQC":
        return True, get_client_key()
    return False, None
