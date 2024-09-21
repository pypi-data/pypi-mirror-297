# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["EvaluationDatasetVersionCreateParams"]


class EvaluationDatasetVersionCreateParams(TypedDict, total=False):
    account_id: str
    """The ID of the account that owns the given entity."""
