from datetime import datetime
from decimal import Decimal
from typing import Optional, TypedDict, Union

from billing.types._billing_entity import BillingEntity, BillingObject


class FeatureUsage(BillingObject):
    feature_id: str
    feature_codename: str
    period_start: Optional[datetime]
    max_usage_limit: Optional[Decimal]
    used_amount: Optional[Decimal]


class Feature(BillingEntity):
    feature_id: str
    customer_id: str
    amount: Decimal
    refunded_at: Optional[datetime]


class FeatureRecordPayload(TypedDict):
    customer_id: str
    amount: Union[Decimal, int]
