from datetime import datetime
from decimal import Decimal
from typing import Literal, Optional, TypedDict

from typing_extensions import NotRequired

from billing.types._billing_entity import BillingEntityWithTimestamps
from billing.types._offer_product_plan import OfferProductPlanWithProduct


class Invoice(BillingEntityWithTimestamps):
    amount: Decimal
    currency: str
    issued_at: Optional[datetime]
    expired_at: datetime
    paid_at: Optional[datetime]
    refunded_at: Optional[datetime]
    payment_method: Literal["stripe", "telegram_stars"]
    receipt_url: str
    failed_reason: str
    checkout_session_url: Optional[str]


class InvoiceWithProduct(Invoice):
    offer_product_plan: OfferProductPlanWithProduct


class InvoiceListParams(TypedDict):
    order_id: NotRequired[str]
    customer_auth_service_id: NotRequired[str]
