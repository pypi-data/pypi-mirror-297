from typing import List

from billing.types._invoice import Invoice
from billing.types._offer import Offer
from billing.types._offer_product_plan import OfferProductPlan
from billing.types._order import Order
from billing.types._product import Product
from billing.types._product_plan import ProductPlan


class OfferProductPlanBundle(Offer):
    offer_product_plans: List[OfferProductPlan]


class OfferProductPlanInvoiceBundle(OfferProductPlanBundle):
    invoices: List[Invoice]


class OrderWithPlans(Order):
    offers: List[OfferProductPlanBundle]


class OrderWithPlansAndInvoices(Order):
    offers: List[OfferProductPlanInvoiceBundle]


class ProductProductPlanImageBundle(Product):
    product_plans: List[ProductPlan]
