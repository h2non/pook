pook |Build Status| |PyPI| |Coverage Status| |Documentation Status| |Stability| |Quality| |Versions|
====================================================================================================

Versatile and expressive utility library for simple HTTP traffic mocking and expectations in `Python`_.

`pook` is HTTP client agnostic and works with most popular HTTP packages via adapters.
If someone is not supported yet, it can be in a future via interceptor adapter.

pook was heavily inspired by `gock`_ Go package.

**Note**: work in progress.

Features
--------

-  Simple, expressive and fluent API.
-  Pythonic DSL for easy mocks and responses definition.
-  Full-featured, idiomatic HTTP response expectations.
-  Match any HTTP protocol primitive (URL, method, query params, headers, body...)
-  Full RegExp capable HTTP traffic matching.
-  JSON Schema based body matching.
-  HTTP client agnostic via adapters (works with most popular HTTP packages).
-  Extensible design: write your own HTTP matchers and adapters.
-  Extensible, pluggable and hackable API.
-  Work with Python +2.7 and 3.
-  Just one dependency = JSONSchema validator.

Supported HTTP clients
----------------------

- [✔] urllib3 / requests
- [✔] aiohttp
- [✔] urllib / http.client (experimental)
- [x] pycurl (pending)

Installation
------------

Using ``pip`` package manager:

.. code:: bash

    pip install pook

Or install the latest sources from Github::

.. code:: bash

    pip install -e git+git://github.com/h2non/pook.git#egg=pook

API
---

See `API reference`_ documention.

Examples
--------

Basic mocking
^^^^^^^^^^^^^

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

Using the chainable API
^^^^^^^^^^^^^^^^^^^^^^^

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

License
-------

MIT - Tomas Aparicio

.. _Python: http://python.org
.. _gock: https://github.com/h2non/gock
.. _annotated API reference: http://pook.rtfd.io


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
