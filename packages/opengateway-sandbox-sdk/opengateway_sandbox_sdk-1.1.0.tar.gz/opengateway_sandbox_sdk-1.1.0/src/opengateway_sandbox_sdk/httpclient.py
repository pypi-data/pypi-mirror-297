import logging
from typing import Optional, cast

import requests
from requests.compat import urljoin
from requests.exceptions import JSONDecodeError

from .settings import AUTH_CODE_GRANT_TYPE, BASE_URL

logger = logging.getLogger(__name__)


def bc_authorize(
    client_id: str, client_secret: str, purpose: str, login_hint: str
) -> tuple[int, dict]:
    request_body = {"purpose": purpose, "login_hint": login_hint, "acr_values": 2}

    r = requests.post(
        urljoin(BASE_URL, "bc-authorize"),
        data=request_body,
        auth=(client_id, client_secret),
        timeout=5,
    )

    if not r.ok:
        logger.error("Error POST /bc-authorize: %s - %s", r.status_code, r.text)
        r.raise_for_status()

    return r.status_code, r.json()


def token(
    client_id: str,
    client_secret: str,
    grant_type: str,
    auth_req_id: Optional[str] = None,
    code: Optional[str] = None,
) -> tuple[int, dict]:
    if grant_type == AUTH_CODE_GRANT_TYPE:
        request_body = {
            "grant_type": grant_type,
            "code": code,
            "redirect_uri": "whatever",
        }
    else:
        request_body = {"grant_type": grant_type, "auth_req_id": auth_req_id}

    r = requests.post(
        urljoin(BASE_URL, "token"),
        data=request_body,
        auth=(client_id, client_secret),
        timeout=5,
    )

    if r.status_code == 415:
        r = requests.post(
            urljoin(BASE_URL, "token"),
            json=request_body,
            auth=(client_id, client_secret),
            timeout=5,
        )

    if not r.ok and not _is_auth_pending_error(r):
        logger.error("Error POST /token: %s - %s", r.status_code, r.text)
        r.raise_for_status()

    return r.status_code, r.json()


def post(endpoint: str, token_str: str, data: dict | None = None) -> tuple[int, dict]:
    headers = {"Authorization": token_str}
    data = data or {}

    r = requests.post(endpoint, json=data, headers=headers, timeout=5)

    if not r.ok:
        logger.error("Error POST %s: %s - %s", endpoint, r.status_code, r.text)
        r.raise_for_status()

    return r.status_code, r.json()


def put(endpoint: str, token_str: str, data: dict | None = None) -> tuple[int, dict]:
    headers = {"Authorization": token_str}
    data = data or {}

    r = requests.put(endpoint, json=data, headers=headers, timeout=5)

    if not r.ok:
        logger.error("Error PUT {endpoint}: %s - %s", r.status_code, r.text)
        r.raise_for_status()

    try:
        data = r.json()
    except JSONDecodeError:
        data = {}

    data = cast(dict, data)  # Help mypy typehints
    return r.status_code, data


def _is_auth_pending_error(response: requests.Response) -> bool:
    return (
        not response.ok
        and "error" in response.json()
        and response.json()["error"] == "authorization_pending"
    )
