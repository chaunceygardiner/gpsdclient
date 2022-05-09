"""
Connect to a running gpsd instance and show human readable output.
"""

from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from collections import namedtuple

from . import GPSDClient

import json
import sys

Column = namedtuple("Column", "key width formatter")

TPV_COLUMNS = (
    Column("mode", width=4, formatter=str),
    Column(
        "time",
        width=20,
        formatter=lambda x: x.isoformat(sep=" ", timespec="seconds"),
    ),
    Column("lat", width=12, formatter=str),
    Column("lon", width=12, formatter=str),
    Column("track", width=6, formatter=str),
    Column("speed", width=6, formatter=str),
    Column("alt", width=9, formatter=str),
    Column("climb", width=9, formatter=str),
)
NA = "n/a"


def print_version(data):
    print("Connected to gpsd v%s" % data.get("release", NA))


def print_devices(data):
    output = ", ".join(x.get("path", NA) for x in data["devices"])
    print("Devices: %s" % output)


def print_tpv_header():
    titles = (col.key.title().ljust(col.width) for col in TPV_COLUMNS)
    lines = ("-" * col.width for col in TPV_COLUMNS)
    print()
    print(" | ".join(titles))
    print("-+-".join(lines))


def print_tpv_row(data):
    values = []
    for key, width, formatter in TPV_COLUMNS:
        value = formatter(data[key]) if key in data else NA
        values.append(value.ljust(width))
    print(" | ".join(values))


def stream_readable(client):
    needs_tpv_header = True
    for x in client.dict_stream(convert_datetime=True):
        if x["class"] == "VERSION":
            print_version(x)
            needs_tpv_header = True
        elif x["class"] == "DEVICES":
            print_devices(x)
            needs_tpv_header = True
        elif x["class"] == "TPV":
            if needs_tpv_header:
                print_tpv_header()
                needs_tpv_header = False
            print_tpv_row(x)


def stream_json(client):
    for x in client.json_stream():
        print(x)


def check_sky_fields(fields):
    valid_fields = { "class", "device", "gdop", "hdop", "nSat", "pdop", "satellites", "tdop", "uSat", "vdop", "xdop", "ydop" }
    for field in fields:
        if field not in valid_fields:
            print('field: %s is not part of the SKY response.' % field)
            sys.exit(1)


def print_sky(client, fields):
    fields = fields.split(',')
    check_sky_fields(fields)
    for x in client.json_stream(filter=["SKY"]):
        j = json.loads(x)
        first = True
        for field in fields:
            if not first:
                print(' ', end='')
            try:
                print(j[field], end='')
            except KeyError as e:
                # Earlier versions of GPSD don't include nSat and uSat.  Compute them.
                if field == 'nSat':
                    print(len(j['satellites']), end='')
                elif field == 'uSat':
                    uSat = 0
                    for sat in j['satellites']:
                        if sat['used']:
                            uSat += 1
                    print(uSat, end='')
                else:
                    raise e
            first = False
        print()
        sys.exit(0)


def main():
    parser = ArgumentParser(
        formatter_class=ArgumentDefaultsHelpFormatter,
        description=__doc__,
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="The host running GPSD",
    )
    parser.add_argument(
        "--port",
        default="2947",
        help="GPSD port",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON strings",
    )
    parser.add_argument(
        "--sky",
        action="store",
        type=str,
        default=None,
        help="Output the values of the specified fields of a single SKY response and exit (e.g., --sky=nSat,uSat).",
    )
    args = parser.parse_args()

    try:
        client = GPSDClient(host=args.host, port=args.port)
        if args.json:
            stream_json(client)
        elif args.sky is not None:
            print_sky(client, args.sky)
        else:
            stream_readable(client)
    except (ConnectionError, EnvironmentError) as e:
        print(e)
    except KeyboardInterrupt:
        print()
        return 0
