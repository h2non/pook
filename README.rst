pook |Build Status| |PyPI| |Coverage Status| |Documentation Status| |Stability| |Quality| |Versions|
====================================================================================================

Versatile, expressive and hackable utility library for HTTP traffic mocking and expectations in `Python`_.

``pook`` was heavily inspired in `gock`_, its equivalent package for `Go`_.

**Still beta**: please, report any issue you may experiment.


Features
--------

-  Simple, expressive and fluent API.
-  Provides both Pythonic and chainable DSL API styles.
-  Full-feated HTTP response definitions and expectations.
-  Match any HTTP protocol primitive (URL, method, query params, headers, body...).
-  Full regular expressions capable mock expectations matching.
-  HTTP client agnostic via adapters (works with most popular HTTP packages).
-  Supports JSON Schema body matching.
-  Configurable volatile, persistent or TTL limited mocks.
-  Works with any testing framework or engine (unittest, pytest, nosetests...).
-  Usable in both runtime and testing environments.
-  Can be used as decorator and/or via context managers.
-  Real networking mode with optional custom traffic filtering.
-  Map/filter mocks easily for generic or custom mock expectations.
-  First-class JSON/XML body matching support and response expectations.
-  Simulated error exceptions.
-  Network delay simulation (only available in ``aiohttp``).
-  Pluggable and hackable API.
-  Does not support WebSocket.
-  Works with Python +2.7 and +3.0 (including PyPy).
-  Dependency-less (just 2 small dependencies for JSONSchema and XML comparison helpers)


Supported HTTP clients
----------------------

-  ✔ `urllib3`_ / `requests`_
-  ✔ `aiohttp`_
-  ✔ `urllib`_ / `http.client`_ (experimental)
-  ✘ `pycurl`_ (see `#16`_)


Installation
------------

Using ``pip`` package manager:

.. code:: bash

    pip install pook

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

    @pook.activate
    def test_my_api():
        mock = pook.get('http://twitter.com/api/1/foobar',
                        type='json',
                        json={'error': 'not found'})
        mock.reply(404, json={'error': 'foo'})

        resp = requests.get('http://twitter.com/api/1/foobar')
        assert resp.json() == {"error": "not found"}
        assert len(mock.calls) == 1
        assert mock.calls[0].request.url == 'http://twitter.com/api/1/foobar'
        assert mock.calls[0].response.text == '{"error": "not found"}'

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
        assert len(mock.calls) == 1
        assert mock.calls[0].request.url == 'http://twitter.com/api/1/foobar'
        assert mock.calls[0].response.text == '{"error": "not found"}'


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


Install dependencies:

.. code:: bash

    pip install -r requirements.txt requirements-dev.txt


Install Python dependencies:

.. code:: bash

    make install


Lint code:

.. code:: bash

    make lint


Run tests:

.. code:: bash

    make test


Generate documentation:

.. code:: bash

    make htmldocs


License
-------

MIT - Tomas Aparicio

.. _Go: https://golang.org
.. _Python: http://python.org
.. _gock: https://github.com/h2non/gock
.. _annotated API reference: http://pook.rtfd.io
.. _#16: https://github.com/h2non/pook/issues/16
.. _examples/: http://pook.readthedocs.io/en/latest/examples.html
.. _aiohttp: https://github.com/KeepSafe/aiohttp
.. _requests: http://docs.python-requests.org/en/master/
.. _urllib3: https://github.com/shazow/urllib3
.. _urllib: https://docs.python.org/3/library/urllib.html
.. _http.client: https://docs.python.org/3/library/http.client.html
.. _pycurl: http://pycurl.io/

.. |Build Status| image:: https://travis-ci.org/h2non/pook.svg?branch=master
   :target: https://travis-ci.org/h2non/pook
.. |PyPI| image:: https://img.shields.io/pypi/v/pook.svg?maxAge=2592000?style=flat-square
   :target: https://pypi.python.org/pypi/pook
.. |Coverage Status| image:: https://coveralls.io/repos/github/h2non/pook/badge.svg?branch=master
   :target: https://coveralls.io/github/h2non/pook?branch=master
.. |Documentation Status| image:: https://readthedocs.org/projects/pook/badge/?version=latest
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
