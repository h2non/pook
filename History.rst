History
=======

v2.1.3 / 2024-12-16
-------------------------

  * Ensure aiohttp headers can be matched from both the session and request in the same matcher

v2.1.2 / 2024-11-21
-------------------------

  * Return the correct type of ``headers`` object for standard library urllib by @sarayourfriend in https://github.com/h2non/pook/pull/154.
  * Support ``Sequence[tuple[str, str]]`` header input with aiohttp by @sarayourfriend in https://github.com/h2non/pook/pull/154.
  * Fix network filters when multiple filters are active by @rsmeral in https://github.com/h2non/pook/pull/155.
  * Fix aiohttp matching not working with session base URL or headers by @sarayourfriend in https://github.com/h2non/pook/pull/157.
  * Add support for Python 3.13 by @sarayourfriend in https://github.com/h2non/pook/pull/149.

v2.1.1 / 2024-10-15
-------------------------

  * Flush mocks when `pook.activate` used as a wrapper by @shift0965 in https://github.com/h2non/pook/pull/145.

    * This prevents mocks from leaking between test cases and should fix some potentially confusing edge case bugs.


v2.1.0 / 2024-10-08
-------------------------

  * Drop support for Python 3.8 (it is EOL 2024-10-07)

v2.0.1 / 2024-10-08
-------------------------

  * Improve aiohttp JSONMatcher support by @KyleJamesWalker in https://github.com/h2non/pook/pull/139

v2.0.0 / 2024-07-01
-------------------------

See https://github.com/h2non/pook/issues/128 for a summary of the breaking changes and how to update your code if you are affected.

  * **Breaking change**: Remove ``Response::body``'s ``binary`` parameter and enforce a keyword argument for ``chunked``.

    * The ``binary`` parameter is no longer needed since responses are now always byte-encoded in all cases (see below).
    * A keyword argument is now enforced for ``chunked`` to ensure unnamed arguments meant for the removed ``binary`` parameter cannot be confused as ``chunked`` arguments.

  * Only return byte-encoded response bodies, matching the bahviour of all supported client libraries.

    * This is possible because for all supported client libraries, pook mocks the actual response sent to the
      client library over the wire, which will, in all cases, be bytes. Client libraries that support reading
      response content as a string or other formats will continue to work as expected, because they'll always
      be handling bytes from pook.
    * This causes no change to application code for users of pook, except for users of the standard library ``urllib``,
      for which this also fixed a bug where non-bytes bodies were returned by pook in certain cases. This is impossible
      in real application code. If you rely on pook to mock ``urllib`` responses and have code that handles non-bytes response
      bodies, that code can be safely deleted (provided the only reason it was there was pook in the first place).

  * **Breaking change**: Remove ``Mock::body``'s ``binary`` parameter.

    * This parameter was already unused due to a bug in the code (it was not passed through to the ``BodyMatcher``),
      so this will not cause any changes to tests that relied on it: it didn't do anything to begin with.
    * The breaking change is simply the removal of the unused parameter, which should be deleted from tests using pook.
    * Pook's code has also been updated to remove all cases where non-bytes objects were being handled. Instead, the body
      of any interecepted request will always be stored as bytes, and only decoded when necessary for individual downstream
      matchers (JSON, XML).

  * Correct documentation strings for ``XMLMatcher`` and ``JSONMatcher`` to no longer suggest they can handle regex matchers.

    * These classes never implemented regex matching.

  * Add a pytest fixture to the package.

v1.4.3 / 2024-02-23
-------------------

  * Fix httpx incorrectly named method on interceptor subclass by @sarayourfriend in https://github.com/h2non/pook/pull/126

v1.4.2 / 2024-02-15
-------------------

  * fix #122: httpx streaming via `iter_raw` raises `httpx.StreamConsumed` by @petarmaric in https://github.com/h2non/pook/pull/123

v1.4.1 / 2024-02-12
-------------------

  * Fix `Mock` constructor params/url order mishandling (#111)
  * Optionally match empty values in query parameter presence matcher (#113)
  * Fix httpx network mode (#116)

v1.4.0 / 2023-12-29
-------------------

  * Add support for httpx (#90)
  * Enable mocket integration tests for Python >= 3.11 (#103)

v1.3.0 / 2023-12-25
-------------------

This release modernizes Pook build and development environments.

  * Drop support for EOL'd Python versions (in other words, 3.6 and 3.7)
  * Use pyproject.toml
  * Use ruff to lint files
  * Use pre-commit to add pre-commit hooks
  * Use hatch to manage test, development, and build environments
  * Fix the test configuration to actually run the example tests
  * Fix the documentation build
  * Fix support for asynchronous functions in the activate decorator (this was a direct result of re-enabling the example tests and finding lots of little issues)
  * Remove all mention of the unsupported pycurl library
  * Clean up tests that can use pytest parametrize to do so (and get better debugging information during tests runs as a result)
  * Use pytest-pook to clean up a bunch of unnecessary test fixtures
  * Fix deprecation warning for invalid string escape sequences caused by untagged regex strings

v1.2.1 / 2023-12-23
-------------------

  * Fix usage of regex values in header matchers (#97)
  * Fix urllib SSL handling (#98)

v1.2.0 / 2023-12-17
-------------------

  * feat(api): add support for binary bodies (#88)
  * fix(urllib3): don't put non-strings into HTTP header dict (#87)
  * refactor: drop Python 3.5 support (#92). Note: Python 3.5 had been supported for some time. The change here only makes the documentation accurately reflect that 3.5 is not supported.

v1.1.0 / 2023-01-01
-------------------

  * chore(version): bump minor v1.1.0
  * Switch to Python >= 3.5 and fix latest aiohttp compatability (#83)
  * fix: remove print call (#81)

v1.0.2 / 2021-09-10
-------------------

  * fix(urllib3): interceptor is never really disabled (#68)
  * Closes #75 Re consider @fluent decorator (#76)
  * fix(#69): use match keyword in pytest.raises
  * fix(History): invalid rst syntax

v1.0.1 / 2020-03-24
-------------------

  * fix(aiohttp): compatible with non aiohttp projects (#67)
  * feat(History): add release changes

v1.0.0 / 2020-03-18
-------------------

  * fix(aiohttp): use latest version, allow Python 3.5+ for async http client

v0.2.8 / 2019-10-31
-------------------

  * fix collections import warning (#61)

v0.2.7 / 2019-10-21
-------------------

  * fix collections import warning (#61)

v0.2.6 / 2019-02-01
-------------------

  * Add mock.reply(new_response=True) to reset response definition object

v0.2.5 / 2017-10-19
-------------------

  * refactor(setup): remove extra install dependency
  * Fix py27 compatibility (#49)
  * Add activate_async decorator (#48)
  * fix typo in pook.mock.Mock.ismatched.__doc__ (#47)
  * fix README example (#46)

v0.2.4 / 2017-10-03
-------------------

* fix(#45): regex URL issue
* fix(travis): allow failures in pypy
* feat(docs): add sponsor banner
* refactor(History): normalize style

v0.2.3 / 2017-04-28
-------------------

* feat(docs): add supported version for aiohttp
* Merge branch 'master' of https://github.com/h2non/pook
* fix(api): export missing symbol "disable_network"
* Update README.rst (#43)

v0.2.2 / 2017-04-03
-------------------

* refactor(compare): disable maxDiff length limit while comparing values

v0.2.1 / 2017-03-25
-------------------

* fix(engine): enable new mock engine on register if needed
* fix(engine): remove activate argument before instantiating the Mock

v0.2.0 / 2017-03-18
-------------------

* refactor(engine): do not activate engine on mock declaration if not explicitly requested. This introduces a behavioral library change: you must explicitly use ``pook.on()`` to enable `pook` mock engine.

v0.1.14 / 2017-03-17
--------------------

* feat(docs): list supported HTTP client versions
* fix(#41): disable mocks after decorator call invokation
* feat(examples): add mock context manager example file
* feat(#40): support context manager definitions
* feat(#39): improve unmatched request output
* feat(docs): add mocket example file
* feat(#33): add mocket examples and documentation

v0.1.13 / 2017-01-29
--------------------

* fix(api): `mock.calls` property should be an `int`.

v0.1.12 / 2017-01-28
--------------------

* feat(#33): proxy mock definitions into mock.Request
* refactor(api): `pook.unmatched_requests()` now returns a `list` instead of a lazy `tuple`.

v0.1.11 / 2017-01-14
--------------------

* refactor(query)
* fix(#37): fix URL comparison
* fix(#38): proper mock engine interface validation.

v0.1.10 / 2017-01-13
--------------------

* fix(#37): decode byte bodies
* feat(setup.py): add author email

v0.1.9 / 2017-01-06
-------------------

* fix(Makefile): remove proper egg file
* feat(package): add wheel package distribution support
* feat(docs): add documentation links

v0.1.8 / 2016-12-24
-------------------

* fix(assertion): extract regex pattern only when required
* feat(examples): add regular expression example

v0.1.7 / 2016-12-18
-------------------

* feat(#33): add support for user defined custom mock engine

v0.1.6 / 2016-12-14
-------------------

* fix(setup.py): force utf-8 encoding
* feat(setup.py): add encoding header
* feat(api): add debug mode
* refactor(docs): minor enhancements
* refactor(tests): update URL matcher test cases
* refactor(docs): add note about HTTP clients and update features list
* fix(setup.py): remove encoding param
* fix(tests): use strict equality assertion

0.1.5 / 2016-12-12
------------------

* fix(matchers): fix matching issue in URL.
* refactor(assertion): regex expression based matching must be explicitly enabled.
* feat(tests): add initial matchers tests.

0.1.4 / 2016-12-08
------------------

* refactor(README): minor changes
* fix(setup.py): lint error
* fix(#32): use explicit encoding while reading files in setup.py

0.1.3 / 2016-12-08
------------------

* fix(core): several bug fixes.
* feat(core): add pending features and major refactors.
* feat(matchers): use ``unittest.TestCase`` matching engine by default.

0.1.2 / 2016-12-01
------------------

* fix(matchers): runtime missing variable.

0.1.1 / 2016-12-01
------------------

* fix: Python 2 dictionary iteration syntax.
* feat(docs): add more examples.
* fix(matchers): better regular expression comparison support.

0.1.0 / 2016-11-30
------------------

* First version (still beta)

0.1.0-rc.1 / 2016-11-27
-----------------------

* First release candidate version (still beta)
