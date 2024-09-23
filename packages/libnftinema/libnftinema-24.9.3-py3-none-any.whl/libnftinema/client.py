import uuid

import arrow
import loguru
import sentry_sdk
from django.test import Client as DjangoTestClient
from requests import Request
from requests import Session

from .common import HEADER_REQ_SIGNATURE_TOKEN
from .common import sign_request
from .structs import ClientKey


class APIClient:
    base_url: str
    user_jwt: str
    user_uuid: str
    client_key: ClientKey
    is_test: bool
    jti: str
    iat: int
    exp: int

    def __init__(
        self,
        base_url: str,
        client_key: ClientKey,
        user_jwt: str = None,
        user_uuid: str = None,
        jti: str = None,
        iat: int = None,
        exp: int = None,
        is_test: bool = False,
    ):
        self.base_url = base_url
        self.user_jwt = user_jwt
        self.user_uuid = user_uuid
        self.client_key = client_key
        self.is_test = is_test
        if self.is_test:
            self.django_client = DjangoTestClient()
        self.jti = str(uuid.uuid4()) if not jti else jti
        self.iat = arrow.utcnow().int_timestamp if not iat else iat
        self.exp = arrow.utcnow().shift(minutes=5).int_timestamp if not exp else exp

    def _prepare_signed_request(self, method, endpoint, headers=None, **kwargs):
        url = f"{self.base_url}{endpoint}"
        request = Request(method, url, headers=headers, **kwargs)
        prepared_request = request.prepare()
        signature_jwt = sign_request(
            prepared_request,
            client_key=self.client_key,
            user_jwt=self.user_jwt,
            user_uuid=self.user_uuid,
            jti=self.jti,
            iat=self.iat,
            exp=self.exp,
        )
        print(f"Generated signature_jwt: {signature_jwt}")  # Debugging line
        prepared_request.headers[HEADER_REQ_SIGNATURE_TOKEN] = signature_jwt
        print(
            f"Headers after adding signature: {prepared_request.headers}",
        )  # Debugging line
        return prepared_request

    def _send_signed_request(self, method, endpoint, headers=None, **kwargs):
        prepared_request = self._prepare_signed_request(
            method,
            endpoint,
            headers,
            **kwargs,
        )
        if self.is_test:
            client_method = getattr(self.django_client, method.lower())
            return client_method(
                prepared_request.path_url,
                prepared_request.body,
                content_type="application/json",
                headers=dict(prepared_request.headers),
            )

        with Session() as session:
            return session.send(prepared_request)

    def _send_unsigned_request(self, method, endpoint, headers=None, **kwargs):
        url = f"{self.base_url}{endpoint}"
        request = Request(method, url, headers=headers, **kwargs)
        prepared_request = request.prepare()

        if self.is_test:
            client_method = getattr(self.django_client, method.lower())
            return client_method(
                prepared_request.path_url,
                prepared_request.body,
                content_type="application/json",
                headers=dict(prepared_request.headers),
            )

        with Session() as session:
            return session.send(prepared_request)

    def request(self, method, endpoint, data=None, params=None, headers=None):
        return self._send_signed_request(
            method,
            endpoint,
            headers=headers,
            json=data,
            params=params,
        )

    def post(self, endpoint, data=None, headers=None):
        return self._send_unsigned_request("POST", endpoint, headers=headers, json=data)

    def put(self, endpoint, data=None, headers=None):
        return self._send_unsigned_request("PUT", endpoint, headers=headers, json=data)

    def patch(self, endpoint, data=None, headers=None):
        return self._send_unsigned_request(
            "PATCH",
            endpoint,
            headers=headers,
            json=data,
        )

    def get(self, endpoint, params=None, headers=None):
        return self._send_unsigned_request(
            "GET",
            endpoint,
            headers=headers,
            params=params,
        )

    def head(self, endpoint, headers=None):
        return self._send_unsigned_request("HEAD", endpoint, headers=headers)

    def spost(self, endpoint, data, headers=None):
        return self.request("POST", endpoint, data=data, headers=headers)

    def sput(self, endpoint, data, headers=None):
        return self.request("PUT", endpoint, data=data, headers=headers)

    def spatch(self, endpoint, data, headers=None):
        return self.request("PATCH", endpoint, data=data, headers=headers)

    def sget(self, endpoint, params=None, headers=None):
        return self.request("GET", endpoint, params=params, headers=headers)

    def shead(self, endpoint, headers=None):
        return self.request("HEAD", endpoint, headers=headers)


class NftinemaClient(APIClient):
    def check_mints(self, batch_id: str) -> list[dict]:
        response = self.get(f"/api/mint/status/{batch_id}")
        assert response.status_code == 200, response.content
        return response.json()

    def issue(
        self,
        collection_wid: str,
        exact_token_id: str,
        amount: int,
        batch_id: str,
    ) -> dict:
        assert self.user_uuid
        response = self.spost(
            "/api/issue",
            dict(
                user_uuid=self.user_uuid,
                collection_wid=collection_wid,
                exact_token_id=exact_token_id,
                amount=amount,
                batch_id=batch_id,
            ),
        )
        assert response.status_code == 200, response.content
        return response.json()

    def get_nfts(self) -> tuple[list[dict], int]:
        assert self.user_uuid
        assert self.client_key.kid
        url = f"/api/portfolio/{self.client_key.kid}/{self.user_uuid}"
        try:
            loguru.logger.debug(f"nft_client.get_nfts url: {url}")
            r = self.get(url)
            loguru.logger.debug(f"nft_client.get_nfts status_code: {r.status_code}")
            assert r.status_code == 200, r.content
            j = r.json()
            nfts = j["nfts"]
            nfts_count = j["nfts_count"]
            loguru.logger.debug(f"nft_client.get_nfts nfts_count: {nfts_count}")
        except Exception as e:
            loguru.logger.warning(f"nft_client.get_nfts error: {e}")
            sentry_sdk.capture_exception(e)
            nfts = []
            nfts_count = 0

        return nfts, nfts_count
