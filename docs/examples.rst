Examples
========


Basic mocking example using requests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/requests_client.py



Chainable API DSL
^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/chainable_api.py



Context manager for isolated mocking
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/context_manager.py


Single mock context manager definition for isolated mocking
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/mock_context_manager.py


Declaring mocks as decorators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/decorators.py


Activating the mock engine via decorator within the function context
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/decorator_activate.py


Activating the mock engine via decorator within an async coroutine function context
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/decorator_activate_async.py


Featured JSON body matching
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/json_matching.py



JSONSchema based body matching
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/json_schema.py


Request Query Params matching
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/query_params_matching.py


Enable real networking mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/network_mode.py



Persistent mock
^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/persistent_mock.py



Time TTL limited mock
^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/time_ttl_mock.py



Regular expression matching
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/regex.py



``unittest`` integration
^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/unittest_example.py



``py.test`` integration
^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/pytest_example.py



Simulated error exception on mock matching
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/simulated_error.py



Using ``urllib3`` as HTTP client
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/urllib3_client.py



Using ``urllib3`` to return a chunked response
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/urllib3_chunked_response.py



Asynchronous HTTP request using ``aiohttp``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/aiohttp_client.py



Using ``http.client`` standard Python package as HTTP client
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/http_client_native.py


Example using `mocket`_ Python library as underlying mock engine
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/mocket_example.py


Hy programming language example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/basic.hy


.. _mocket: https://github.com/mindflayer/python-mocket
