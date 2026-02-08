import argparse
import json

import pkg_resources
from tabulate import tabulate

from .evolutions import get_evolution_items
from .sbc import get_sbc_items

try:
    version = pkg_resources.require("futcli")[0].version
except pkg_resources.DistributionNotFound:
    version = "unknown"


def format_output(data, output_format):
    """Format the output to either json or table."""
    if output_format == "json":
        print(json.dumps(data, indent=4))
    else:
        print(tabulate(data, headers="keys", tablefmt="grid"))


def get_output(data_type, option, output_format):
    """Retrieve data based on the specified type and option."""
    if data_type == "sbc":
        sbc_data = get_sbc_items()
        if option is None:
            combined_data = [item for sublist in sbc_data.values() for item in sublist]
            format_output(combined_data, output_format)
        elif option in sbc_data:
            format_output(sbc_data[option], output_format)
        else:
            print("Invalid SBC option.")
    elif data_type == "evolutions":
        evolutions_data = get_evolution_items()
        formatted_evolutions = []
        for item in evolutions_data:
            formatted_item = {
                key: (json.dumps(value, indent=4) if isinstance(value, dict) else value)
                for key, value in item.items()
            }
            formatted_evolutions.append(formatted_item)
        format_output(formatted_evolutions, output_format)
    else:
        print("Invalid data type.")


def futcli():
    """Command-line interface for fetching FIFA Ultimate Team data."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-o",
        "--output",
        choices=["table", "json"],
        default="table",
        help="Choose the output format (table or json).",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s {version}".format(version=version),
    )

    subparsers = parser.add_subparsers(
        dest="data_type", title="args", metavar="[sbc.{options}, evolutions]"
    )
    sbc_categories = ["challenges", "foundations", "icons", "players", "swaps", "upgrades"]
    for sbc_type in sbc_categories:
        subparsers.add_parser(f"sbc.{sbc_type}", help=f"Outputs list of SBC {sbc_type}")
    subparsers.add_parser("sbc", help="Outputs list of all SBC types")
    subparsers.add_parser("evolutions", help="Outputs list of all active Evolutions")

    args = parser.parse_args()

    if args.data_type:
        if "." in args.data_type:
            data_type, option = args.data_type.split(".")
        else:
            data_type = args.data_type
            option = None

        get_output(data_type, option, args.output)


if __name__ == "__main__":
    futcli()
