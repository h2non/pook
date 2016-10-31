pook |Build Status| |PyPI| |Coverage Status| |Documentation Status| |Stability| |Quality| |Versions|
====================================================================================================

Expressive utility library for HTTP traffic mocking and expectations made simply in `Python`_.

pook is heavily inspired by `gock`_.

**Note**: work in progress.

Features
--------

-  Simple, expressive and fluent API
-  Full-featured, idiomatic HTTP expectations.
-  JSON schema based body matching.
-  HTTP client agnostic (works with most popular HTTP libraries).
-  Extensible design: write your own HTTP matchers and adapters.
-  Pluggable hackable API.
-  Compatible with Python 2 and 3.
-  Dependency free.

Supported HTTP clients
----------------------

- [X] urllib3
- [X] requests
- [ ] urllib
- [ ] aiohttp
- [ ] pycurl

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

See `annotated API reference`_.

Examples
--------

Basic mocking
^^^^^^^^^^^^^

.. code:: python

    import pook
    import requests

    @pook.activate
    def test_my_api():
        mock = httpok.get('http://twitter.com/api/1/foobar',
                        type='application/json',
                        json={'error': 'not found'})
        mock.reply(404, json={'error': 'foo'})

        resp = requests.get('http://twitter.com/api/1/foobar')
        assert resp.json() == {"error": "not found"}
        assert len(mock.calls) == 1
        assert mock.calls[0].request.url == 'http://twitter.com/api/1/foobar'
        assert mock.calls[0].response.text == '{"error": "not found"}'

Using the fluent API
^^^^^^^^^^^^^^^^^^^^

.. code:: python

    import pook
    import requests

    @pook.activate
    def test_my_api():
        mock = pook.get('http://twitter.com/api/1/foobar'). \
               status(404). \
               json({'error': 'not found'})

        resp = requests.get('http://twitter.com/api/1/foobar')
        assert resp.json() == {"error": "not found"}
        assert len(mock.calls) == 1
        assert mock.calls[0].request.url == 'http://twitter.com/api/1/foobar'
        assert mock.calls[0].response.text == '{"error": "not found"}'

License
-------

MIT - Tomas Aparicio

.. _Python: http://python.org
.. _magic numbers: https://en.wikipedia.org/wiki/Magic_number_(programming)#Magic_numbers_in_files
.. _gock: https://github.com/h2non/gock
.. _annotated API reference: https://h2non.github.io/pook


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
