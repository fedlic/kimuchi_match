import io
import unittest
from urllib.parse import urlencode

import web_server
from match import KimchiMaker, KimchiRequester, match_makers_to_requesters


class MatchingTests(unittest.TestCase):
    def test_location_matching_is_trimmed_and_case_insensitive(self):
        maker = KimchiMaker("Maker", " Tokyo ")
        requester = KimchiRequester("Requester", "tokyo")
        self.assertEqual(match_makers_to_requesters([maker], [requester]), [(maker, requester)])


class WebTests(unittest.TestCase):
    def setUp(self):
        web_server.makers.clear()
        web_server.requesters.clear()

    def request(self, path="/", method="GET", fields=None):
        raw = urlencode(fields or {}).encode()
        environ = {
            "PATH_INFO": path,
            "REQUEST_METHOD": method,
            "CONTENT_LENGTH": str(len(raw)),
            "wsgi.input": io.BytesIO(raw),
        }
        captured = {}

        def start_response(status, headers):
            captured["status"] = status
            captured["headers"] = dict(headers)

        captured["body"] = b"".join(web_server.application(environ, start_response)).decode()
        return captured

    def test_post_redirects_and_creates_person(self):
        response = self.request(method="POST", fields={"role": "maker", "name": "A", "location": "Osaka"})
        self.assertEqual(response["status"], "303 See Other")
        self.assertEqual(response["headers"]["Location"], "/")
        self.assertEqual(web_server.makers, [KimchiMaker("A", "Osaka")])

    def test_invalid_post_is_rejected(self):
        response = self.request(method="POST", fields={"role": "maker", "name": "", "location": "Osaka"})
        self.assertEqual(response["status"], "400 Bad Request")

    def test_match_output_is_html_escaped(self):
        web_server.makers.append(KimchiMaker("<script>alert(1)</script>", "Tokyo"))
        web_server.requesters.append(KimchiRequester("Reader", "Tokyo"))
        response = self.request(path="/matches")
        self.assertNotIn("<script>", response["body"])
        self.assertIn("&lt;script&gt;", response["body"])
        self.assertIn("Content-Security-Policy", response["headers"])

    def test_unknown_path_returns_404(self):
        self.assertEqual(self.request(path="/missing")["status"], "404 Not Found")


if __name__ == "__main__":
    unittest.main()
