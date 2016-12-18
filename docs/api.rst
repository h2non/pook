.. _api:

API Documentation
=================

Core API
--------

.. toctree::

   pook.activate <http://pook.readthedocs.io/en/latest/api.html#pook.activate>
   pook.on <http://pook.readthedocs.io/en/latest/api.html#pook.on>
   pook.disable <http://pook.readthedocs.io/en/latest/api.html#pook.disable>
   pook.off <http://pook.readthedocs.io/en/latest/api.html#pook.off>
   pook.reset <http://pook.readthedocs.io/en/latest/api.html#pook.reset>
   pook.engine <http://pook.readthedocs.io/en/latest/api.html#pook.engine>
   pook.use <http://pook.readthedocs.io/en/latest/api.html#pook.use>
   pook.context <http://pook.readthedocs.io/en/latest/api.html#pook.context>
   pook.enable_network <http://pook.readthedocs.io/en/latest/api.html#pook.enable_network>
   pook.disable_network <http://pook.readthedocs.io/en/latest/api.html#pook.disable_network>
   pook.use_network <http://pook.readthedocs.io/en/latest/api.html#pook.use_network>
   pook.use_network_filter <http://pook.readthedocs.io/en/latest/api.html#pook.use_network_filter>
   pook.flush_network_filters <http://pook.readthedocs.io/en/latest/api.html#pook.flush_network_filters>
   pook.mock <http://pook.readthedocs.io/en/latest/api.html#pook.mock>
   pook.get <http://pook.readthedocs.io/en/latest/api.html#pook.get>
   pook.put <http://pook.readthedocs.io/en/latest/api.html#pook.put>
   pook.delete <http://pook.readthedocs.io/en/latest/api.html#pook.delete>
   pook.head <http://pook.readthedocs.io/en/latest/api.html#pook.head>
   pook.patch <http://pook.readthedocs.io/en/latest/api.html#pook.patch>
   pook.options <http://pook.readthedocs.io/en/latest/api.html#pook.options>
   pook.pending <http://pook.readthedocs.io/en/latest/api.html#pook.pending>
   pook.ispending <http://pook.readthedocs.io/en/latest/api.html#pook.ispending>
   pook.pending_mocks <http://pook.readthedocs.io/en/latest/api.html#pook.pending_mocks>
   pook.unmatched_requests <http://pook.readthedocs.io/en/latest/api.html#pook.unmatched_requests>
   pook.unmatched <http://pook.readthedocs.io/en/latest/api.html#pook.unmatched>
   pook.isunmatched <http://pook.readthedocs.io/en/latest/api.html#pook.isunmatched>
   pook.isactive <http://pook.readthedocs.io/en/latest/api.html#pook.isactive>
   pook.isdone <http://pook.readthedocs.io/en/latest/api.html#pook.isdone>
   pook.regex <http://pook.readthedocs.io/en/latest/api.html#pook.regex>

   pook.Mock <http://pook.readthedocs.io/en/latest/api.html#pook.Mock>
   pook.Engine <http://pook.readthedocs.io/en/latest/api.html#pook.Engine>
   pook.Request <http://pook.readthedocs.io/en/latest/api.html#pook.Request>
   pook.Response <http://pook.readthedocs.io/en/latest/api.html#pook.Response>
   pook.MockEngine <http://pook.readthedocs.io/en/latest/api.html#pook.MockEngine>
   pook.MatcherEngine <http://pook.readthedocs.io/en/latest/api.html#pook.MatcherEngine>


.. automodule:: pook
    :members:
    :undoc-members:
    :show-inheritance:


Matchers API
------------

.. toctree::

   pook.matchers.init <http://pook.readthedocs.io/en/latest/api.html#pook.matchers.init>
   pook.matchers.add <http://pook.readthedocs.io/en/latest/api.html#pook.matchers.add>
   pook.matchers.get <http://pook.readthedocs.io/en/latest/api.html#pook.matchers.get>
   pook.matchers.BaseMatcher <http://pook.readthedocs.io/en/latest/api.html#pook.matchers.BaseMatcher>
   pook.matchers.MethodMatcher <http://pook.readthedocs.io/en/latest/api.html#pook.matchers.MethodMatcher>
   pook.matchers.URLMatcher <http://pook.readthedocs.io/en/latest/api.html#pook.matchers.URLMatcher>
   pook.matchers.HeadersMatcher <http://pook.readthedocs.io/en/latest/api.html#pook.matchers.HeadersMatcher>
   pook.matchers.PathMatcher <http://pook.readthedocs.io/en/latest/api.html#pook.matchers.PathMatcher>
   pook.matchers.BodyMatcher <http://pook.readthedocs.io/en/latest/api.html#pook.matchers.BodyMatcher>
   pook.matchers.XMLMatcher <http://pook.readthedocs.io/en/latest/api.html#pook.matchers.XMLMatcher>
   pook.matchers.JSONMatcher <http://pook.readthedocs.io/en/latest/api.html#pook.matchers.JSONMatcher>
   pook.matchers.JSONSchemaMatcher <http://pook.readthedocs.io/en/latest/api.html#pook.matchers.JSONSchemaMatcher>
   pook.matchers.QueryMatcher <http://pook.readthedocs.io/en/latest/api.html#pook.matchers.QueryMatcher>


.. automodule:: pook.matchers
    :members:
    :undoc-members:
    :show-inheritance:


Interceptors API
----------------

.. toctree::

   pook.interceptors.add <http://pook.readthedocs.io/en/latest/api.html#pook.interceptors.add>
   pook.interceptors.get <http://pook.readthedocs.io/en/latest/api.html#pook.interceptors.get>
   pook.interceptors.BaseInterceptor <http://pook.readthedocs.io/en/latest/api.html#pook.interceptors.BaseInterceptor>
   pook.interceptors.Urllib3Interceptor <http://pook.readthedocs.io/en/latest/api.html#pook.interceptors.Urllib3Interceptor>
   pook.interceptors.AIOHTTPInterceptor <http://pook.readthedocs.io/en/latest/api.html#pook.interceptors.AIOHTTPInterceptor>
   pook.interceptors.HTTPClientInterceptor <http://pook.readthedocs.io/en/latest/api.html#pook.interceptors.HTTPClientInterceptor>

.. automodule:: pook.interceptors
    :members:
    :undoc-members:
    :show-inheritance:
