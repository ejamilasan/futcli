# FC Ultimate Team CLI (futcli)

The `futcli` is a Python-based tool designed to provide users with quick access to FC Ulimate Team (FUT) contents such as SBCs and Evolutions.

![pre-commit](https://github.com/ejamilasan/futcli/actions/workflows/pre-commit.yml/badge.svg)
![pypi version](https://badge.fury.io/py/futcli.svg)

## Features
* **Query SBC Content**: Retrieve SBC items: including name, price, expiration, challenges, and repeatable status.
    ![sbc-players-output.png](./docs/sbc-players-output.png)
* **Query Evolutions Content**: Retrieve Evolutions items including name, price, requirements, upgrades, expiration, levels, and the number of players involved.
    ![evolutions-output.png](./docs/evolutions-output.png)
* **JSON or Table Formats**: Display data in either JSON or table formats for easy readability and/or consumability.
    ```bash
    ➜  ~ futcli -o json sbc.challenges
    [
        {
            "Name": "Daily Fantasy FC Challenge",
            "New": "no",
            "Price": "",
            "Expiration": "12 days",
            "Challenges": "1",
            "Repeatable": "1",
            "Refreshes": "24 hours"
        },
        {
            "Name": "Marquee Matchups",
            "New": "no",
            "Price": "",
            "Expiration": "4 days",
            "Challenges": "4",
            "Repeatable": "-",
            "Refreshes": "-"
        },
        {
            "Name": "UEFA Marquee Matchups",
            "New": "no",
            "Price": "",
            "Expiration": "1 day",
            "Challenges": "2",
            "Repeatable": "-",
            "Refreshes": "-"
        }
    ]
    ```

## Installation
To install `futcli`, simply use pip:
```bash
pip install futcli
```

## Usage
For more information about available options and usage, you can use the `-h` or `--help`:
```bash
➜  ~ futcli -h
usage: futcli [-h] [-o {table,json}] [--version] [sbc.{options}, evolutions] ...

options:
  -h, --help            show this help message and exit
  -o {table,json}, --output {table,json}
                        Choose the output format (table or json).
  --version             show program's version number and exit

args:
  [sbc.{options}, evolutions]
    sbc.challenges      Outputs list of SBC challenges
    sbc.foundations     Outputs list of SBC foundations
    sbc.icons           Outputs list of SBC icons
    sbc.players         Outputs list of SBC players
    sbc.swaps           Outputs list of SBC swaps
    sbc.upgrades        Outputs list of SBC upgrades
    sbc                 Outputs list of all SBC types
    evolutions          Outputs list of all active Evolutions
```

## Dependencies
`futcli` relies on the following Python packages:
* **requests**: For making HTTP requests and fetching data from https://www.fut.gg
* **tabulate**: For formatting data into visually appealing tables in the terminal.

## Contributing
Contributions to `futcli` are welcome! If you encounter any bugs, issues, or have suggestions for improvements, please feel free to open an [issue](https://github.com/ejamilasan/futcli/issues) or submit a [pull request](https://github.com/ejamilasan/futcli/pulls).

## License
`futcli` is licensed under the GNU General Public License v3.0.
