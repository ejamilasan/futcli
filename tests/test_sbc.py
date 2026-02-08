from unittest.mock import patch

from futcli.sbc import get_sbc_items, get_sbc_types

SAMPLE_SBC_ITEM = {
    "name": "Gold Upgrade",
    "category": {"slug": "upgrades"},
    "cost": 5000,
    "isNew": True,
    "expiresIn": "2 days",
    "challengesCount": 1,
    "repeatabilityMode": "unlimited",
    "repeatRefreshIntervalText": "24h",
}

SAMPLE_SBC_ITEM_2 = {
    "name": "Icon Pick",
    "category": {"slug": "icons"},
    "cost": 250000,
    "isNew": False,
    "expiresIn": "5 days",
    "challengesCount": 3,
    "repeatabilityMode": "no",
    "repeatRefreshIntervalText": None,
}

SINGLE_PAGE_RESPONSE = {
    "data": [SAMPLE_SBC_ITEM, SAMPLE_SBC_ITEM_2],
    "next": None,
}

MULTI_PAGE_RESPONSE_1 = {
    "data": [SAMPLE_SBC_ITEM],
    "next": 2,
}

MULTI_PAGE_RESPONSE_2 = {
    "data": [SAMPLE_SBC_ITEM_2],
    "next": None,
}


def _reset_cache():
    """Reset the module-level cache between tests."""
    import futcli.sbc as sbc_mod

    sbc_mod._cached_items = None


@patch("futcli.sbc.get_json")
def test_get_sbc_items_single_page(mock_get_json):
    _reset_cache()
    mock_get_json.return_value = SINGLE_PAGE_RESPONSE

    result = get_sbc_items()

    assert "upgrades" in result
    assert "icons" in result
    assert len(result["upgrades"]) == 1
    assert result["upgrades"][0]["Name"] == "Gold Upgrade"
    assert result["upgrades"][0]["New"] == "yes"
    assert result["upgrades"][0]["Price"] == "5,000"
    assert result["upgrades"][0]["Repeatable"] == "unlimited"
    assert result["upgrades"][0]["Refreshes"] == "24h"

    assert result["icons"][0]["Name"] == "Icon Pick"
    assert result["icons"][0]["New"] == "no"
    assert result["icons"][0]["Price"] == "250,000"
    assert result["icons"][0]["Repeatable"] == "no"
    assert result["icons"][0]["Refreshes"] == "-"


@patch("futcli.sbc.get_json")
def test_get_sbc_items_pagination(mock_get_json):
    _reset_cache()
    mock_get_json.side_effect = [MULTI_PAGE_RESPONSE_1, MULTI_PAGE_RESPONSE_2]

    result = get_sbc_items()

    assert "upgrades" in result
    assert "icons" in result
    assert mock_get_json.call_count == 2


@patch("futcli.sbc.get_json")
def test_get_sbc_items_empty(mock_get_json, capsys):
    _reset_cache()
    mock_get_json.return_value = None

    result = get_sbc_items()

    assert result == {}
    captured = capsys.readouterr()
    assert "Error" in captured.out


@patch("futcli.sbc.get_json")
def test_get_sbc_types(mock_get_json):
    _reset_cache()
    mock_get_json.return_value = SINGLE_PAGE_RESPONSE

    result = get_sbc_types()

    assert result == ["icons", "upgrades"]


@patch("futcli.sbc.get_json")
def test_sbc_item_zero_cost(mock_get_json):
    _reset_cache()
    item = {**SAMPLE_SBC_ITEM, "cost": 0}
    mock_get_json.return_value = {"data": [item], "next": None}

    result = get_sbc_items()

    assert result["upgrades"][0]["Price"] == "0"


@patch("futcli.sbc.get_json")
def test_sbc_caching(mock_get_json):
    _reset_cache()
    mock_get_json.return_value = SINGLE_PAGE_RESPONSE

    get_sbc_items()
    get_sbc_items()

    # Should only call get_json once due to caching
    assert mock_get_json.call_count == 1
