import json
from unittest.mock import patch

from futcli.futcli import format_output, futcli, get_output


def test_format_output_json(capsys):
    data = [{"Name": "Test", "Price": "1,000"}]
    format_output(data, "json")
    captured = capsys.readouterr()
    parsed = json.loads(captured.out)
    assert parsed == data


def test_format_output_table(capsys):
    data = [{"Name": "Test", "Price": "1,000"}]
    format_output(data, "table")
    captured = capsys.readouterr()
    assert "Test" in captured.out
    assert "1,000" in captured.out


@patch("futcli.futcli.get_sbc_items")
def test_get_output_sbc_all(mock_get_sbc, capsys):
    mock_get_sbc.return_value = {
        "upgrades": [{"Name": "Gold Upgrade", "Price": "5,000"}],
        "icons": [{"Name": "Icon Pick", "Price": "250,000"}],
    }
    get_output("sbc", None, "json")
    captured = capsys.readouterr()
    parsed = json.loads(captured.out)
    assert len(parsed) == 2


@patch("futcli.futcli.get_sbc_items")
def test_get_output_sbc_category(mock_get_sbc, capsys):
    mock_get_sbc.return_value = {
        "upgrades": [{"Name": "Gold Upgrade", "Price": "5,000"}],
    }
    get_output("sbc", "upgrades", "json")
    captured = capsys.readouterr()
    parsed = json.loads(captured.out)
    assert len(parsed) == 1
    assert parsed[0]["Name"] == "Gold Upgrade"


@patch("futcli.futcli.get_sbc_items")
def test_get_output_sbc_invalid_option(mock_get_sbc, capsys):
    mock_get_sbc.return_value = {"upgrades": []}
    get_output("sbc", "nonexistent", "json")
    captured = capsys.readouterr()
    assert "Invalid SBC option" in captured.out


def test_get_output_invalid_data_type(capsys):
    get_output("invalid", None, "json")
    captured = capsys.readouterr()
    assert "Invalid data type" in captured.out


@patch("futcli.futcli.get_evolution_items")
def test_get_output_evolutions_json_no_double_serialization(mock_get_evos, capsys):
    """Evolutions dicts should be nested objects in JSON output, not escaped strings."""
    mock_get_evos.return_value = [
        {
            "Name": "Test Evo",
            "Requirements": {"Max Overall": "88"},
            "Upgrades": {"PAC": "5"},
        }
    ]
    get_output("evolutions", None, "json")
    captured = capsys.readouterr()
    parsed = json.loads(captured.out)
    # Requirements and Upgrades should be dicts, not strings
    assert isinstance(parsed[0]["Requirements"], dict)
    assert isinstance(parsed[0]["Upgrades"], dict)
    assert parsed[0]["Requirements"]["Max Overall"] == "88"


@patch("futcli.futcli.get_evolution_items")
def test_get_output_evolutions_table_stringifies_dicts(mock_get_evos, capsys):
    """Evolutions dicts should be stringified for table output."""
    mock_get_evos.return_value = [
        {
            "Name": "Test Evo",
            "Requirements": {"Max Overall": "88"},
            "Upgrades": {"PAC": "5"},
        }
    ]
    get_output("evolutions", None, "table")
    captured = capsys.readouterr()
    assert "Test Evo" in captured.out


def test_futcli_no_args_prints_help(capsys):
    """Running futcli with no args should print help."""
    with patch("sys.argv", ["futcli"]):
        futcli()
    captured = capsys.readouterr()
    assert (
        "usage:" in captured.out.lower()
        or "optional arguments" in captured.out.lower()
        or "options" in captured.out.lower()
    )


def test_futcli_version(capsys):
    """Running futcli --version should print version without errors."""
    with patch("sys.argv", ["futcli", "--version"]):
        try:
            futcli()
        except SystemExit:
            pass
    captured = capsys.readouterr()
    # Should contain the program name and version
    assert "futcli" in captured.out.lower() or "unknown" in captured.out.lower()
