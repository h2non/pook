import json as _json

from .regex import isregex
from .headers import HTTPHeaderDict
from .helpers import trigger_methods
from .matchers.url import protoregex

from urllib.parse import urlparse, parse_qs, urlunparse


class Request(object):
    """
    Request object representing the request mock expectation DSL.

    Arguments:
        method (str): HTTP method to match. Defaults to ``GET``.
        url (str): URL request to intercept and match.
        headers (dict): HTTP headers to match.
        query (dict): URL query params to match. Complementely to URL
            defined query params.
        body (str|regex): request body payload to match.
        json (str|dict|list): JSON payload body structure to match.
        xml (str): XML payload data structure to match.

    Attributes:
        method (str): HTTP method to match. Defaults to ``GET``.
        url (str): URL request to intercept and match.
        headers (dict): HTTP headers to match.
        query (dict): URL query params to match. Complementely to URL
            defined query params.
        body (str|regex): request body payload to match.
        json (str|dict|list): JSON payload body structure to match.
        xml (str): XML payload data structure to match.
    """

    # Store keys
    keys = ("method", "headers", "body", "url", "query")

    def __init__(self, method="GET", **kw):
        self._url = None
        self._body = None
        self._query = None
        self._method = method
        self._extra = kw.get("extra")
        self._headers = HTTPHeaderDict()

        trigger_methods(self, kw)

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, method):
        self._method = method

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, headers):
        if not hasattr(headers, "__setitem__"):
            raise TypeError("headers must be a dictionary")
        self._headers.extend(headers)

    @property
    def extra(self):
        return self._extra

    @extra.setter
    def extra(self, extra):
        if not isinstance(extra, dict):
            raise TypeError("extra must be a dictionary")
        self._extra = extra

    @property
    def url(self):
        return self._url

    @property
    def rawurl(self):
        return self._url if isregex(self._url) else urlunparse(self._url)

    @url.setter
    def url(self, url):
        if isregex(url):
            self._url = url
        else:
            if not protoregex.match(url):
                url = "http://{}".format(url)
            self._url = urlparse(url)
            self._query = parse_qs(self._url.query) if self._url.query else self._query

    @property
    def query(self, url):
        return self._query

    @query.setter
    def query(self, params):
        self._query = parse_qs(params)

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, body):
        if hasattr(body, "decode"):
            try:
                body = body.decode("utf-8", "strict")
            except Exception:
                pass

        self._body = body

    @property
    def json(self):
        return _json.loads(self._body)

    @json.setter
    def json(self, data):
        if isinstance(data, str):
            self._body = data
        else:
            self._body = _json.dumps(data)

    @property
    def xml(self):
        return self._body

    @xml.setter
    def xml(self, data):
        self._body = data

    def copy(self):
        """
        Copies the current Request object instance for side-effects purposes.

        Returns:
            pook.Request: copy of the current Request instance.
        """
        req = type(self)()
        req.__dict__ = self.__dict__.copy()
        req._headers = self.headers.copy()
        return req

    def __repr__(self):
        """
        Returns an human friendly readable instance data representation.

        Returns:
            str
        """
        entries = []

        entries.append("Method: {}".format(self._method))
        entries.append(
            "URL: {}".format(self._url if isregex(self._url) else self.rawurl)
        )

        if self._query:
            entries.append("Query: {}".format(self._query))

        if self._headers:
            entries.append("Headers: {}".format(self._headers))

        if self._body:
            entries.append("Body: {}".format(self._body))

        separator = "=" * 50
        return (separator + "\n{}\n" + separator).format("\n".join(entries))
