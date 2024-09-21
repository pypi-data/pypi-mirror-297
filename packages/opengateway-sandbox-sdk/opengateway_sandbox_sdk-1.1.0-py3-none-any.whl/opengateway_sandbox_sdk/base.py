from typing import Optional

from .clientcredentials import (
    ClientCredentials,
    ClientSecretApikey,
    ClientSecretAuthCode,
)
from .settings import BASE_URL


class Base:
    purpose = None
    path = None

    def __init__(
        self,
        credentials: ClientCredentials,
        code: Optional[str] = None,
        phone_number: Optional[str] = None,
    ):
        self.code = code

        if self.code is None:
            self.phone_number = phone_number

            self.credentials = ClientSecretApikey(
                credentials.client_id,
                credentials.client_secret,
                login_hint=f"phone_number:{phone_number}",
                purpose=self.purpose,
            )
        else:
            self.credentials = ClientSecretAuthCode(
                credentials.client_id, credentials.client_secret
            )

        self.base_url = BASE_URL + self.path

    def _get_token(self) -> str:
        return (
            self.credentials.get_token(self.code)
            if self.code
            else self.credentials.get_token()
        )
