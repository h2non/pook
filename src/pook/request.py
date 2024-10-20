import json as _json
from urllib.parse import parse_qs, urlparse, urlunparse

from .headers import HTTPHeaderDict
from .helpers import trigger_methods
from .matchers.url import protoregex
from .regex import isregex


class Request:
    """
    Request object representing the request mock expectation DSL.

    Arguments:
        method (str): HTTP method to match. Defaults to ``GET``.
        url (str): URL request to intercept and match.
        headers (dict): HTTP headers to match.
        query (dict): URL query params to match. Complementely to URL
            defined query params.
        body (bytes|regex): request body payload to match.
        json (str|dict|list): JSON payload body structure to match.
        xml (str): XML payload data structure to match.
    """

    # Store keys
    keys = ("method", "headers", "body", "url", "query", "xml", "json")
    """
    :meta private:
    """

    def __init__(self, method="GET", **kw):
        self._url = None
        self._body = None
        self._query = None
        self._method = method
        self._extra = kw.get("extra")
        self._headers = HTTPHeaderDict()

        trigger_methods(self, kw, self.keys)

    @property
    def method(self):
        """HTTP method to match. Defaults to ``GET``."""
        return self._method

    @method.setter
    def method(self, method):
        self._method = method

    @property
    def headers(self):
        """HTTP headers to match."""
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
        """URL request to intercept and match."""
        return self._url

    @url.setter
    def url(self, url):
        if isregex(url):
            self._url = url
        else:
            if not protoregex.match(url):
                url = f"http://{url}"
            self._url = urlparse(url)
            # keep_blank_values necessary for `param_exists` when a parameter has no value but is present
            self._query = (
                parse_qs(self._url.query, keep_blank_values=True)
                if self._url.query
                else self._query
            )

    @property
    def rawurl(self):
        return self._url if isregex(self._url) else urlunparse(self._url)

    @property
    def query(self):
        """URL query params to match. Complementary to URL defined query params."""
        return self._query

    @query.setter
    def query(self, params):
        self._query = parse_qs(params)

    @property
    def body(self):
        """request body payload to match."""
        return self._body

    @body.setter
    def body(self, body):
        if hasattr(body, "encode"):
            body = body.encode("utf-8", "backslashreplace")

        self._body = body

    @property
    def json(self):
        """JSON payload body structure to match."""
        return _json.loads(self.body.decode("utf-8"))

    @json.setter
    def json(self, data):
        if isinstance(data, str):
            self.body = data
        else:
            self.body = _json.dumps(data)

    @property
    def xml(self):
        """XML payload data structure to match."""
        return self.body.decode("utf-8")

    @xml.setter
    def xml(self, data):
        self.body = data

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

        entries.append(f"Method: {self._method}")
        entries.append(f"URL: {self._url if isregex(self._url) else self.rawurl}")

        if self._query:
            entries.append(f"Query: {self._query}")

        if self._headers:
            entries.append(f"Headers: {self._headers}")

        if self._body:
            entries.append(f"Body: {self._body}")

        separator = "=" * 50
        return (separator + "\n{}\n" + separator).format("\n".join(entries))
