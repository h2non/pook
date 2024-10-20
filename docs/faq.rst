FAQ
===

How does it work?
-----------------

Please, read `how it works`_ section.


What HTTP clients are supported?
--------------------------------

Please, see `supported HTTP clients`_ section.


.. _supported HTTP clients: index.html#supported-http-clients

.. _how it works: how_it_works.html


Does ``pook`` mock out all the outgoing HTTP traffic from my app?
-----------------------------------------------------------------

Yes, that's the default behaviour: any outgoing HTTP traffic across the supported
HTTP clients will be intercepted by ``pook``.

In case that an outgoing request does not match any mock expectation, an exception error
will be raised, telling you no mock was matched in order to review or fix your code accordingly.

You can change this behaviour and don't raise any exception if no mock definition can be matched.

You can change this enabling the real networking mode via :func:`pook.enable_network`.


Can I use ``pook`` in a non-testing environment?
------------------------------------------------

Absolutely. ``pook`` is testing environment agnostic.

You simply have to take care of the side effects of mocking HTTP traffic in
a runtime environment.

For that cases you probably want to enable the real networking mode.


Can I use ``pook`` with a custom HTTP traffic mock interceptor engine?
----------------------------------------------------------------------

Yes, you can. ``pook`` is very modular and open for extensibility.

You can programmatically define the HTTP traffic mock engine you want to use via
:func:`pook.set_mock_engine`. This will replace the built-in one.

This can be particularly useful if you are already using another HTTP mocking
engine that satisfy your needs, but you want to take benefit of ``pook``
features, versatility and simple to use expressive API.

For mock engine implementation details, see :any:`pook.MockEngine` API documentation.


Can I use ``pook`` with any test framework?
-------------------------------------------

Yes. ``pook`` is framework-agnostic.
You can use it within ``unittest``, ``pytest`` or others.
