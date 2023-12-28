pook |PyPI| |Coverage Status| |Documentation Status| |Stability| |Quality| |Versions|
=====================================================================================

Versatile, expressive and hackable utility library for HTTP traffic mocking
and expectations made easy in `Python`_. Heavily inspired by `gock`_.

To get started, read the `documentation`_, `how it works`_, `FAQ`_ or `examples`_.

Features
--------

-  Simple, expressive and fluent API.
-  Provides both Pythonic and chainable DSL API styles.
-  Full-featured HTTP response definitions and expectations.
-  Matches any HTTP protocol primitive (URL, method, query params, headers, body...).
-  Full regular expressions capable mock expectations matching.
-  Supports most popular HTTP clients via interceptor adapters.
-  Configurable volatile, persistent or TTL limited mocks.
-  Works with unittest and pytest.
-  First-class JSON & XML support matching and responses.
-  Supports JSON Schema body matching.
-  Works in both runtime and testing environments.
-  Can be used as decorator and/or via context managers.
-  Supports real networking mode with optional traffic filtering.
-  Map/filter mocks easily for generic or custom mock expectations.
-  Custom user-defined mock matcher functions.
-  Simulated raised error exceptions.
-  Network delay simulation (only available for ``aiohttp``).
-  Pluggable and hackable API.
-  Customizable HTTP traffic mock interceptor engine.
-  Supports third-party mocking engines, such as `mocket`_.
-  Fits good for painless test doubles.
-  Does not support WebSocket traffic mocking.
-  Works with +3.8 (including PyPy).
-  Dependency-less: just 3 small dependencies for JSONSchema, XML tree comparison, and URL parsing.


Supported HTTP clients
----------------------

``pook`` can work with multiple mock engines, however it provides a
built-in one by default, which currently supports traffic mocking in
the following HTTP clients:

-  ✔  `urllib3`_ v1+
-  ✔  `requests`_ v2+
-  ✔  `aiohttp`_ v3+
-  ✔  `urllib`_ / `http.client`_
-  ✔  `httpx`_

More HTTP clients can be supported progressively.

**Note**: only recent HTTP client package versions were tested.

Installation
------------

Using ``pip`` package manager (requires pip 1.8+):

.. code:: bash

    pip install --upgrade pook

Or install the latest sources from Github:

.. code:: bash

    pip install -e git+git://github.com/h2non/pook.git#egg=pook


Getting started
---------------

See ReadTheDocs documentation:

|Documentation Status|


API
---

See `annotated API reference`_ documention.


Examples
--------

See `examples`_ documentation for full featured code and use case examples.

Basic mocking:

.. code:: python

    import pook
    import requests

    @pook.on
    def test_my_api():
        mock = pook.get('http://twitter.com/api/1/foobar', reply=404, response_json={'error': 'not found'})

        resp = requests.get('http://twitter.com/api/1/foobar')
        assert resp.status_code == 404
        assert resp.json() == {"error": "not found"}
        assert mock.calls == 1

Using the chainable API DSL:

.. code:: python

    import pook
    import requests

    @pook.on
    def test_my_api():
        mock = (pook.get('http://twitter.com/api/1/foobar')
                  .reply(404)
                  .json({'error': 'not found'}))

        resp = requests.get('http://twitter.com/api/1/foobar')
        assert resp.json() == {"error": "not found"}
        assert mock.calls == 1

Using the decorator:

.. code:: python

    import pook
    import requests

    @pook.get('http://httpbin.org/status/500', reply=204)
    @pook.get('http://httpbin.org/status/400', reply=200)
    def fetch(url):
        return requests.get(url)

    res = fetch('http://httpbin.org/status/400')
    print('#1 status:', res.status_code)

    res = fetch('http://httpbin.org/status/500')
    print('#2 status:', res.status_code)


Simple ``unittest`` integration:

.. code:: python

    import pook
    import unittest
    import requests


    class TestUnitTestEngine(unittest.TestCase):

        @pook.on
        def test_request(self):
            pook.get('server.com/foo').reply(204)
            res = requests.get('http://server.com/foo')
            self.assertEqual(res.status_code, 204)

        def test_request_with_context_manager(self):
            with pook.use():
                pook.get('server.com/bar', reply=204)
                res = requests.get('http://server.com/bar')
                self.assertEqual(res.status_code, 204)


Using the context manager for isolated HTTP traffic interception blocks:

.. code:: python

    import pook
    import requests

    # Enable HTTP traffic interceptor
    with pook.use():
        pook.get('http://httpbin.org/status/500', reply=204)

        res = requests.get('http://httpbin.org/status/500')
        print('#1 status:', res.status_code)

    # Interception-free HTTP traffic
    res = requests.get('http://httpbin.org/status/200')
    print('#2 status:', res.status_code)

Example using `mocket`_ Python library as underlying mock engine:

.. code:: python

    import pook
    import requests
    from mocket.plugins.pook_mock_engine import MocketEngine

    # Use mocket library as underlying mock engine
    pook.set_mock_engine(MocketEngine)

    # Explicitly enable pook HTTP mocking (optional)
    pook.on()

    # Target server URL to mock out
    url = 'http://twitter.com/api/1/foobar'

    # Define your mock
    mock = pook.get(url,
                    reply=404, times=2,
                    headers={'content-type': 'application/json'},
                    response_json={'error': 'foo'})

    # Run first HTTP request
    requests.get(url)
    assert mock.calls == 1

    # Run second HTTP request
    res = requests.get(url)
    assert mock.calls == 2

    # Assert response data
    assert res.status_code == 404
    assert res.json() == {'error': 'foo'}

    # Explicitly disable pook (optional)
    pook.off()


Example using Hy language (Lisp dialect for Python):

.. code:: hy

    (import [pook])
    (import [requests])

    (defn request [url &optional [status 404]]
      (doto (.mock pook url) (.reply status))
      (let [res (.get requests url)]
        (. res status_code)))

    (defn run []
      (with [(.use pook)]
        (print "Status:" (request "http://server.com/foo" :status 204))))

    ;; Run test program
    (defmain [&args] (run))


Development
-----------

Clone the repository:

.. code:: bash

    git clone git@github.com:h2non/pook.git


Use [`hatch`](https://hatch.pypa.io/) to configure the environment by running the test suite:

.. code:: bash

    hatch run test


Install the pre-commit hook:

.. code:: bash

    hatch run lint:install


Lint the code:

.. code:: bash

    hatch run lint:run


Run tests on all supported Python versions and implementations (this requires your host operating system to have each implementation available):

.. code:: bash

    hatch run test:test


To run tests only for a specific version, affix the version designation to the environment name (the left side of the `:`):

.. code:: bash

    hatch run test.pypy3.10:test


Generate documentation:

.. code:: bash

    hatch run docs:build


License
-------

MIT - Tomas Aparicio

.. _Go: https://golang.org
.. _Python: http://python.org
.. _gock: https://github.com/h2non/gock
.. _annotated API reference: http://pook.readthedocs.io/en/latest/api.html
.. _examples: http://pook.readthedocs.io/en/latest/examples.html
.. _aiohttp: https://github.com/KeepSafe/aiohttp
.. _httpx: https://www.python-httpx.org/
.. _requests: http://docs.python-requests.org/en/master/
.. _urllib3: https://github.com/shazow/urllib3
.. _urllib: https://docs.python.org/3/library/urllib.html
.. _http.client: https://docs.python.org/3/library/http.client.html
.. _documentation: http://pook.readthedocs.io/en/latest/
.. _FAQ: http://pook.readthedocs.io/en/latest/faq.html
.. _how it works: http://pook.readthedocs.io/en/latest/how_it_works.html
.. _mocket: https://github.com/mindflayer/python-mocket

.. |PyPI| image:: https://img.shields.io/pypi/v/pook.svg?maxAge=2592000?style=flat-square
   :target: https://pypi.python.org/pypi/pook
.. |Coverage Status| image:: https://coveralls.io/repos/github/h2non/pook/badge.svg?branch=master
   :target: https://coveralls.io/github/h2non/pook?branch=master
.. |Documentation Status| image:: https://img.shields.io/badge/docs-latest-green.svg?style=flat
   :target: http://pook.readthedocs.io/en/latest/?badge=latest
.. |Quality| image:: https://codeclimate.com/github/h2non/pook/badges/gpa.svg
   :target: https://codeclimate.com/github/h2non/pook
   :alt: Code Climate
.. |Stability| image:: https://img.shields.io/pypi/status/pook.svg
   :target: https://pypi.python.org/pypi/pook
   :alt: Stability
.. |Versions| image:: https://img.shields.io/pypi/pyversions/pook.svg
   :target: https://pypi.python.org/pypi/pook
   :alt: Python Versions
