# gpsdclient

[![PyPI Version][pypi-version]][pypi-url]
[![PyPI License][pypi-license]][mit-license]
[![tests][test-badge]][test-url]

> A simple and lightweight [gpsd](https://gpsd.gitlab.io/gpsd) client and library

## Installation

Needs Python 3 (no other dependencies).
If you want to use the library, use pip:

```
pip3 install gpsdclient
```

If you want to use only the standalone gpsd viewer, I recommend to use pipx:

```
pipx install gpsdclient
```

## Library usage

```python
from gpsdclient import GPSDClient

client = GPSDClient(host="127.0.0.1")

# get your data as json strings:
for result in client.json_stream():
    print(result)

# or as python dicts (optionally convert time information to `datetime` objects)
for result in client.dict_stream(convert_datetime=True):
    if result["class"] == "TPV":
        print("Latitude: %s" % result.get("lat", "n/a"))
        print("Longitude: %s" % result.get("lon", "n/a"))

# you can optionally filter by report class
for result in client.dict_stream(filter=["TPV", "SKY"]):
    print(result)
```

You can find the documentation for the available data and JSON fields in the
[gpsd_json(5) manpage](https://www.mankier.com/5/gpsd_json).

## Command line usage

You can use the `gpsdclient` standalone program or execute the module with
`python3 -m gpsdclient`.

```
$ gpsdclient
Connected to gpsd v3.17
Devices: /dev/ttyO4

Mode | Time                 | Lat          | Lon          | Speed  | Track  | Alt       | Climb
-----+----------------------+--------------+--------------+--------+--------+-----------+-----------
1    | n/a                  | n/a          | n/a          | n/a    | n/a    | n/a       | n/a
1    | n/a                  | n/a          | n/a          | n/a    | n/a    | n/a       | n/a
1    | n/a                  | n/a          | n/a          | n/a    | n/a    | n/a       | n/a
3    | n/a                  | 51.813360383 | 6.550329033  | n/a    | n/a    | 46.518    | 0.0
3    | n/a                  | 51.813360383 | 6.550329033  | n/a    | n/a    | 46.518    | 0.0
3    | 2021-08-13 14:06:25  | 51.813360383 | 6.550329033  | 0.674  | 260.53 | 46.518    | 0.0
3    | 2021-08-13 14:06:27  | 51.81335905  | 6.550316283  | 0.54   | 245.71 | 46.002    | 0.0
3    | 2021-08-13 14:06:28  | 51.8133673   | 6.55033345   | 0.422  | 241.88 | 46.476    | 0.0
3    | 2021-08-13 14:06:29  | 51.813365833 | 6.5503352    | 0.34   | 246.35 | 46.868    | 0.0
3    | 2021-08-13 14:06:30  | 51.81336285  | 6.550339117  | 0.242  | 246.35 | 47.22     | 0.0
3    | 2021-08-13 14:06:31  | 51.8133614   | 6.550350367  | 0.273  | 246.35 | 46.846    | 0.0
3    | 2021-08-13 14:06:32  | 51.813359233 | 6.550353767  | 0.226  | 246.35 | 46.635    | 0.0
3    | 2021-08-13 14:06:33  | 51.8133574   | 6.550349817  | 0.221  | 246.35 | 46.52     | 0.0
3    | 2021-08-13 14:06:34  | 51.813356733 | 6.550345917  | 0.319  | 274.21 | 46.453    | 0.0
3    | 2021-08-13 14:06:35  | 51.813357917 | 6.5503521    | 0.149  | 274.21 | 46.529    | 0.0
^C
```

Or use the raw json mode:

```json
$ gpsdclient --json
{"class":"VERSION","release":"3.17","rev":"3.17","proto_major":3,"proto_minor":12}
{"class":"DEVICES","devices":[{"class":"DEVICE","path":"/dev/ttyO4","driver":"NMEA0183","activated":"2021-08-13T12:25:00.896Z","flags":1,"native":0,"bps":9600,"parity":"N","stopbits":1,"cycle":1.00}]}
{"class":"WATCH","enable":true,"json":true,"nmea":false,"raw":0,"scaled":false,"timing":false,"split24":false,"pps":false}
{"class":"SKY","device":"/dev/ttyO4","xdop":0.87,"ydop":1.86,"vdop":0.93,"tdop":2.26,"hdop":1.36,"gdop":3.96,"pdop":1.65,"satellites":[{"PRN":1,"el":84,"az":318,"ss":22,"used":true},{"PRN":22,"el":78,"az":234,"ss":16,"used":true},{"PRN":21,"el":72,"az":115,"ss":0,"used":false},{"PRN":3,"el":55,"az":239,"ss":19,"used":true},{"PRN":17,"el":34,"az":309,"ss":20,"used":true},{"PRN":32,"el":32,"az":53,"ss":32,"used":true},{"PRN":8,"el":21,"az":172,"ss":13,"used":false},{"PRN":14,"el":18,"az":274,"ss":13,"used":false},{"PRN":131,"el":10,"az":115,"ss":0,"used":false},{"PRN":19,"el":9,"az":321,"ss":33,"used":true},{"PRN":4,"el":4,"az":187,"ss":0,"used":false},{"PRN":31,"el":1,"az":106,"ss":0,"used":false},{"PRN":69,"el":80,"az":115,"ss":17,"used":true},{"PRN":84,"el":73,"az":123,"ss":0,"used":false},{"PRN":85,"el":42,"az":318,"ss":26,"used":true},{"PRN":68,"el":33,"az":39,"ss":0,"used":false},{"PRN":70,"el":27,"az":208,"ss":0,"used":false},{"PRN":76,"el":12,"az":330,"ss":19,"used":true},{"PRN":83,"el":12,"az":133,"ss":16,"used":false},{"PRN":77,"el":9,"az":18,"ss":0,"used":false}]}
{"class":"TPV","device":"/dev/ttyO4","mode":3,"time":"2021-08-13T12:25:01.000Z","ept":0.005,"lat":51.813525983,"lon":6.550081367,"alt":63.037,"epx":13.150,"epy":27.967,"epv":21.390,"track":211.3400,"speed":0.000,"climb":0.000,"eps":62.58,"epc":42.78}
^C
```

Or use gdop to output the geometric (hyperspherical) dilution of precision (pdop & tdop) and exit:

```gdop
$ gpsdclient --gdop
1.36
```

Or use nsat to output the number of satellites in the array and exit:

```nsat
$ gpsdclient --nsat
22
```

Or use pdop to output the Position (spherical/3D) dilution of precision and exit:

```pdop
$ gpsdclient --pdop
1.19
```

Or use sky to output a single SKY response (in json) and exit:

```sky
$ gpsdclient --sky
{"class":"SKY","device":"/dev/ttyAMA0","xdop":0.39,"ydop":0.57,"vdop":0.96,"tdop":0.61,"hdop":0.69,"gdop":1.33,"pdop":1.18,"nSat":21,"uSat":17,"satellites":[{"PRN":23,"el":66.0,"az":233.0,"ss":44.0,"used":true,"gnssid":0,"svid":23},{"PRN":18,"el":66.0,"az":11.0,"ss":44.0,"used":true,"gnssid":0,"svid":18},{"PRN":29,"el":49.0,"az":136.0,"ss":44.0,"used":true,"gnssid":0,"svid":29},{"PRN":48,"el":46.0,"az":184.0,"ss":43.0,"used":false,"gnssid":1,"svid":135},{"PRN":15,"el":44.0,"az":94.0,"ss":46.0,"used":true,"gnssid":0,"svid":15},{"PRN":10,"el":33.0,"az":228.0,"ss":41.0,"used":true,"gnssid":0,"svid":10},{"PRN":26,"el":30.0,"az":262.0,"ss":39.0,"used":true,"gnssid":0,"svid":26},{"PRN":16,"el":27.0,"az":298.0,"ss":39.0,"used":true,"gnssid":0,"svid":16},{"PRN":13,"el":22.0,"az":60.0,"ss":40.0,"used":true,"gnssid":0,"svid":13},{"PRN":5,"el":13.0,"az":47.0,"ss":38.0,"used":true,"gnssid":0,"svid":5},{"PRN":27,"el":9.0,"az":317.0,"ss":24.0,"used":true,"gnssid":0,"svid":27},{"PRN":25,"el":1.0,"az":180.0,"ss":0.0,"used":false,"gnssid":0,"svid":25},{"PRN":70,"el":63.0,"az":66.0,"ss":34.0,"used":true,"gnssid":6,"svid":6},{"PRN":85,"el":57.0,"az":55.0,"ss":42.0,"used":true,"gnssid":6,"svid":21},{"PRN":71,"el":48.0,"az":173.0,"ss":41.0,"used":true,"gnssid":6,"svid":7},{"PRN":86,"el":43.0,"az":333.0,"ss":32.0,"used":true,"gnssid":6,"svid":22},{"PRN":76,"el":14.0,"az":274.0,"ss":27.0,"used":true,"gnssid":6,"svid":12},{"PRN":84,"el":11.0,"az":105.0,"ss":15.0,"used":true,"gnssid":6,"svid":20},{"PRN":69,"el":9.0,"az":27.0,"ss":36.0,"used":true,"gnssid":6,"svid":5},{"PRN":77,"el":9.0,"az":321.0,"ss":0.0,"used":false,"gnssid":6,"svid":13},{"PRN":72,"el":4.0,"az":194.0,"ss":0.0,"used":false,"gnssid":6,"svid":8}]}
```

Or use tdop to output the time dilution of precision and exit:

```tdop
$ gpsdclient --tdop
0.75
```

Or use usat to print the number of satellites used in the navigation solution:

```usat
$ gpsdclient --usat
19
```

All command line options:

```
$ gpsdclient -h
usage: gpsdclient [-h] [--host HOST] [--port PORT] [--json | --gdop | --nsat | --pdop | --sky | --tdop | --usat]

Connect to a running gpsd instance and show human readable output.

optional arguments:
  -h, --help   show this help message and exit
  --host HOST  The host running GPSD (default: 127.0.0.1)
  --port PORT  GPSD port (default: 2947)
  --json       Output as JSON strings (default: False)
  --gdop       Output the geometric (hyperspherical) dilution of precision (pdop & tdop) and exit (default: False)
  --nsat       Output the number of satellites in the array and exit (default: False)
  --pdop       Output the Position (spherical/3D) dilution of precision and exit (default: False)
  --sky        Output a single SKY response (in json) and exit (default: False)
  --tdop       Output the time dilution of precision and exit (default: False)
  --usat       Output the number of satellites used in the navigation solution  and exit (default: False)
```

## Why

I made this because I just needed a simple client library to read the json data gpsd is
sending.
The other python libraries have various problems, like 100 % cpu usage, missing python 3
support, license problems, lots of dependencies or they aren't available on PyPI.
I also wanted a simple gpsd client to check if everything is working.

This client is as simple as possible with one exception: It supports the automatic
conversion of "time" data into `datetime.datetime` objects.

Have fun, hope you like it.

## License

[MIT][mit-license]

<!-- Badges -->

[pypi-version]: https://img.shields.io/pypi/v/gpsdclient
[pypi-license]: https://img.shields.io/pypi/l/gpsdclient
[pypi-url]: https://pypi.org/project/gpsdclient/
[mit-license]: https://choosealicense.com/licenses/mit/
[test-badge]: https://github.com/tfeldmann/gpsdclient/actions/workflows/tests.yml/badge.svg?branch=main
[test-url]: https://github.com/tfeldmann/gpsdclient/actions/workflows/tests.yml
