from typing import List

from typing_extensions import Unpack

from billing.services._billing_api_service import BillingAPIService
from billing.types import Feature, FeatureRecordPayload, FeatureUsage


class FeatureAPIService(BillingAPIService):
    def retrieve(
        self,
        codename: str,
        customer_id: str,
    ) -> FeatureUsage:
        return self._request(
            "GET",
            f"/v1/features/{codename}/",
            params={"customer_id": customer_id},
            data_model=FeatureUsage,
        )

    async def retrieve_async(
        self,
        codename: str,
        customer_id: str,
    ) -> FeatureUsage:
        return await self._request_async(
            "GET",
            f"/v1/features/{codename}/",
            params={"customer_id": customer_id},
            data_model=FeatureUsage,
        )

    def list(
        self,
        customer_id: str,
        page_number: int = 1,
        page_size: int = 50,
    ) -> List[FeatureUsage]:
        return self._request(
            "GET",
            "/v1/features/",
            params={
                "page": page_number,
                "page_size": page_size,
                "customer_id": customer_id,
            },
            data_model=FeatureUsage,
            batch_mode=True,
        )

    async def list_async(
        self,
        customer_id: str,
        page_number: int = 1,
        page_size: int = 50,
    ) -> List[FeatureUsage]:
        return await self._request_async(
            "GET",
            "/v1/features/",
            params={
                "page": page_number,
                "page_size": page_size,
                "customer_id": customer_id,
            },
            data_model=FeatureUsage,
            batch_mode=True,
        )

    def record(
        self,
        codename: str,
        **payload: Unpack[FeatureRecordPayload],
    ) -> Feature:
        return self._request(
            "POST",
            f"/v1/features/{codename}/",
            json=payload,
            data_model=Feature,
        )

    async def record_async(
        self,
        codename: str,
        **payload: Unpack[FeatureRecordPayload],
    ) -> Feature:
        return await self._request_async(
            "POST",
            f"/v1/features/{codename}/",
            json=payload,
            data_model=Feature,
        )
