from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from ..enums import RevenueWithdrawalStateType
from .revenue_withdrawal_state import RevenueWithdrawalState


class RevenueWithdrawalStateFailed(RevenueWithdrawalState):
    """
    The withdrawal failed and the transaction was refunded.

    Source: https://core.telegram.org/bots/api#revenuewithdrawalstatefailed
    """

    type: Literal[RevenueWithdrawalStateType.FAILED] = RevenueWithdrawalStateType.FAILED
    """Type of the state, always 'failed'"""

    if TYPE_CHECKING:
        # DO NOT EDIT MANUALLY!!!
        # This section was auto-generated via `butcher`

        def __init__(
            __pydantic__self__,
            *,
            type: Literal[RevenueWithdrawalStateType.FAILED] = RevenueWithdrawalStateType.FAILED,
            **__pydantic_kwargs: Any,
        ) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via `butcher`
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(type=type, **__pydantic_kwargs)
