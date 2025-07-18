from __future__ import annotations

from typing import List, Dict, Any, Optional

from scrap.jobs.statistic import get_attribute_value, find_element_value


def _extract_price(ad: Dict[str, Any]) -> Optional[float]:
    values = find_element_value(ad, "price")
    if not values:
        return None
    val = values[0] if isinstance(values, list) else values
    try:
        return float(str(val).replace(" ", "").replace(",", "."))
    except (ValueError, TypeError):
        return None


def _extract_city(ad: Dict[str, Any]) -> Optional[str]:
    values = find_element_value(ad, "city")
    if values:
        return str(values[0] if isinstance(values, list) else values)
    return None


def _extract_brand(ad: Dict[str, Any]) -> Optional[str]:
    values = get_attribute_value(ad, "brand")
    if values:
        return str(values[0] if isinstance(values, list) else values)
    return None


def filter_ads(
    data: List[Dict[str, Any]], *,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    city: Optional[str] = None,
    brand: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Filter ads with optional price, city and brand criteria."""
    result = []
    for ad in data:
        price = _extract_price(ad)
        if min_price is not None and (price is None or price < min_price):
            continue
        if max_price is not None and (price is None or price > max_price):
            continue

        ad_city = _extract_city(ad)
        if city is not None and (ad_city is None or ad_city.lower() != city.lower()):
            continue

        ad_brand = _extract_brand(ad)
        if brand is not None and (ad_brand is None or ad_brand.lower() != brand.lower()):
            continue

        result.append(ad)
    return result
