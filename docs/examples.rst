assertion
---------

.. code-block:: python

    pook('http://api.example.com').get('/foo').reply(200, headers={'Server': 'nginx'})

    pook('http://api.example.com').get('/bar').reply(404)

    pook('http://api.example.com').get('/baz').reply(400)
