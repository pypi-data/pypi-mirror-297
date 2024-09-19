========
datahold
========

Overview
--------

Wrap common mutable datastructures for inheritance with modification.

Content
-------

HoldABC
~~~~~~~

.. code-block:: python

    class HoldABC(abc.ABC):
        @abc.abstractmethod
        def __init__(self, *args, **kwargs) -> None: ...

        @property
        @abc.abstractmethod
        def data(self): ...

HoldList
~~~~~~~~

To understand the class ``HoldList`` here the beginning of its code:

.. code-block:: python

    class HoldList(HoldABC):

        data: list

        @functools.wraps(list.__add__)
        def __add__(self, *args, **kwargs):
            data = self.data
            ans = data.__add__(*args, **kwargs)
            self.data = data
            return ans

The following methods are defined this way:
``__add__``, ``__contains__``, ``__delitem__``, ``__eq__``, ``__format__``, ``__ge__``, ``__getitem__``, ``__gt__``, ``__hash__``, ``__iadd__``, ``__imul__``, ``__iter__``, ``__le__``, ``__len__``, ``__lt__``, ``__mul__``, ``__repr__``, ``__reversed__``, ``__rmul__``, ``__setitem__``, ``__str__``, ``append``, ``clear``, ``copy``, ``count``, ``extend``, ``index``, ``insert``, ``pop``, ``remove``, ``reverse``, ``sort``.

The only function present in ``list`` and absent in ``HoldList`` is ``__class_getitem__``

We can use ``HoldList`` as parent for a list-like class. It is necessary to implement in the subclass:

* a property named ``data``
* the ``__init__`` magic method

This allows the creatation of a list-like class with modified behaviour with only minimal effort. To enhance perpormance we can overwrite some of the methods.

HoldDict
~~~~~~~~

Just like ``HoldList`` but for dict...
The following methods are implemented: ``__contains__``, ``__delitem__``, ``__eq__``, ``__format__``, ``__ge__``, ``__getitem__``, ``__gt__``, ``__hash__``, ``__ior__``, ``__iter__``, ``__le__``, ``__len__``, ``__lt__``, ``__or__``, ``__repr__``, ``__reversed__``, ``__ror__``, ``__setitem__``, ``__str__``, ``clear``, ``copy``, ``get``, ``items``, ``keys``, ``pop``, ``popitem``, ``setdefault``, ``update``, ``values``.
The classmethods ``__class_getitem__`` and ``fromkeys`` are not implemented.


HoldSet
~~~~~~~

Just like ``HoldSet`` but for set...
The following methods are implemented: ``__and__``, ``__contains__``, ``__eq__``, ``__format__``, ``__ge__``, ``__gt__``, ``__hash__``, ``__iand__``, ``__ior__``, ``__isub__``, ``__iter__``, ``__ixor__``, ``__le__``, ``__len__``, ``__lt__``, ``__or__``, ``__rand__``, ``__repr__``, ``__ror__``, ``__rsub__``, ``__rxor__``, ``__str__``, ``__sub__``, ``__xor__``, ``add``, ``clear``, ``copy``, ``difference``, ``difference_update``, ``discard``, ``intersection``, ``intersection_update``, ``isdisjoint``, ``issubset``, ``issuperset``, ``pop``, ``remove``, ``symmetric_difference``, ``symmetric_difference_update``, ``union``, ``update``.
The classmethod ``__class_getitem__`` is not implemented.

OkayABC
~~~~~~~

A common abc (child of ``HoldABC`` and `scaevola.Scaevola <https://pypi.org/project/datahold/>`_) for ``OkayList``, ``OkayDict``, and ``OkaySet``. It implements common sense overwrites for some methods. For example:

* all methods that cannot actually change the underlying object are now bound to ``_data`` instead of data
* ``__bool__`` is implemented as bool(self._data) because neither ``list``, ``dict``, nor ``set`` have a ``__bool__`` method defined.
* ``__hash__`` raises now a more fitting exception
* the comparison operations are overwritten:

  + ``__eq__`` returns self._data == type(self._data)(other)
  + ``__ne__`` negates ``__eq__``
  + ``__ge__`` returns ``type(self)(other) <= self`` (inherited from ``scaevola.Scaevola``)
  + ``__gt__`` returns ``not (self == other) and (self >= other)``
  + ``__lt__`` returns ``not (self == other) and (self <= other)``
  + ``__le__`` returns ``self._data <= type(self)(other)._data``
  + modify ``__eq__`` or ``__le__`` as needed to change the behaviour of the other comparison methods

OkayList
~~~~~~~~

This class inherits from ``HoldList`` and ``OkayABC``. It implements a ``data`` property that binds a variable ``_data``.

.. code-block:: python

    @property
    def data(self, /):
        return list(self._data)

    @data.setter
    def data(self, values, /):
        self._data = list(values)

    @data.deleter
    def data(self, /):
        self._data = list()

Based on that it implements common sense methods. For example:

* all methods that returned a list before now return ``OkayList`` (type adapts to further inheritance)
* ``__init__`` allows now to set data immediately

OkayDict
~~~~~~~~

A subclass of ``HoldDict`` with common sense implementations for further inheritance just like ``OkayList`` for ``HoldList``.

OkaySet
~~~~~~~

A subclass of ``HoldSet`` with common sense implementations for further inheritance just like ``OkayList`` for ``HoldList``.

Installation
------------

To install ``datahold``, you can use ``pip``. Open your terminal and run:

.. code-block:: bash

    pip install datahold

License
-------

This project is licensed under the MIT License.

Links
-----

* `Documentation <https://pypi.org/project/datahold/>`_
* `Download <https://pypi.org/project/datahold/#files>`_
* `Source <https://github.com/johannes-programming/datahold>`_

Credits
-------

* Author: `Johannes <http://johannes-programming.website>`_
* Email: `johannes-programming@mailfence.com <mailto:johannes-programming@mailfence.com>`_

Thank you for using ``datahold``!