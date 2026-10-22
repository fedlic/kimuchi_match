"""Dependency-free local web UI for kimchi maker/requester matching."""

from html import escape
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server

from match import KimchiMaker, KimchiRequester, match_makers_to_requesters

MAX_BODY_BYTES = 4096
MAX_FIELD_LENGTH = 100
makers = []
requesters = []


def page(title, content):
    return f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>{escape(title)}</title></head>
<body><main><h1>Kimchi Match Service</h1>{content}</main></body>
</html>"""


def homepage(error=""):
    notice = f'<p role="alert">{escape(error)}</p>' if error else ""
    return page(
        "Kimchi Match Service",
        f"""{notice}
<h2>Add maker</h2>
<form method="post" action="/">
  <input type="hidden" name="role" value="maker">
  <label>Name <input name="name" maxlength="{MAX_FIELD_LENGTH}" required></label><br>
  <label>Location <input name="location" maxlength="{MAX_FIELD_LENGTH}" required></label><br>
  <button type="submit">Add maker</button>
</form>
<h2>Add requester</h2>
<form method="post" action="/">
  <input type="hidden" name="role" value="requester">
  <label>Name <input name="name" maxlength="{MAX_FIELD_LENGTH}" required></label><br>
  <label>Location <input name="location" maxlength="{MAX_FIELD_LENGTH}" required></label><br>
  <button type="submit">Add requester</button>
</form>
<p><a href="/matches">View matches</a></p>""",
    )


def matches_page():
    matches = match_makers_to_requesters(makers, requesters)
    if matches:
        items = "".join(
            f"<li>{escape(maker.name)} can make kimchi for {escape(requester.name)} "
            f"in {escape(maker.location)}</li>"
            for maker, requester in matches
        )
        content = f"<h2>Matches</h2><ul>{items}</ul>"
    else:
        content = "<h2>Matches</h2><p>No matches found.</p>"
    return page("Matches · Kimchi Match Service", f'{content}<p><a href="/">Back</a></p>')


def send(start_response, status, body, extra_headers=(), head_only=False):
    encoded = body.encode("utf-8")
    headers = [
        ("Content-Type", "text/html; charset=utf-8"),
        ("Content-Length", str(len(encoded))),
        ("Cache-Control", "no-store"),
        ("Content-Security-Policy", "default-src 'none'; form-action 'self'; base-uri 'none'"),
        ("Referrer-Policy", "no-referrer"),
        ("X-Content-Type-Options", "nosniff"),
    ]
    headers.extend(extra_headers)
    start_response(status, headers)
    return [b"" if head_only else encoded]


def application(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    method = environ.get("REQUEST_METHOD", "GET").upper()
    head_only = method == "HEAD"

    if method in {"GET", "HEAD"}:
        if path == "/":
            return send(start_response, "200 OK", homepage(), head_only=head_only)
        if path == "/matches":
            return send(start_response, "200 OK", matches_page(), head_only=head_only)
        return send(start_response, "404 Not Found", page("Not found", "<p>Page not found.</p>"), head_only=head_only)

    if method != "POST" or path != "/":
        return send(
            start_response,
            "405 Method Not Allowed",
            page("Method not allowed", "<p>Method not allowed.</p>"),
            (("Allow", "GET, HEAD, POST"),),
        )

    try:
        size = int(environ.get("CONTENT_LENGTH") or 0)
    except ValueError:
        size = -1
    if size < 0 or size > MAX_BODY_BYTES:
        return send(start_response, "413 Payload Too Large", homepage("Invalid request size."))

    fields = parse_qs(environ["wsgi.input"].read(size).decode("utf-8"), keep_blank_values=True)
    role = fields.get("role", [""])[0]
    name = fields.get("name", [""])[0].strip()
    location = fields.get("location", [""])[0].strip()

    if role not in {"maker", "requester"} or not name or not location:
        return send(start_response, "400 Bad Request", homepage("Role, name, and location are required."))
    if len(name) > MAX_FIELD_LENGTH or len(location) > MAX_FIELD_LENGTH:
        return send(start_response, "400 Bad Request", homepage("Name and location must be 100 characters or fewer."))

    person_type = KimchiMaker if role == "maker" else KimchiRequester
    target = makers if role == "maker" else requesters
    target.append(person_type(name, location))
    return send(start_response, "303 See Other", "", (("Location", "/"),))


if __name__ == "__main__":
    with make_server("127.0.0.1", 5050, application) as httpd:
        print("Serving on http://127.0.0.1:5050")
        httpd.serve_forever()
