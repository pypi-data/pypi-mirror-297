import inspect
import math
import sys
import time
from collections import defaultdict
from contextlib import contextmanager
from dataclasses import dataclass, field
from functools import wraps
from typing import Callable
from unittest import TestCase

HEADERS = ['label', 'total (s)', 'time (%)', 'count', 'min', 'max', 'mean', 'std']
TOTAL_TIME = '__total_time__'
NOT_MEASURED = '__not-measured__'


def _tabulate(headers: list[str], data: list[list[str]]):
    try:
        from tabulate import tabulate
        return tabulate(
            headers=headers,
            floatfmt='.5f',
            tabular_data=data,
        )
    except:
        pass

    def _format(val: str | float):
        if isinstance(val, float | int):
            return f'{val:.5f}'
        return val

    raw = [
        headers,
        *[
            list(map(_format, row))
            for row in data
        ]
    ]

    lengths = [
        max(len(raw[row][col]) for row in range(len(raw)))
        for col in range(len(headers))
    ]

    raw.insert(1, ['-' * _ for _ in lengths])

    return '\n'.join([
        '   '.join([_.rjust(l) for _, l in zip(row, lengths)])
        for row in raw
    ])


@dataclass
class TimeEntry:
    events: list[float] = field(default_factory=list)
    processed: int = 0
    values: dict[str, float] = field(default_factory=dict)

    def compress(self):
        if not self.events:
            return
        self.values = {
            'sum': self.values.get('sum', 0) + sum(self.events),
            'square_sum': self.values.get('square_sum', 0) + sum([_ * _ for _ in self.events]),
            'count': self.values.get('count', 0) + len(self.events),
            'min': min([self.values.get('min', sys.float_info.max), *self.events]),
            'max': max([self.values.get('max', sys.float_info.min), *self.events]),
        }
        self.events = []

    def raw_line(self, key: str, total_time: float):
        self.compress()
        return [
            key,
            self.values['sum'],
            100 * self.values['sum'] / total_time,
            self.values['count'],
            self.values['min'],
            self.values['max'],
            self.mean,
            self.std
        ]

    @property
    def total(self):
        self.compress()
        return self.values['sum']

    @property
    def count(self):
        self.compress()
        return self.values['count']

    @property
    def mean(self):
        self.compress()
        return self.values['sum'] / max(1., self.count)

    @property
    def std(self):
        self.compress()
        s1 = self.values['sum']
        s2 = self.values['square_sum']
        n = self.values['count']
        if n == 0:
            return 0.
        res = math.sqrt(s2 / n - (s1 / n) ** 2)
        return res

    def _undefined(self, value: float):
        if len(self.events) <= 1:
            return ''
        return value


class DefaultLogger:
    debug = print
    info = print
    warning = print


class Timings:
    def __init__(self):
        self.event_per_entry_limit = 100
        self.db: dict[str, TimeEntry] = defaultdict(lambda: TimeEntry())
        self.active = False
        self.logs = False
        self.logger = DefaultLogger
        self.start_time: float = None
        try:
            from loguru import logger
            self.logger = logger
        except:
            pass

    @contextmanager
    def timing(self, name: str = None):
        if name is None:
            name = inspect.stack()[11].function
        start = self._before(name)
        yield
        self._after(name, start)

    def time_func[** P, R](self, func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def inner(*args: P.args, **kwargs: P.kwargs) -> R:
            with self.timing(func.__qualname__):
                return func(*args, **kwargs)

        return inner

    def show_timing(self):
        if not self.active:
            return
        try:
            self.logger.info('\n' + self.format_table())
        except Exception as e:
            self.logger.warning(f'Warning: {e}')

    def raw_table(self):
        total_time = time.time() - self.start_time
        unmeasured = sum([_.total for _ in self.db.values()])

        return list(sorted([
            [
                TOTAL_TIME, total_time, 100, 1, total_time, total_time, total_time, 0.
            ], [
                NOT_MEASURED, unmeasured, 100 * unmeasured / total_time, 1, unmeasured, unmeasured, unmeasured, 0.
            ],
            *[
                entry.raw_line(key, total_time)
                for key, entry in self.db.items()
            ]
        ], key=lambda row: row[1], reverse=True))

    def format_table(self):
        return _tabulate(headers=HEADERS, data=self.raw_table())

    def setup_timing(self, status: bool = True, logs: bool = False):
        self.active = status
        self.logs = logs
        self.start_time = time.time()

    def tree_structure(self):
        groups = {}

        for key, entry in self.db.items():
            try:
                major, minor = key.split('.', maxsplit=1)
            except:
                major = '___'
                minor = key
            if major not in groups:
                groups[major] = {}
            groups[major][minor] = entry
        return groups

    def _before(self, name: str):
        if self.logs:
            self.logger.debug(f'+ {name}')
        if self.active:
            return time.time()

    def _after(self, name: str, start: float | None):
        if self.logs:
            self.logger.debug(f'- {name}')
        if start is not None:
            total = time.time() - start
            self.db[name].events.append(total)
            if len(self.db[name].events) >= self.event_per_entry_limit:
                self.db[name].compress()


_TIMING = Timings()
timing = _TIMING.timing
time_func = _TIMING.time_func
show_timing = _TIMING.show_timing
setup_timing = _TIMING.setup_timing


class TimingTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        setup_timing()

    @classmethod
    def tearDownClass(cls):
        show_timing()
