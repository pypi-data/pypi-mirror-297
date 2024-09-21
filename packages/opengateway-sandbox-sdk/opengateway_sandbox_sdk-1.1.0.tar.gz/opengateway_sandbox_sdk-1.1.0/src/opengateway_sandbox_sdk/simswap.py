from datetime import datetime
from typing import Optional

from .clientcredentials import (
    httpclient,
    ClientCredentials,
)
from .purposes import SimswapPurpose
from .base import Base


class SimSwap(Base):
    path = "sim-swap/v0/"
    purpose = SimswapPurpose.FRAUD_PREVENTION_AND_DETECTION

    def check(self, max_age: int, phone_number: Optional[str] = None) -> bool:
        _, json = httpclient.post(
            endpoint=self.base_url + "check",
            token_str=self._get_token(),
            data={"phoneNumber": phone_number or self.phone_number, "maxAge": max_age},
        )

        return json["swapped"]

    def retrieve_date(self, phone_number: Optional[str] = None) -> datetime:
        _, json = httpclient.post(
            endpoint=self.base_url + "retrieve-date",
            token_str=self._get_token(),
            data={"phoneNumber": phone_number or self.phone_number},
        )

        return datetime.fromisoformat(json["latestSimChange"].partition("Z")[0])


# keep for backwards compatibility
class Simswap(SimSwap):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        phone_number: Optional[str] = None,
        code: Optional[str] = None,
        purpose: SimswapPurpose = SimswapPurpose.FRAUD_PREVENTION_AND_DETECTION,
    ):
        self.purpose = purpose
        credentials = ClientCredentials(client_id, client_secret)
        super().__init__(credentials=credentials, code=code, phone_number=phone_number)
