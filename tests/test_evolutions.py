from unittest.mock import patch

from futcli.evolutions import (
    _extract_blocks,
    _extract_expiration,
    _extract_levels,
    _extract_name,
    _extract_players,
    _extract_price,
    _extract_requirements,
    _extract_upgrades,
    get_evolution_items,
)

# Realistic sample block mimicking SSR-dehydrated HTML
SAMPLE_BLOCK = (
    '{id:1,game:"26",eaId:100,url:"/evolutions/test-evo",'
    'name:"Test Evolution",'
    "coinsCost:25000,pointsCost:0,"
    "requirements:$R[5]={maxOverall:88,minOverall:75,maxPlaystyles:3,maxPlaystylesPlus:1},"
    "totalUpgradesText:$R[10]=["
    'label:"PAC",value:"3",maxValue:"5",'
    'label:"SHO",value:"2",maxValue:"4",'
    'label:"PAS",value:"1",maxValue:""'
    "],"
    'endTime:"2025-03-15T18:00:00Z",'
    'idx:0,game:"26",challenges:[],'
    'idx:1,game:"26",challenges:[],'
    "numberOfPlayers:500"
)


def test_extract_blocks_single():
    html = f"some prefix {SAMPLE_BLOCK} some suffix"
    blocks = _extract_blocks(html)
    assert len(blocks) == 1


def test_extract_blocks_multiple():
    block2 = '{id:2,game:"26",eaId:200,url:"/evolutions/other",name:"Other"}'
    html = f"prefix {SAMPLE_BLOCK} middle {block2} suffix"
    blocks = _extract_blocks(html)
    assert len(blocks) == 2


def test_extract_blocks_empty():
    blocks = _extract_blocks("no evolution data here")
    assert blocks == []


def test_extract_name():
    assert _extract_name(SAMPLE_BLOCK) == "Test Evolution"


def test_extract_name_missing():
    assert _extract_name("no name here") == "Unknown"


def test_extract_price_coins_only():
    assert _extract_price(SAMPLE_BLOCK) == "25,000 Coins"


def test_extract_price_free():
    block = "coinsCost:0,pointsCost:0"
    assert _extract_price(block) == "FREE"


def test_extract_price_points_only():
    block = "coinsCost:0,pointsCost:100"
    assert _extract_price(block) == "100 Points"


def test_extract_price_both():
    block = "coinsCost:10000,pointsCost:200"
    assert _extract_price(block) == "10,000 Coins / 200 Points"


def test_extract_requirements():
    reqs = _extract_requirements(SAMPLE_BLOCK)
    assert reqs.get("Max Overall") == "88"
    assert reqs.get("Min Overall") == "75"
    assert reqs.get("Max Playstyles") == "3"
    assert reqs.get("Max Playstyles+") == "1"


def test_extract_requirements_missing():
    reqs = _extract_requirements("no requirements here")
    assert reqs == {}


def test_extract_upgrades():
    upgrades = _extract_upgrades(SAMPLE_BLOCK)
    assert upgrades.get("PAC") == "5"
    assert upgrades.get("SHO") == "4"
    # PAS has empty maxValue, should use value
    assert upgrades.get("PAS") == "1"


def test_extract_upgrades_missing():
    upgrades = _extract_upgrades("no upgrades here")
    assert upgrades == {}


def test_extract_expiration():
    result = _extract_expiration(SAMPLE_BLOCK)
    assert result == "2025-03-15 18:00:00"


def test_extract_expiration_missing():
    assert _extract_expiration("no end time") == "-"


def test_extract_levels():
    assert _extract_levels(SAMPLE_BLOCK) == "2"


def test_extract_levels_missing():
    assert _extract_levels("no levels") == "0"


def test_extract_players():
    assert _extract_players(SAMPLE_BLOCK) == "500"


def test_extract_players_missing():
    assert _extract_players("no players") == "0"


@patch("futcli.evolutions.get_html")
def test_get_evolution_items(mock_get_html):
    mock_get_html.return_value = f"prefix {SAMPLE_BLOCK} suffix"

    result = get_evolution_items()

    assert len(result) == 1
    item = result[0]
    assert item["Name"] == "Test Evolution"
    assert item["Price"] == "25,000 Coins"
    assert item["Levels"] == "2"
    assert item["Players"] == "500"
    assert isinstance(item["Requirements"], dict)
    assert isinstance(item["Upgrades"], dict)


@patch("futcli.evolutions.get_html")
def test_get_evolution_items_empty(mock_get_html, capsys):
    mock_get_html.return_value = None

    result = get_evolution_items()

    assert result == []
    captured = capsys.readouterr()
    assert "Error" in captured.out
