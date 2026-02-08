from .urls import get_json

API_URL = "https://www.fut.gg/api/fut/sbc/"

_cached_items = None


def _fetch_all_sbc_items():
    """Paginate through all SBC API pages and return all items."""
    global _cached_items
    if _cached_items is not None:
        return _cached_items

    all_items = []
    page = 1
    while True:
        data = get_json(f"{API_URL}?page={page}")
        if data is None:
            break
        all_items.extend(data.get("data", []))
        if data.get("next") is None:
            break
        page = data["next"]

    _cached_items = all_items
    return _cached_items


def get_sbc_types():
    """Derive SBC category slugs from API data."""
    items = _fetch_all_sbc_items()
    return sorted({item["category"]["slug"] for item in items})


def get_sbc_items():
    """Group SBC items by category with formatted fields."""
    items = _fetch_all_sbc_items()
    sbc_data = {}

    for item in items:
        category = item["category"]["slug"]
        cost = item.get("cost", 0)
        repeatable = item.get("repeatabilityMode", "no")
        refresh_text = item.get("repeatRefreshIntervalText") or "-"

        sbc_data.setdefault(category, []).append({
            "Name": item["name"],
            "New": "yes" if item.get("isNew") else "no",
            "Price": f"{cost:,}" if cost else "0",
            "Expiration": item.get("expiresIn", "-"),
            "Challenges": str(item.get("challengesCount", 0)),
            "Repeatable": repeatable,
            "Refreshes": refresh_text,
        })

    return sbc_data
