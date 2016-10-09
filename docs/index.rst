.. pook documentation master file, created by
   sphinx-quickstart on Tue Oct  4 18:59:54 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Pook
====

**pook** is an *expressive* and *extensible* HTTP mocking library for Python.
pook can be *extended* by defining `new matchers <custom-matchers.html>`_.

Usage
-----

Just import the ``expect`` callable and the `built-in matchers <matchers.html>`_ and start writing test assertions.

.. code-block:: python

    import pook

    pook('api.server.com').get('/foo').reply(200).json({'foo': 'bar'})


Contents
--------

.. toctree::
   :maxdepth: 2

   install
   matchers
   history


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
