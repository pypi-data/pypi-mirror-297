from .clientcredentials import ClientCredentials, httpclient
from .base import Base


class NumberVerification(Base):
    path = "number-verification/v0/"

    def __init__(self, credentials: ClientCredentials, code: str):
        super().__init__(credentials=credentials, code=code)

    def verify(self, phone_number: str) -> bool:
        _, json = httpclient.post(
            endpoint=self.base_url + "verify",
            token_str=self._get_token(),
            data={"phoneNumber": phone_number},
        )

        return json["devicePhoneNumberVerified"]
