"""Thndr order-fee model (FR fees, Market rules & costs section)."""
from __future__ import annotations


def order_fees(value: float, fees: dict, same_session: bool = False, fills: int = 1) -> dict:
    """Fees for ONE order (a buy or a sell) of `value` EGP.

    `fills` = how many transactions the order executed in; the FRA fee is
    charged per transaction. Returns a breakdown plus `total`.
    """
    if value <= 0:
        return {"brokerage": 0.0, "egx": 0.0, "mcdr": 0.0, "fra": 0.0,
                "insurance": 0.0, "stamp": 0.0, "total": 0.0}
    brokerage = 0.0 if fees.get("commission_waived") else (
        fees["brokerage_fixed"] + fees["brokerage_pct"] * value)
    egx = min(fees["egx_pct"] * value, fees["egx_max"])
    mcdr = min(fees["mcdr_pct"] * value, fees["mcdr_max"])
    per_fill = value / max(fills, 1)
    fra = fills * min(max(fees["fra_pct"] * per_fill, fees["fra_min"]), fees["fra_max"])
    insurance = min(fees["insurance_pct"] * value, fees["insurance_max"])
    stamp = (fees["stamp_pct_t0"] if same_session else fees["stamp_pct"]) * value
    parts = {"brokerage": brokerage, "egx": egx, "mcdr": mcdr, "fra": fra,
             "insurance": insurance, "stamp": stamp}
    parts = {k: round(v, 4) for k, v in parts.items()}
    parts["total"] = round(sum(parts.values()), 4)
    return parts


def round_trip_cost(buy_value: float, sell_value: float, fees: dict,
                    same_session: bool = False) -> float:
    return (order_fees(buy_value, fees, same_session)["total"]
            + order_fees(sell_value, fees, same_session)["total"])


def round_trip_pct(value: float, fees: dict) -> float:
    """Approximate round-trip cost as a share of `value` (buy and sell at the same price)."""
    return round_trip_cost(value, value, fees) / value
