# kimuchi_match

This repository contains a simple Python script that demonstrates a basic matching service for people who make kimchi and those who would like to request it.

The script defines two simple classes (`KimchiMaker` and `KimchiRequester`) and matches them based on shared locations.

## Usage

Run the script with Python 3. You will be asked for the number of makers and requesters and their names and locations.

```bash
python3 match.py
```

After entering the information, the program shows matches between makers and requesters in the same city.

## Web server

Run `web_server.py` to start a simple web interface on port 5050. Open a browser to `http://localhost:5050/` to add makers and requesters and see matches.

```bash
python3 web_server.py
```
