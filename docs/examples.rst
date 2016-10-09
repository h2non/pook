assertion
---------

.. code-block:: python

    pock('http://api.example.com').get('/foo').reply(200, headers={'Server': 'nginx'})

    pock('http://api.example.com').get('/bar').reply(404)

    pock('http://api.example.com').get('/baz').reply(400)
