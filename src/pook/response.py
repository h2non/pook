import json

from .constants import TYPES
from .headers import HTTPHeaderDict
from .helpers import trigger_methods


class Response:
    """
    Response is used to declare and compose an HTTP mock responses fields.

    It provides a chainable DSL interface for easier and declarative usage.

    Arguments:
        status (int): HTTP response status code. Defaults to ``200``.
        headers (dict): HTTP response headers.
        body (str|bytes): HTTP response body.
        json (str|dict|list): HTTP response JSON body.
        xml (str): HTTP response XML body.
        type (str): HTTP response content MIME type.
        file (str): file path to HTTP body response.

    Attributes:
        mock (pook.Mock): reference to mock instance.
    """

    _KEY_ORDER = (
        "body",
        "content",
        "file",
        "header",
        "headers",
        "json",
        "mock",
        "set",
        "status",
        "type",
        "xml",
    )

    def __init__(self, **kw):
        self._status = 200
        self._mock = None
        self._body = None
        self._headers = HTTPHeaderDict()

        # Trigger response method based on input arguments
        trigger_methods(self, kw, self._KEY_ORDER)

    def status(self, code=200):
        """
        Defines the response status code.

        Arguments:
            code (int): response status code.

        Returns:
            self: ``pook.Response`` current instance.
        """
        self._status = int(code)
        return self

    def header(self, key, value):
        """
        Defines a new response header.
        Alias to ``Response.header()``.

        Arguments:
            header (str): header name.
            value (str): header value.

        Returns:
            self: ``pook.Response`` current instance.
        """
        if type(key) is tuple:
            key, value = str(key[0]), key[1]

        headers = {key: value}
        self._headers.extend(headers)
        return self

    def headers(self, headers):
        """
        Defines a new response header.
        Alias to ``Response.header()``.

        Arguments:
            header (str): header name.
            value (str): header value.

        Returns:
            self: ``pook.Response`` current instance.
        """
        self._headers.extend(headers)
        return self

    def set(self, header, value):
        """
        Defines a new response header.
        Alias to ``Response.header()``.

        Arguments:
            header (str): header name.
            value (str): header value.

        Returns:
            self: ``pook.Response`` current instance.
        """
        self._headers[header] = value
        return self

    def type(self, name):
        """
        Defines the response ``Content-Type`` header.
        Alias to ``Response.content(mime)``.

        You can pass one of the following type aliases instead of the full
        MIME type representation:

        - ``json`` = ``application/json``
        - ``xml`` = ``application/xml``
        - ``html`` = ``text/html``
        - ``text`` = ``text/plain``
        - ``urlencoded`` = ``application/x-www-form-urlencoded``
        - ``form`` = ``application/x-www-form-urlencoded``
        - ``form-data`` = ``application/x-www-form-urlencoded``

        Arguments:
            value (str): type alias or header value to match.

        Returns:
            self: ``pook.Response`` current instance.
        """
        return self.content(name)

    def content(self, name):
        """
        Defines the response ``Content-Type`` header.

        You can pass one of the following type aliases instead of the full
        MIME type representation:

        - ``json`` = ``application/json``
        - ``xml`` = ``application/xml``
        - ``html`` = ``text/html``
        - ``text`` = ``text/plain``
        - ``urlencoded`` = ``application/x-www-form-urlencoded``
        - ``form`` = ``application/x-www-form-urlencoded``
        - ``form-data`` = ``application/x-www-form-urlencoded``

        Arguments:
            value (str): type alias or header value to match.

        Returns:
            self: ``pook.Response`` current instance.
        """
        self._headers["Content-Type"] = TYPES.get(name, name)
        return self

    def body(self, body, *, chunked=False):
        """
        Defines response body data.

        Arguments:
            body (str|bytes|list): response body to use.
            chunked (bool): return a chunked response.

        Returns:
            self: ``pook.Response`` current instance.
        """
        if hasattr(body, "encode"):
            body = body.encode("utf-8", "backslashreplace")
        elif isinstance(body, list):
            for i, chunk in enumerate(body):
                if hasattr(chunk, "encode"):
                    body[i] = chunk.encode("utf-8", "backslashreplace")

        self._body = body

        if chunked:
            self.header("Transfer-Encoding", "chunked")
        return self

    def json(self, data):
        """
        Defines the mock response JSON body.

        Arguments:
            data (dict|list|str): JSON body data.

        Returns:
            self: ``pook.Response`` current instance.
        """
        self._headers["Content-Type"] = "application/json"
        if not isinstance(data, str):
            data = json.dumps(data, indent=4)

        return self.body(data)

    def xml(self, xml):
        """
        Defines the mock response XML body.

        For not it only supports ``str`` as input type.

        Arguments:
            xml (str): XML body data to use.

        Returns:
            self: ``pook.Response`` current instance.
        """
        return self.body(xml)

    def file(self, path):
        """
        Defines the response body from file contents.

        Arguments:
            path (str): disk file path to load.

        Returns:
            self: ``pook.Response`` current instance.
        """
        with open(path, "rb") as f:
            return self.body(f.read())

    @property
    def mock(self):
        """
        Getter accessor for `mock` attribute.
        """
        return self._mock

    @mock.setter
    def mock(self, mock):
        """
        Setter for ``mock`` attribute.
        """
        self._mock = mock

    def __repr__(self):
        """
        Returns an human friendly readable instance data representation.

        Returns:
            str
        """
        args = []
        for key in ("headers", "status", "body"):
            value = getattr(self, f"_{key}")
            args.append(f"{key}={value}")
        return "Response(\n    {}\n)".format(",\n    ".join(args))
