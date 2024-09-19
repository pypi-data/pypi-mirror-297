from typing import List

from typing_extensions import Unpack

from billing.services._billing_api_service import BillingAPIService
from billing.types import OrderCreatePayload, OrderListParams, OrderWithPlans, OrderWithPlansAndInvoices


class OrderAPIService(BillingAPIService):
    def retrieve(self, object_id: str) -> OrderWithPlans:
        return self._request(
            "GET",
            f"/v1/orders/{object_id}/",
            data_model=OrderWithPlans,
        )

    async def retrieve_async(self, object_id: str) -> OrderWithPlans:
        return await self._request_async(
            "GET",
            f"/v1/orders/{object_id}/",
            data_model=OrderWithPlans,
        )

    def list(
        self,
        page_number: int = 1,
        page_size: int = 50,
        **params: Unpack[OrderListParams],
    ) -> List[OrderWithPlans]:
        return self._request(
            "GET",
            "/v1/orders/",
            params={
                "page": page_number,
                "page_size": page_size,
                **params,
            },
            data_model=OrderWithPlans,
            batch_mode=True,
        )

    async def list_async(
        self,
        page_number: int = 1,
        page_size: int = 50,
        **params: Unpack[OrderListParams],
    ) -> List[OrderWithPlans]:
        return await self._request_async(
            "GET",
            "/v1/orders/",
            params={
                "page": page_number,
                "page_size": page_size,
                **params,
            },
            data_model=OrderWithPlans,
            batch_mode=True,
        )

    def create(self, **payload: Unpack[OrderCreatePayload]) -> OrderWithPlansAndInvoices:
        return self._request(
            "POST",
            "/v1/orders/",
            json=payload,
            data_model=OrderWithPlansAndInvoices,
        )

    async def create_async(self, **payload: Unpack[OrderCreatePayload]) -> OrderWithPlansAndInvoices:
        return await self._request_async(
            "POST",
            "/v1/orders/",
            json=payload,
            data_model=OrderWithPlansAndInvoices,
        )
