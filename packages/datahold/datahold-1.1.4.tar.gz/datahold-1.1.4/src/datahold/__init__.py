import functools
from abc import ABC, abstractmethod
from collections import abc
from typing import *

from protectedclasses import Protected
from scaevola import Scaevola

__all__ = [
    "HoldABC",
    "HoldDict",
    "HoldList",
    "HoldSet",
    "OkayABC",
    "OkayDict",
    "OkayList",
    "OkaySet",
]


class HoldABC(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs) -> None: ...

    @property
    @abstractmethod
    def data(self): ...


class HoldDict(HoldABC, abc.MutableMapping):

    data: dict

    @functools.wraps(dict.__contains__)
    def __contains__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__contains__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.__delitem__)
    def __delitem__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__delitem__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.__eq__)
    def __eq__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__eq__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.__format__)
    def __format__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__format__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.__ge__)
    def __ge__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__ge__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.__getitem__)
    def __getitem__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__getitem__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.__gt__)
    def __gt__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__gt__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.__hash__)
    def __hash__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__hash__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.__ior__)
    def __ior__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__ior__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.__iter__)
    def __iter__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__iter__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.__le__)
    def __le__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__le__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.__len__)
    def __len__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__len__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.__lt__)
    def __lt__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__lt__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.__or__)
    def __or__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__or__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.__repr__)
    def __repr__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__repr__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.__reversed__)
    def __reversed__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__reversed__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.__ror__)
    def __ror__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__ror__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.__setitem__)
    def __setitem__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__setitem__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.__str__)
    def __str__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__str__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.clear)
    def clear(self, /, *args, **kwargs):
        data = self.data
        ans = data.clear(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.copy)
    def copy(self, /, *args, **kwargs):
        data = self.data
        ans = data.copy(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.get)
    def get(self, /, *args, **kwargs):
        data = self.data
        ans = data.get(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.items)
    def items(self, /, *args, **kwargs):
        data = self.data
        ans = data.items(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.keys)
    def keys(self, /, *args, **kwargs):
        data = self.data
        ans = data.keys(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.pop)
    def pop(self, /, *args, **kwargs):
        data = self.data
        ans = data.pop(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.popitem)
    def popitem(self, /, *args, **kwargs):
        data = self.data
        ans = data.popitem(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.setdefault)
    def setdefault(self, /, *args, **kwargs):
        data = self.data
        ans = data.setdefault(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.update)
    def update(self, /, *args, **kwargs):
        data = self.data
        ans = data.update(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(dict.values)
    def values(self, /, *args, **kwargs):
        data = self.data
        ans = data.values(*args, **kwargs)
        self.data = data
        return ans


class HoldList(HoldABC, abc.MutableSequence):

    data: list

    @functools.wraps(list.__add__)
    def __add__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__add__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__contains__)
    def __contains__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__contains__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__delitem__)
    def __delitem__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__delitem__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__eq__)
    def __eq__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__eq__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__format__)
    def __format__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__format__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__ge__)
    def __ge__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__ge__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__getitem__)
    def __getitem__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__getitem__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__gt__)
    def __gt__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__gt__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__hash__)
    def __hash__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__hash__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__iadd__)
    def __iadd__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__iadd__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__imul__)
    def __imul__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__imul__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__iter__)
    def __iter__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__iter__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__le__)
    def __le__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__le__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__len__)
    def __len__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__len__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__lt__)
    def __lt__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__lt__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__mul__)
    def __mul__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__mul__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__repr__)
    def __repr__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__repr__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__reversed__)
    def __reversed__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__reversed__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__rmul__)
    def __rmul__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__rmul__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__setitem__)
    def __setitem__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__setitem__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.__str__)
    def __str__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__str__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.append)
    def append(self, /, *args, **kwargs):
        data = self.data
        ans = data.append(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.clear)
    def clear(self, /, *args, **kwargs):
        data = self.data
        ans = data.clear(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.copy)
    def copy(self, /, *args, **kwargs):
        data = self.data
        ans = data.copy(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.count)
    def count(self, /, *args, **kwargs):
        data = self.data
        ans = data.count(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.extend)
    def extend(self, /, *args, **kwargs):
        data = self.data
        ans = data.extend(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.index)
    def index(self, /, *args, **kwargs):
        data = self.data
        ans = data.index(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.insert)
    def insert(self, /, *args, **kwargs):
        data = self.data
        ans = data.insert(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.pop)
    def pop(self, /, *args, **kwargs):
        data = self.data
        ans = data.pop(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.remove)
    def remove(self, /, *args, **kwargs):
        data = self.data
        ans = data.remove(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.reverse)
    def reverse(self, /, *args, **kwargs):
        data = self.data
        ans = data.reverse(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(list.sort)
    def sort(self, /, *args, **kwargs):
        data = self.data
        ans = data.sort(*args, **kwargs)
        self.data = data
        return ans


class HoldSet(HoldABC, abc.MutableSet):

    data: set

    @functools.wraps(set.__and__)
    def __and__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__and__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__contains__)
    def __contains__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__contains__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__eq__)
    def __eq__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__eq__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__format__)
    def __format__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__format__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__ge__)
    def __ge__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__ge__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__gt__)
    def __gt__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__gt__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__hash__)
    def __hash__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__hash__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__iand__)
    def __iand__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__iand__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__ior__)
    def __ior__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__ior__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__isub__)
    def __isub__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__isub__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__iter__)
    def __iter__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__iter__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__ixor__)
    def __ixor__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__ixor__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__le__)
    def __le__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__le__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__len__)
    def __len__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__len__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__lt__)
    def __lt__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__lt__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__or__)
    def __or__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__or__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__rand__)
    def __rand__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__rand__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__repr__)
    def __repr__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__repr__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__ror__)
    def __ror__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__ror__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__rsub__)
    def __rsub__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__rsub__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__rxor__)
    def __rxor__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__rxor__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__str__)
    def __str__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__str__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__sub__)
    def __sub__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__sub__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.__xor__)
    def __xor__(self, /, *args, **kwargs):
        data = self.data
        ans = data.__xor__(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.add)
    def add(self, /, *args, **kwargs):
        data = self.data
        ans = data.add(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.clear)
    def clear(self, /, *args, **kwargs):
        data = self.data
        ans = data.clear(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.copy)
    def copy(self, /, *args, **kwargs):
        data = self.data
        ans = data.copy(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.difference)
    def difference(self, /, *args, **kwargs):
        data = self.data
        ans = data.difference(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.difference_update)
    def difference_update(self, /, *args, **kwargs):
        data = self.data
        ans = data.difference_update(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.discard)
    def discard(self, /, *args, **kwargs):
        data = self.data
        ans = data.discard(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.intersection)
    def intersection(self, /, *args, **kwargs):
        data = self.data
        ans = data.intersection(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.intersection_update)
    def intersection_update(self, /, *args, **kwargs):
        data = self.data
        ans = data.intersection_update(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.isdisjoint)
    def isdisjoint(self, /, *args, **kwargs):
        data = self.data
        ans = data.isdisjoint(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.issubset)
    def issubset(self, /, *args, **kwargs):
        data = self.data
        ans = data.issubset(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.issuperset)
    def issuperset(self, /, *args, **kwargs):
        data = self.data
        ans = data.issuperset(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.pop)
    def pop(self, /, *args, **kwargs):
        data = self.data
        ans = data.pop(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.remove)
    def remove(self, /, *args, **kwargs):
        data = self.data
        ans = data.remove(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.symmetric_difference)
    def symmetric_difference(self, /, *args, **kwargs):
        data = self.data
        ans = data.symmetric_difference(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.symmetric_difference_update)
    def symmetric_difference_update(self, /, *args, **kwargs):
        data = self.data
        ans = data.symmetric_difference_update(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.union)
    def union(self, /, *args, **kwargs):
        data = self.data
        ans = data.union(*args, **kwargs)
        self.data = data
        return ans

    @functools.wraps(set.update)
    def update(self, /, *args, **kwargs):
        data = self.data
        ans = data.update(*args, **kwargs)
        self.data = data
        return ans


class OkayABC(Protected, Scaevola, HoldABC):

    def __bool__(self, /) -> bool:
        """Return bool(self)."""
        return bool(self._data)

    def __contains__(self, value, /) -> bool:
        """Return value in self."""
        return value in self._data

    def __eq__(self, other, /) -> bool:
        """Return self==other."""
        return self._data == type(self._data)(other)

    def __format__(self, format_spec="", /) -> str:
        """Return format(self, format_spec)."""
        return format(str(self), format_spec)

    def __getitem__(self, key, /) -> Any:
        """Return self[key]."""
        return self._data[key]

    def __gt__(self, other, /) -> bool:
        """Return self>=other."""
        return not (self == other) and (self >= other)

    def __hash__(self, /) -> int:
        """raise TypeError"""
        raise TypeError("unhashable type: %r" % type(self).__name__)

    def __iter__(self, /) -> Iterator:
        """Return iter(self)."""
        return iter(self._data)

    def __le__(self, other, /) -> bool:
        """Return self<=other."""
        return self._data <= type(self._data)(other)

    def __len__(self, /) -> int:
        """Return len(self)."""
        return len(self._data)

    def __lt__(self, other, /) -> bool:
        """Return self<other."""
        return not (self == other) and (self <= other)

    def __ne__(self, other, /) -> bool:
        """Return self!=other."""
        return not (self == other)

    def __repr__(self, /) -> str:
        """Return repr(self)."""
        return "%s(%r)" % (type(self).__name__, self._data)

    def __reversed__(self, /) -> Self:
        """Return reversed(self)."""
        return type(self)(reversed(self.data))

    def __str__(self, /) -> str:
        """Return str(self)."""
        return repr(self)

    def copy(self, /) -> Self:
        """New holder for equivalent data."""
        return type(self)(self.data)


class OkayDict(OkayABC, HoldDict):

    @functools.wraps(dict.__init__)
    def __init__(self, data, /, **kwargs) -> None:
        """Initialize self."""
        self.data = dict(data, **kwargs)

    def __or__(self, other, /) -> Self:
        """Return self|other."""
        return type(self)(self._data | dict(other))

    @property
    def data(self, /) -> dict:
        return dict(self._data)

    @data.setter
    def data(self, values, /) -> None:
        self._data = dict(values)

    @data.deleter
    def data(self, /) -> None:
        self._data = dict()

    @classmethod
    def fromkeys(cls, iterable, value=None, /) -> Self:
        """Create a new instance with keys from iterable and values set to value."""
        return cls(dict.fromkeys(iterable, value))

    @functools.wraps(dict.get)
    def get(self, /, *args) -> Any:
        return self._data.get(*args)

    @functools.wraps(dict.items)
    def items(self, /) -> abc.ItemsView:
        return self._data.items()

    @functools.wraps(dict.keys)
    def keys(self, /) -> abc.KeysView:
        return self._data.keys()

    @functools.wraps(dict.values)
    def values(self, /) -> abc.ValuesView:
        return self._data.values()


class OkayList(OkayABC, HoldList):

    def __add__(self, other, /) -> Self:
        """Return self+other."""
        return type(self)(self._data + list(other))

    def __init__(self, data=[]) -> None:
        """Initialize self."""
        self.data = data

    def __mul__(self, value, /) -> Self:
        """Return self*other."""
        return type(self)(self.data * value)

    def __rmul__(self, value, /) -> Self:
        """Return other*self."""
        return self * value

    @functools.wraps(list.count)
    def count(self, value, /) -> int:
        return self._data.count(value)

    @property
    def data(self, /) -> list:
        return list(self._data)

    @data.setter
    def data(self, values, /) -> None:
        self._data = list(values)

    @data.deleter
    def data(self, /) -> None:
        self._data = list()

    @functools.wraps(list.index)
    def index(self, /, *args) -> int:
        return self._data.index(*args)


class OkaySet(OkayABC, HoldSet):

    def __and__(self, other, /) -> Self:
        """Return self&other."""
        return type(self)(self._data & set(other))

    def __init__(self, data=set()) -> None:
        """Initialize self."""
        self.data = data

    def __or__(self, other, /) -> Self:
        """Return self|other."""
        return type(self)(self._data | set(other))

    def __sub__(self, other, /) -> Self:
        """Return self-other."""
        return type(self)(self._data - set(other))

    def __xor__(self, other, /) -> Self:
        """Return self^other."""
        return type(self)(self._data ^ set(other))

    @property
    def data(self, /) -> set:
        return set(self._data)

    @data.setter
    def data(self, values: Iterable) -> None:
        self._data = set(values)

    @data.deleter
    def data(self, /) -> None:
        self._data = set()

    @functools.wraps(set.difference)
    def difference(self, /, *args) -> Self:
        return type(self)(self._data.difference(*args))

    @functools.wraps(set.intersection)
    def intersection(self, /, *args) -> set:
        return type(self)(self._data.intersection(*args))

    @functools.wraps(set.isdisjoint)
    def isdisjoint(self, other, /) -> bool:
        return self._data.isdisjoint(other)

    @functools.wraps(set.issubset)
    def issubset(self, other, /) -> bool:
        return self._data.issubset(other)

    @functools.wraps(set.issuperset)
    def issuperset(self, other, /) -> bool:
        return self._data.issuperset(other)

    @functools.wraps(set.symmetric_difference)
    def symmetric_difference(self, other, /) -> Self:
        return type(self)(self._data.symmetric_difference(other))

    @functools.wraps(set.union)
    def union(self, /, *args) -> Self:
        return type(self)(self._data.union(*args))
