How it works
============

HTTP traffic interception
-------------------------

In a nutshell, ``pook`` uses ``unittest.mock`` standard Python package in order
to patch external library objects, allowing ``pook`` HTTP interceptor adapter to patch any third-party packages
and intercept specific function calls.

``pook`` entirely relies on this interception strategy, therefore in the meantime ``pook`` is active,
any outgoing HTTP traffic intercepted by the supported HTTP clients won't imply any real TCP networking,
except if you enabled the real networking mode via ``pook.enable_network()``, which in
that case real network traffic can be established.

Worth clarifying that ``pook`` only works at Python programmatic runtime level.
There's no network/socket programming involved.


HTTP request matching
---------------------

Outgoing HTTP traffic is intercepted and matched against a pool of mock matchers
defined in your mock expectations.

Matching process in sequential and executed as FIFO order, meaning the first has always
preference.

For instance, if you declare multiple identical mocks, the first one will be matched first and the others
will be ignored. Once the first one expires, the subsequent mock definition in the chain will be matched instead.


Real networking mode
--------------------

By default real networking mode is disabled.
This basically means that real networking will not happen unless you explicitely enable it.

This behaviour has been adopted to improve predictability, control and mitigate developers fear between
behaviour boundaries and expectations.

``pook`` will prevent you to communicate with real HTTP servers unless you enable it via: ``pook.enable_network()``.

Also, you can partially restrict the real networking by filtering only certain hosts.
You can do that via ``pook.use_network_filter(filter_fn)``.


Volatile vs Persistent mocks
----------------------------

By default, mocks are volatile. This means that once a mock has been matched,
and therefore consumed, it will be flushed.

You can modify this behaviour via:

Explicitly definining the TTL of each mock, so effectively the number of times the mock can be matched and consumed:

.. code:: python

    # Match a mock up to 5 times, then flush it
    pook.get('server.com/api').times(5)

    # The above is equivalent to
    pook.get('server.com/api', times=5)


Explicitly definining a persistent mock:

.. code:: python

    # Make a mock definition persistent, so it won't be never flushed
    pook.get('server.com/api').persist()

    # The above is equivalent to
    pook.get('server.com/api', persist=True)
