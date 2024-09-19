from __future__ import annotations
from abc import ABC, abstractmethod
from functools import wraps, reduce, partial
from collections import OrderedDict
from typing import Callable, TypeVar, Iterable, Optional, Iterator, Any, Tuple, Type
from itertools import chain
from concurrent.futures import ThreadPoolExecutor, Executor, ProcessPoolExecutor
from multiprocessing import cpu_count

__all__ = [
    "Predicate", "Supplier", "Consumer", "BiConsumer", "Function", "BiFunction", "BinaryOperator", "Stream"
]

T = TypeVar("T")
R = TypeVar("R")
U = TypeVar("U")

E = TypeVar("E")

Predicate = Callable[[T], bool]
Supplier = Callable[[], T]
Consumer = Callable[[T], None]
BiConsumer = Callable[[T, R], None]
Function = Callable[[T], R]
BiFunction = Callable[[U, T], U]
BinaryOperator = Callable[[T, T], T]

class _buffer(Iterable[T]):
    def __init__(self, t: Optional[T | Iterable[T] | Supplier[Iterable[T]]] = None) -> None:
        if isinstance(t, Iterable):
            self._data = t
        elif callable(t):
            self._data = t
        else:
            self._data = [] if t is None else [t]

    @property
    def data(self) -> Iterable[T] | Supplier[Iterable[T]]:
        return self._data

    def __iter__(self) -> Iterator[T]:
        yield from self._data() if callable(self._data) else self._data

def try_catch(
    ignored: Type[Exception] | Tuple[Type[Exception], ...] = Exception,
    ret_val: Optional[T] = None
) -> Callable[..., Optional[T]]:
    def _wrapper(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def _decorator(*args: Any, **kwargs: Any) -> Optional[T]:
            # noinspection PyBroadException
            try:
                return func(*args, **kwargs)
            except ignored:
                return ret_val
        return _decorator
    return _wrapper

def get_executor(size: Optional[int] = None, **kwargs: Any) -> Executor:
    executor = ThreadPoolExecutor if kwargs.pop("io_intensive", True) else ProcessPoolExecutor
    return executor(max_workers=size or cpu_count(), **kwargs)

def concurrent_map(func: Function[T, R], *iterables: T | Iterable[T], **kwargs: Any) -> Iterable[R]:
    with get_executor(**kwargs) as executor:
        return executor.map(func, *iterables)

def eval_map(func: Function[T, R], *iterables: T | Iterable[T]) -> Iterable[R]:
    return tuple(map(func, *iterables))

class Stream(Iterable[E], ABC):
    """A sequence of elements supporting sequential and parallel aggregate operations.

    Using cases:
        >>> import os.path
        >>> import requests
        >>> from bs4 import BeautifulSoup
        >>>
        >>> def download(url: str, out: str) -> bool:
        >>>     os.makedirs(out, exist_ok=True)
        >>>     with open(os.path.join(out, os.path.basename(url)), "wb") as fp:
        >>>         try:
        >>>             resp = requests.get(url)
        >>>             assert resp.status_code == 200
        >>>             assert resp.content.strip() != ""
        >>>             fp.write(resp.content)
        >>>             return True
        >>>         except (AssertionError, requests.RequestException):
        >>>             return False
        >>>
        >>> (Stream.of(range(2))
        >>> .map(lambda e: f"https://wallhaven.cc/toplist?page={e}")
        >>> .map(lambda e: requests.get(e), parallel=True)
        >>> .filter(lambda e: e.status_code == 200)
        >>> .map(lambda e: BeautifulSoup(e.text, features="html.parser"))
        >>> .flat_map(lambda e: e.select("#thumbs > section > ul > li > figure > a"))
        >>> .map(lambda e: requests.get(e["href"]), parallel=True)
        >>> .filter(lambda e: e.status_code == 200)
        >>> .map(lambda e: BeautifulSoup(e.text, features="html.parser"))
        >>> .map(lambda e: e.select_one("#wallpaper")["src"])
        >>> .peek(print)
        >>> .foreach(partial(download, out="wallpapers"), parallel=True))

        Here, we shown you a example of crawlling wallpapers from wallhaven.cc in a Stream manner, where you can see that
        a Stream can be clear to describe the data flow and not a consideration about the complicated hidden variables.
        And, there are also embedded the concurrent handling for speeding-up io processes and cpu calculations.
    """

    @staticmethod
    def of(
        e: Optional[E | Iterable[E] | Supplier[E] | Supplier[Iterable[E]]] = None,
        **kwargs: Any
    ) -> Stream[E]:
        """
        Returns a sequential ordered stream whose elements are the specified values.
        """
        return StreamImpl(e, **kwargs)

    @staticmethod
    def concat(a: Stream[E], b: Stream[E]) -> Stream[E]:
        return StreamImpl(lambda: chain.from_iterable((a, b)))

    @abstractmethod
    def all_match(self, predicate: Predicate[E]) -> bool:
        """
        Returns whether all elements of this stream match the provided predicate.
        """
        raise NotImplementedError("all_match")

    @abstractmethod
    def any_match(self, predicate: Predicate[E]) -> bool:
        """
        Returns whether any elements of this stream match the provided predicate.
        """
        raise NotImplementedError("any_match")

    @abstractmethod
    def collect(self, supplier: Supplier[R], accumulator: BiConsumer[R, E]) -> R:
        """
        Performs a mutable reduction operation on the elements of this stream using a Collector.
        """
        raise NotImplementedError("collect")

    @abstractmethod
    def count(self) -> int:
        """
        Returns the count of elements in this stream.
        """
        raise NotImplementedError("count")

    @abstractmethod
    def distinct(self) -> Stream[E]:
        """
        Returns a stream consisting of the distinct elements (according to __eq__) of this stream.
        """
        raise NotImplementedError("distinct")

    @abstractmethod
    def filter(self, predicate: Predicate[E]) -> Stream[E]:
        """
        Returns a stream consisting of the elements of this stream that match the given predicate.
        """
        raise NotImplementedError("filter")

    @abstractmethod
    def find_any(self, predicate: Predicate[E]) -> Optional[E]:
        """
        Returns an Optional describing some element of the stream, or an empty Optional if the stream is empty.
        """
        raise NotImplementedError("find_any")

    @abstractmethod
    def find_first(self) -> Optional[E]:
        """
        Returns an Optional describing the first element of this stream, or an empty Optional if the stream is empty.
        """
        raise NotImplementedError("find_first")

    @abstractmethod
    def flat_map(self, mapper: Function[E, Iterable[R]], parallel: bool = False, **kwargs: Any) -> Stream[R]:
        """
        Returns a stream consisting of the results of replacing each element of this stream with the contents of a mapped
        stream produced by applying the provided mapping function to each element.
        """
        raise NotImplementedError("flat_map")

    @abstractmethod
    def foreach(self, action: Consumer[E], parallel: bool = False, **kwargs: Any) -> None:
        """
        Performs an action for each element of this stream.
        """
        raise NotImplementedError("foreach")

    @abstractmethod
    def limit(self, max_size: int) -> Stream[E]:
        """
        Returns a stream consisting of the elements of this stream, truncated to be no longer than maxSize in length.
        """
        raise NotImplementedError("limit")

    @abstractmethod
    def map(self, mapper: Function[E, R], parallel: bool = False, **kwargs: Any) -> Stream[R]:
        """
        Returns a stream consisting of the results of applying the given function to the elements of this stream.
        """
        raise NotImplementedError("")

    @abstractmethod
    def max(self, key: Optional[Function[E, R]] = None) -> Optional[E]:
        """
        Returns the maximum element of this stream according to the provided key.
        """
        raise NotImplementedError("max")

    @abstractmethod
    def min(self, key: Optional[Function[E, R]] = None) -> Optional[E]:
        """
        Returns the minimum element of this stream according to the provided key.
        """
        raise NotImplementedError("min")

    @abstractmethod
    def none_match(self, predicate: Predicate[E]) -> bool:
        """
        Returns whether no elements of this stream match the provided predicate.
        """
        raise NotImplementedError("none_match")

    @abstractmethod
    def peek(self, action: Consumer[E], parallel: bool = False, **kwargs: Any) -> Stream[E]:
        """
        Returns a stream consisting of the elements of this stream, additionally performing the provided action on each
        element as elements are consumed from the resulting stream.
        """
        raise NotImplementedError("peek")

    @abstractmethod
    def reduce(self, e: E, accumulator: BinaryOperator[E]) -> Optional[E]:
        """
        Performs a reduction on the elements of this stream, using an associative accumulation function, and returns an
        Optional describing the reduced value, if any.
        """
        raise NotImplementedError("reduce")

    @abstractmethod
    def skip(self, n: int) -> Stream[E]:
        """
        Returns a stream consisting of the remaining elements of this stream after discarding the first n elements of the stream.
        """
        raise NotImplementedError("skip")

    @abstractmethod
    def sorted(self, key: Optional[Function[E, R]] = None, ascending: bool = True) -> Stream[E]:
        """
        Returns a stream consisting of the elements of this stream, sorted according to key.
        """
        raise NotImplementedError("sorted")

class StreamImpl(Stream[E]):
    def __init__(
        self,
        e: Optional[E | Iterable[E] | Supplier[E] | Supplier[Iterable[E]]] = None,
        parallel: bool = False
    ) -> None:
        super(StreamImpl, self).__init__()
        self._data = _buffer(e)
        self.parallel = parallel

    def __iter__(self) -> Iterator[E]:
        yield from self._data

    def all_match(self, predicate: Predicate[E]) -> bool:
        return all(map(predicate, self._data))

    def any_match(self, predicate: Predicate[E]) -> bool:
        return any(map(predicate, self._data))

    def collect(self, supplier: Supplier[R], accumulator: BiConsumer[R, E]) -> R:
        container = supplier()
        eval_map(lambda e: accumulator(container, e), self._data)
        return container

    def count(self) -> int:
        if hasattr(self._data.data, "__len__"):
            return getattr(self._data.data, "__len__")()
        return len(tuple(self._data))

    def distinct(self) -> Stream[E]:
        return StreamImpl(lambda: OrderedDict.fromkeys(self._data))

    def filter(self, predicate: Predicate[E]) -> Stream[E]:
        return StreamImpl(filter(predicate, self._data))

    @try_catch(ignored=StopIteration, ret_val=None)
    def find_any(self, predicate: Predicate[E]) -> Optional[E]:
        return next(filter(predicate, self._data))

    @try_catch(ignored=StopIteration, ret_val=None)
    def find_first(self) -> Optional[E]:
        return next(iter(self._data))

    def flat_map(self, mapper: Function[E, Iterable[R]], parallel: bool = False, **kwargs: Any) -> Stream[R]:
        _map = partial(concurrent_map, **kwargs) if parallel or self.parallel else map
        return StreamImpl(lambda: chain.from_iterable(_map(mapper, self._data)))

    def foreach(self, action: Consumer[E], parallel: bool = False, **kwargs: Any) -> None:
        _map = partial(concurrent_map, **kwargs) if parallel or self.parallel else eval_map
        _map(action, self._data)

    def limit(self, max_size: int) -> Stream[T]:
        return StreamImpl(lambda: tuple(self._data)[:max_size])

    def map(self, mapper: Function[E, R], parallel: bool = False, **kwargs: Any) -> Stream[R]:
        _map = partial(concurrent_map, **kwargs) if parallel or self.parallel else map
        return StreamImpl(lambda: _map(mapper, self._data))

    @try_catch(ignored=(ValueError, StopIteration), ret_val=None)
    def max(self, key: Optional[Function[E, R]] = None) -> Optional[E]:
        return max(self._data, key=key)

    @try_catch(ignored=(ValueError, StopIteration), ret_val=None)
    def min(self, key: Optional[Function[E, R]] = None) -> Optional[E]:
        return min(self._data, key=key)

    def none_match(self, predicate: Predicate[E]) -> bool:
        return not any(map(predicate, self._data))

    def peek(self, action: Consumer[E], parallel: bool = False, **kwargs: Any) -> Stream[E]:
        def _action(e: E) -> E:
            action(e)
            return e

        _map = partial(concurrent_map, **kwargs) if parallel or self.parallel else eval_map
        return StreamImpl(_map(_action, self._data))

    @try_catch(ignored=(TypeError, StopIteration), ret_val=None)
    def reduce(self, accumulator: BinaryOperator[E], e: Optional[E] = None) -> Optional[E]:
        return reduce(accumulator, self._data, initial=e or object())

    def skip(self, n: int) -> Stream[E]:
        return StreamImpl(filter(lambda args: args[0] != n, enumerate(self._data)))

    def sorted(self, key: Optional[Function[E, R]] = None, ascending: bool = True) -> Stream[E]:
        return StreamImpl(lambda: sorted(self._data, key=key, reverse=not ascending))
