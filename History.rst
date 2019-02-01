

History
=======

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
