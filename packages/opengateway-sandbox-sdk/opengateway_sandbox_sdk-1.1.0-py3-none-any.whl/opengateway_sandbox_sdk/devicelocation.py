from typing import Optional

from .base import Base
from .clientcredentials import (
    httpclient,
)
from .purposes import DeviceLocationPurpose


class DeviceLocation(Base):
    path = "location/v0/"
    purpose = DeviceLocationPurpose.FRAUD_PREVENTION_AND_DETECTION

    def verify(
        self,
        latitude: int,
        longitude: int,
        accuracy: int,
        phone_number: Optional[str] = None,
    ) -> bool:
        _, json = httpclient.post(
            endpoint=self.base_url + "verify",
            token_str=self._get_token(),
            data={
                "ueId": {"msisdn": phone_number or self.phone_number},
                "latitude": latitude,
                "longitude": longitude,
                "accuracy": accuracy,
            },
        )

        return json["verificationResult"]
