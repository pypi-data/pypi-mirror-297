# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["KYCMediaUpdateParams"]


class KYCMediaUpdateParams(TypedDict, total=False):
    bank_id: Required[Annotated[str, PropertyInfo(alias="BANK_ID")]]

    customer_id: Required[Annotated[str, PropertyInfo(alias="CUSTOMER_ID")]]

    body: Required[object]
