# kimuchi_match

A dependency-free Python prototype that matches kimchi makers and requesters by location.

## Command-line demo

Run the script with Python 3 and enter makers and requesters when prompted:

```bash
python3 match.py
```

Locations are compared case-insensitively after surrounding whitespace is removed.

## Local web interface

Start the local-only WSGI server, then open <http://127.0.0.1:5050/>:

```bash
python3 web_server.py
```

Data is held only in memory and is cleared whenever the server stops. The built-in server is intended for local evaluation, not an internet-facing production deployment.

## Tests

```bash
python3 -m unittest discover -s tests -v
```
