"""Simple web server for kimchi maker/requester matching."""

from wsgiref.simple_server import make_server
import urllib.parse

class KimchiMaker:
    def __init__(self, name, location):
        self.name = name
        self.location = location

class KimchiRequester:
    def __init__(self, name, location):
        self.name = name
        self.location = location

makers = []
requesters = []


def match_makers_to_requesters(makers_list, requesters_list):
    matches = []
    for maker in makers_list:
        for requester in requesters_list:
            if maker.location == requester.location:
                matches.append((maker, requester))
    return matches


def generate_homepage():
    return """
    <html><body>
    <h1>Kimchi Match Service</h1>
    <h2>Add Maker</h2>
    <form method='post'>
      <input type='hidden' name='role' value='maker'>
      Name: <input name='name'><br>
      Location: <input name='location'><br>
      <input type='submit' value='Add Maker'>
    </form>

    <h2>Add Requester</h2>
    <form method='post'>
      <input type='hidden' name='role' value='requester'>
      Name: <input name='name'><br>
      Location: <input name='location'><br>
      <input type='submit' value='Add Requester'>
    </form>

    <p><a href='/matches'>View Matches</a></p>
    </body></html>
    """


def application(environ, start_response):
    path = environ.get('PATH_INFO', '/')
    if path == '/matches':
        body = "<html><body><h1>Matches</h1>"
        for maker, requester in match_makers_to_requesters(makers, requesters):
            body += f"<p>{maker.name} can make kimchi for {requester.name} in {maker.location}</p>"
        body += "<p><a href='/'>Back</a></p></body></html>"
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
        return [body.encode('utf-8')]

    if environ['REQUEST_METHOD'] == 'POST':
        size = int(environ.get('CONTENT_LENGTH', 0))
        data = environ['wsgi.input'].read(size).decode()
        fields = urllib.parse.parse_qs(data)
        role = fields.get('role', [''])[0]
        name = fields.get('name', [''])[0]
        location = fields.get('location', [''])[0]
        if role == 'maker':
            makers.append(KimchiMaker(name, location))
        elif role == 'requester':
            requesters.append(KimchiRequester(name, location))

    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    return [generate_homepage().encode('utf-8')]


if __name__ == '__main__':
    with make_server('localhost', 5050, application) as httpd:
        print('Serving on port 5050...')
        httpd.serve_forever()
