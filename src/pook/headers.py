try:
    from collections.abc import Mapping, MutableMapping
except ImportError:
    from collections.abc import Mapping, MutableMapping


class HTTPHeaderDict(MutableMapping):
    """
    :param headers:
        An iterable of field-value pairs. Must not contain multiple field names
        when compared case-insensitively.
    :param kwargs:
        Additional field-value pairs to pass in to ``dict.update``.

    A ``dict`` like container for storing HTTP Headers.
    Field names are stored and compared case-insensitively in compliance with
    RFC 7230. Iteration provides the first case-sensitive key seen for each
    case-insensitive pair.
    Using ``__setitem__`` syntax overwrites fields that compare equal
    case-insensitively in order to maintain ``dict``'s api. For fields that
    compare equal, instead create a new ``HTTPHeaderDict`` and use ``.add``
    in a loop.
    If multiple fields that are equal case-insensitively are passed to the
    constructor or ``.update``, the behavior is undefined and some will be
    lost.

    Usage::

        headers = HTTPHeaderDict()
        headers.add('Set-Cookie', 'foo=bar')
        headers.add('set-cookie', 'baz=quxx')
        headers['content-length'] = '7'
        headers['SET-cookie']
        > 'foo=bar, baz=quxx'
        headers['Content-Length']
        > '7'
    """

    def __init__(self, headers=None, **kwargs):
        super(HTTPHeaderDict, self).__init__()
        self._container = {}
        if headers is not None:
            if isinstance(headers, HTTPHeaderDict):
                self._copy_from(headers)
            else:
                self.extend(headers)
        if kwargs:
            self.extend(kwargs)

    def __setitem__(self, key, val):
        self._container[key.lower()] = (key, val)
        return self._container[key.lower()]

    def __getitem__(self, key):
        val = self._container[key.lower()]
        return ", ".join([to_string_value(v) for v in val[1:]])

    def __delitem__(self, key):
        del self._container[key.lower()]

    def __contains__(self, key):
        return key.lower() in self._container

    def __eq__(self, other):
        if not isinstance(other, Mapping) and not hasattr(other, "keys"):
            return False
        if not isinstance(other, type(self)):
            other = type(self)(other)
        return dict((k.lower(), v) for k, v in self.itermerged()) == dict(
            (k.lower(), v) for k, v in other.itermerged()
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    __marker = object()

    def __len__(self):
        return len(self._container)

    def __iter__(self):
        # Only provide the originally cased names
        for vals in self._container.values():
            yield vals[0]

    def pop(self, key, default=__marker):
        """
        D.pop(k[,d]) -> v, remove specified key and return the
        corresponding value.
        If key is not found, d is returned if given, otherwise KeyError
        is raised.
        """
        # Using the MutableMapping function directly fails due to the
        # private marker. Using ordinary dict.pop would expose the
        # internal structures. So let's reinvent the wheel.
        try:
            value = self[key]
        except KeyError:
            if default is self.__marker:
                raise
            return default
        else:
            del self[key]
            return value

    def discard(self, key):
        try:
            del self[key]
        except KeyError:
            pass

    def add(self, key, val):
        """
        Adds a (name, value) pair, doesn't overwrite the value if it already
        exists.

        Usage::

            headers = HTTPHeaderDict(foo='bar')
            headers.add('Foo', 'baz')
            headers['foo']
            > 'bar, baz'
        """
        key_lower = key.lower()
        new_vals = key, val
        # Keep the common case aka no item present as fast as possible
        vals = self._container.setdefault(key_lower, new_vals)
        if new_vals is not vals:
            # new_vals was not inserted, as there was a previous one
            if isinstance(vals, list):
                # If already several items got inserted, we have a list
                vals.append(val)
            else:
                # vals should be a tuple then, i.e. only one item so far
                # Need to convert the tuple to list for further extension
                self._container[key_lower] = [vals[0], vals[1], val]

    def set(self, key, val):
        """
        Sets a header field with the given value, removing
        previous values.

        Usage::

            headers = HTTPHeaderDict(foo='bar')
            headers.set('Foo', 'baz')
            headers['foo']
            > 'baz'
        """
        key_lower = key.lower()
        new_vals = key, val
        # Keep the common case aka no item present as fast as possible
        vals = self._container.setdefault(key_lower, new_vals)
        if new_vals is not vals:
            self._container[key_lower] = [vals[0], vals[1], val]

    def extend(self, mapping, **kwargs):
        """
        Generic import function for any type of header-like object.
        Adapted version of MutableMapping.update in order to insert items
        with self.add instead of self.__setitem__
        """
        if isinstance(mapping, HTTPHeaderDict):
            for key, val in mapping.iteritems():
                self.add(key, val)
        elif isinstance(mapping, Mapping):
            for key in mapping:
                self.add(key, mapping[key])
        elif hasattr(mapping, "keys"):
            for key in mapping.keys():
                self.add(key, mapping[key])
        else:
            for key, value in mapping:
                self.add(key, value)

        for key, value in kwargs.items():
            self.add(key, value)

    def getlist(self, key):
        """
        Returns a list of all the values for the named field.
        Returns an empty list if the key doesn't exist.
        """
        try:
            vals = self._container[key.lower()]
        except KeyError:
            return []
        else:
            if isinstance(vals, tuple):
                return [vals[1]]
            else:
                return vals[1:]

    # Backwards compatibility for httplib
    getheaders = getlist
    getallmatchingheaders = getlist
    iget = getlist

    def __repr__(self):
        return "%s(%s)" % (type(self).__name__, dict(self.itermerged()))

    def _copy_from(self, other):
        for key in other:
            val = other.getlist(key)
            if isinstance(val, list):
                # Don't need to convert tuples
                val = list(val)
            self._container[key.lower()] = [key] + val

    def copy(self):
        clone = type(self)()
        clone._copy_from(self)
        return clone

    def iteritems(self):
        """
        Iterate over all header lines, including duplicate ones.
        """
        for key in self:
            vals = self._container[key.lower()]
            for val in vals[1:]:
                yield vals[0], val

    def itermerged(self):
        """
        Iterate over all headers, merging duplicate ones together.
        """
        for key in self:
            val = self._container[key.lower()]
            yield val[0], ", ".join([to_string_value(v) for v in val[1:]])

    def items(self):
        return list(self.iteritems())

    def to_dict(self):
        return {key: values for key, values in self.items()}


def to_string_value(value):
    """
    Retrieve a string value for an arbitrary value.

    HTTP header values are specified as ASCII strings. However,
    the specificiation also states that non-ASCII bytes should be
    treated as arbitrary data. In that case, we just rely on unicode
    escaping to return a value that at least somewhat resembles the
    inputs (at least moreso than other encodings that would significantly
    obscure the input, like base 64).

    Arguments::
        value (mixed):
            The value to cast to ``str``.

    Returns::
        str:
            Unicode escaped ``value`` if it was ``bytes``; otherwise,
            ``value`` is returned, cast through ``str``.
    """
    if hasattr(value, "decode"):
        return value.decode("unicode_escape")

    return str(value)
