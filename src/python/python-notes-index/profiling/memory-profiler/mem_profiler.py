"""
Universal Memory Profiler

A flexible tool for profiling memory usage in Python applications.

Usage patterns:
    1. Decorator for functions/methods
    2. Context manager
    3. Explicit control via MemoryProfiler class
    4. Global profiler for application-wide tracking

Examples:
    # Decorator
    @profile_memory(every_n_calls=5, output="mem.log")
    async def process_batch(data):
        ...

    # Context manager
    with memory_snapshot("heavy operation"):
        do_something()

    # Explicit control
    profiler = MemoryProfiler(output=FileOutput("mem.log"))
    profiler.start()
    for batch in batches:
        process(batch)
        profiler.track()
    profiler.stop()
"""

from __future__ import annotations

import asyncio
import sys
import tracemalloc
from abc import ABC, abstractmethod
from contextlib import contextmanager, asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from functools import wraps
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Generic,
    ParamSpec,
    Protocol,
    TypeVar,
    overload,
)

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Iterator


__all__ = [
    "MemoryProfiler",
    "MemoryProfilerConfig",
    "profile_memory",
    "memory_snapshot",
    "async_memory_snapshot",
    "global_profiler",
    # Outputs
    "OutputBackend",
    "FileOutput",
    "LoggerOutput",
    "CallbackOutput",
    "MultiOutput",
    # Data
    "SnapshotData",
    "StatDiff",
]


P = ParamSpec("P")
R = TypeVar("R")
T = TypeVar("T")


# ============================================================================
# Tracemalloc reference counting (shared state)
# ============================================================================

_tracemalloc_refcount = 0
_tracemalloc_lock = __import__("threading").Lock()


def _tracemalloc_acquire(nframes: int = 1) -> None:
    """Increment refcount and start tracemalloc if needed."""
    global _tracemalloc_refcount
    with _tracemalloc_lock:
        if _tracemalloc_refcount == 0:
            tracemalloc.start(nframes)
        _tracemalloc_refcount += 1


def _tracemalloc_release() -> None:
    """Decrement refcount and stop tracemalloc if no more users."""
    global _tracemalloc_refcount
    with _tracemalloc_lock:
        _tracemalloc_refcount = max(0, _tracemalloc_refcount - 1)
        if _tracemalloc_refcount == 0 and tracemalloc.is_tracing():
            tracemalloc.stop()


# ============================================================================
# Data structures
# ============================================================================


class GroupBy(str, Enum):
    """Statistics grouping strategy."""

    LINENO = "lineno"  # By file and line number
    FILENAME = "filename"  # By file only
    TRACEBACK = "traceback"  # Full traceback


@dataclass(frozen=True, slots=True)
class StatDiff:
    """Memory statistics difference between snapshots."""

    filepath: str
    lineno: int
    size_diff: int  # bytes
    size_total: int  # bytes
    count_diff: int
    count_total: int

    @property
    def size_diff_kb(self) -> float:
        return self.size_diff / 1024

    @property
    def size_total_kb(self) -> float:
        return self.size_total / 1024

    @property
    def size_diff_mb(self) -> float:
        return self.size_diff / (1024 * 1024)

    @property
    def size_total_mb(self) -> float:
        return self.size_total / (1024 * 1024)

    def __str__(self) -> str:
        sign = "+" if self.size_diff >= 0 else ""
        return (
            f"{self.filepath}:{self.lineno} | "
            f"{sign}{self.size_diff_kb:,.1f} KiB ({self.size_total_kb:,.1f} KiB total) | "
            f"count: {sign}{self.count_diff} ({self.count_total} total)"
        )

    @classmethod
    def from_tracemalloc(cls, stat: tracemalloc.StatisticDiff) -> StatDiff:
        frame = stat.traceback[0] if stat.traceback else None
        return cls(
            filepath=frame.filename if frame else "<unknown>",
            lineno=frame.lineno if frame else 0,
            size_diff=stat.size_diff,
            size_total=stat.size,
            count_diff=stat.count_diff,
            count_total=stat.count,
        )


@dataclass(frozen=True, slots=True)
class SnapshotData:
    """Memory snapshot data."""

    timestamp: datetime
    iteration: int
    stats: tuple[StatDiff, ...]
    label: str = ""

    # Overall statistics
    traced_memory: int = 0  # current traced memory
    peak_memory: int = 0  # peak value

    @property
    def traced_memory_mb(self) -> float:
        return self.traced_memory / (1024 * 1024)

    @property
    def peak_memory_mb(self) -> float:
        return self.peak_memory / (1024 * 1024)

    @property
    def total_diff(self) -> int:
        return sum(s.size_diff for s in self.stats)

    @property
    def total_diff_mb(self) -> float:
        return self.total_diff / (1024 * 1024)


# ============================================================================
# Output backends
# ============================================================================


class OutputBackend(ABC):
    """Base class for profiling output backends."""

    @abstractmethod
    def write(self, data: SnapshotData) -> None:
        """Write snapshot data."""
        ...

    def start(self) -> None:
        """Called when profiling starts."""
        pass

    def stop(self) -> None:
        """Called when profiling stops."""
        pass


class FileOutput(OutputBackend):
    """Output to file."""

    def __init__(
        self,
        path: str | Path,
        *,
        mode: str = "a",
        include_header: bool = True,
        separator: str = "\n" + "=" * 80 + "\n",
    ) -> None:
        self.path = Path(path)
        self.mode = mode
        self.include_header = include_header
        self.separator = separator
        self._file = None

    def start(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._file = self.path.open(self.mode)
        if self.include_header:
            self._file.write(f"Memory Profiling started at {datetime.now().isoformat()}\n")
            self._file.write(self.separator)
            self._file.flush()

    def stop(self) -> None:
        if self._file:
            self._file.write(f"\nMemory Profiling stopped at {datetime.now().isoformat()}\n")
            self._file.close()
            self._file = None

    def write(self, data: SnapshotData) -> None:
        if not self._file:
            self.start()

        lines = [self._format_snapshot(data), self.separator]
        self._file.write("\n".join(lines))
        self._file.flush()

    def _format_snapshot(self, data: SnapshotData) -> str:
        header = (
            f"Snapshot #{data.iteration}"
            f"{f' [{data.label}]' if data.label else ''}"
            f" at {data.timestamp.strftime('%H:%M:%S.%f')[:-3]}"
        )
        memory_info = (
            f"Memory: {data.traced_memory_mb:,.2f} MB current, "
            f"{data.peak_memory_mb:,.2f} MB peak, "
            f"{data.total_diff_mb:+,.2f} MB diff"
        )
        stats_lines = [f"  {i}) {stat}" for i, stat in enumerate(data.stats, 1)]

        return "\n".join([header, memory_info, "Top allocations:", *stats_lines])


class LoggerOutput(OutputBackend):
    """Output via structlog/logging."""

    def __init__(
        self,
        logger: Any = None,
        *,
        level: str = "debug",
        include_stats: bool = True,
        max_stats_in_log: int = 10,
    ) -> None:
        self._logger = logger
        self.level = level
        self.include_stats = include_stats
        self.max_stats_in_log = max_stats_in_log

    @property
    def logger(self) -> Any:
        if self._logger is None:
            try:
                from structlog import get_logger
                self._logger = get_logger("memory_profiler")
            except ImportError:
                import logging
                self._logger = logging.getLogger("memory_profiler")
        return self._logger

    def write(self, data: SnapshotData) -> None:
        log_method = getattr(self.logger, self.level, self.logger.info)

        log_data: dict[str, Any] = {
            "iteration": data.iteration,
            "traced_memory_mb": round(data.traced_memory_mb, 2),
            "peak_memory_mb": round(data.peak_memory_mb, 2),
            "diff_mb": round(data.total_diff_mb, 2),
        }

        if data.label:
            log_data["label"] = data.label

        if self.include_stats:
            log_data["top_allocations"] = [
                {
                    "location": f"{s.filepath}:{s.lineno}",
                    "size_diff_kb": round(s.size_diff_kb, 1),
                    "size_total_kb": round(s.size_total_kb, 1),
                }
                for s in data.stats[: self.max_stats_in_log]
            ]

        log_method("memory_snapshot", **log_data)


class CallbackOutput(OutputBackend):
    """Output via custom callback."""

    def __init__(self, callback: Callable[[SnapshotData], None]) -> None:
        self.callback = callback

    def write(self, data: SnapshotData) -> None:
        self.callback(data)


class MultiOutput(OutputBackend):
    """Combined output to multiple backends."""

    def __init__(self, *backends: OutputBackend) -> None:
        self.backends = list(backends)

    def add(self, backend: OutputBackend) -> MultiOutput:
        self.backends.append(backend)
        return self

    def start(self) -> None:
        for backend in self.backends:
            backend.start()

    def stop(self) -> None:
        for backend in self.backends:
            backend.stop()

    def write(self, data: SnapshotData) -> None:
        for backend in self.backends:
            backend.write(data)


class NullOutput(OutputBackend):
    """Null output - does nothing."""

    def write(self, data: SnapshotData) -> None:
        pass


# ============================================================================
# Configuration
# ============================================================================


@dataclass
class MemoryProfilerConfig:
    """Profiler configuration."""

    # Take snapshot every N calls to track()
    every_n_calls: int = 1

    # Number of top allocations in report
    top_stats: int = 25

    # Statistics grouping
    group_by: GroupBy = GroupBy.LINENO

    # Number of frames in traceback (more = more detail, but slower)
    nframes: int = 1

    # Auto-stop after N iterations (None = never)
    stop_after: int | None = None

    # Exit program on stop_after (for debugging)
    exit_on_stop: bool = False

    # Filter by filepath (only files containing this string)
    filter_filename: str | None = None

    # Exclude stdlib and site-packages
    exclude_stdlib: bool = True

    # Minimum size change to include in report (bytes)
    min_size_diff: int = 0

    @classmethod
    def for_debugging(cls) -> MemoryProfilerConfig:
        """Config for debugging memory leaks."""
        return cls(
            every_n_calls=1,
            top_stats=50,
            nframes=10,
            exclude_stdlib=True,
        )

    @classmethod
    def for_production(cls) -> MemoryProfilerConfig:
        """Lightweight config for production monitoring."""
        return cls(
            every_n_calls=100,
            top_stats=10,
            nframes=1,
            exclude_stdlib=True,
        )


# ============================================================================
# Main profiler class
# ============================================================================


class MemoryProfiler:
    """
    Universal memory profiler.

    Examples:
        # Basic usage
        profiler = MemoryProfiler(output=FileOutput("mem.log"))
        profiler.start()
        for item in items:
            process(item)
            profiler.track()
        profiler.stop()

        # With config
        profiler = MemoryProfiler(
            config=MemoryProfilerConfig.for_debugging(),
            output=MultiOutput(
                FileOutput("mem.log"),
                LoggerOutput(level="info"),
            ),
        )

        # Quick start
        profiler = MemoryProfiler.create(
            output="mem.log",
            every_n_calls=5,
            top=25,
        )
    """

    def __init__(
        self,
        *,
        config: MemoryProfilerConfig | None = None,
        output: OutputBackend | None = None,
    ) -> None:
        self.config = config or MemoryProfilerConfig()
        self.output = output or NullOutput()

        self._call_count = 0
        self._prev_snapshot: tracemalloc.Snapshot | None = None
        self._started = False
        self._stopped = False

    @classmethod
    def create(
        cls,
        *,
        output: str | Path | OutputBackend | None = None,
        every_n_calls: int = 1,
        top: int = 25,
        stop_after: int | None = None,
        exit_on_stop: bool = False,
        nframes: int = 1,
    ) -> MemoryProfiler:
        """Factory method for quick profiler creation."""
        config = MemoryProfilerConfig(
            every_n_calls=every_n_calls,
            top_stats=top,
            stop_after=stop_after,
            exit_on_stop=exit_on_stop,
            nframes=nframes,
        )

        if output is None:
            output_backend = LoggerOutput()
        elif isinstance(output, (str, Path)):
            output_backend = FileOutput(output)
        else:
            output_backend = output

        return cls(config=config, output=output_backend)

    def start(self) -> MemoryProfiler:
        """Start profiling."""
        if self._started:
            return self

        _tracemalloc_acquire(self.config.nframes)
        self.output.start()
        self._started = True
        self._stopped = False
        return self

    def stop(self) -> MemoryProfiler:
        """Stop profiling."""
        if not self._started or self._stopped:
            return self

        self.output.stop()
        _tracemalloc_release()
        self._stopped = True
        return self

    def reset(self) -> MemoryProfiler:
        """Reset state (counters and snapshot)."""
        self._call_count = 0
        self._prev_snapshot = None
        if self._started:
            tracemalloc.reset_peak()
        return self

    def track(self, label: str = "") -> SnapshotData | None:
        """
        Track an iteration.

        Call after each logical unit of work.
        Snapshot will be taken according to config.every_n_calls.

        Args:
            label: Optional label for the snapshot

        Returns:
            SnapshotData if snapshot was taken, otherwise None
        """
        if not self._started or self._stopped:
            return None

        self._call_count += 1

        # First call - baseline snapshot
        if self._call_count == 1:
            self._prev_snapshot = tracemalloc.take_snapshot()
            return None

        # Check interval
        if self._call_count % self.config.every_n_calls != 0:
            result = None
        else:
            result = self._record_snapshot(label)

        # Check limit
        if self.config.stop_after and self._call_count >= self.config.stop_after:
            self.stop()
            if self.config.exit_on_stop:
                sys.exit(1)

        return result

    def snapshot_now(self, label: str = "") -> SnapshotData:
        """Take snapshot immediately, ignoring interval."""
        if not self._started:
            self.start()
        return self._record_snapshot(label)

    def _record_snapshot(self, label: str = "") -> SnapshotData:
        """Internal method to record a snapshot."""
        current = tracemalloc.take_snapshot()
        traced, peak = tracemalloc.get_traced_memory()

        # Filter snapshot
        current = self._filter_snapshot(current)

        # Compare with previous
        if self._prev_snapshot is not None:
            filtered_prev = self._filter_snapshot(self._prev_snapshot)
            raw_stats = current.compare_to(filtered_prev, self.config.group_by.value)
        else:
            raw_stats = current.statistics(self.config.group_by.value)
            raw_stats = [
                tracemalloc.StatisticDiff(
                    traceback=s.traceback,
                    size=s.size,
                    size_diff=s.size,
                    count=s.count,
                    count_diff=s.count,
                )
                for s in raw_stats
            ]

        # Filter by min_size_diff
        if self.config.min_size_diff > 0:
            raw_stats = [s for s in raw_stats if abs(s.size_diff) >= self.config.min_size_diff]

        # Sort by absolute change
        raw_stats.sort(key=lambda s: abs(s.size_diff), reverse=True)

        # Convert to our format
        stats = tuple(
            StatDiff.from_tracemalloc(s) for s in raw_stats[: self.config.top_stats]
        )

        data = SnapshotData(
            timestamp=datetime.now(),
            iteration=self._call_count,
            stats=stats,
            label=label,
            traced_memory=traced,
            peak_memory=peak,
        )

        self.output.write(data)
        self._prev_snapshot = current

        return data

    def _filter_snapshot(self, snapshot: tracemalloc.Snapshot) -> tracemalloc.Snapshot:
        """Apply filters to snapshot."""
        filters = []

        if self.config.exclude_stdlib:
            # Exclude stdlib
            filters.append(tracemalloc.Filter(False, "<frozen importlib._bootstrap>"))
            filters.append(tracemalloc.Filter(False, "<frozen importlib._bootstrap_external>"))
            filters.append(tracemalloc.Filter(False, "<unknown>"))

            # Exclude tracemalloc itself
            filters.append(tracemalloc.Filter(False, tracemalloc.__file__))

        if self.config.filter_filename:
            filters.append(
                tracemalloc.Filter(True, f"*{self.config.filter_filename}*")
            )

        if filters:
            return snapshot.filter_traces(filters)
        return snapshot

    @property
    def call_count(self) -> int:
        """Number of track() calls."""
        return self._call_count

    @property
    def is_running(self) -> bool:
        """Whether profiler is running."""
        return self._started and not self._stopped

    def __enter__(self) -> MemoryProfiler:
        return self.start()

    def __exit__(self, *args: Any) -> None:
        self.stop()

    async def __aenter__(self) -> MemoryProfiler:
        return self.start()

    async def __aexit__(self, *args: Any) -> None:
        self.stop()


# ============================================================================
# Global profiler instance
# ============================================================================


_global_profiler: MemoryProfiler | None = None


def global_profiler(
    *,
    output: str | Path | OutputBackend | None = None,
    every_n_calls: int = 1,
    top: int = 25,
    stop_after: int | None = None,
    reset: bool = False,
) -> MemoryProfiler:
    """
    Get or create global profiler.

    Convenient for application-wide profiling.

    Args:
        output: File path or OutputBackend
        every_n_calls: Snapshot interval (in track() calls)
        top: Number of top allocations
        stop_after: Stop after N iterations
        reset: Recreate profiler

    Returns:
        Global MemoryProfiler instance
    """
    global _global_profiler

    if _global_profiler is None or reset:
        _global_profiler = MemoryProfiler.create(
            output=output,
            every_n_calls=every_n_calls,
            top=top,
            stop_after=stop_after,
        )
        _global_profiler.start()

    return _global_profiler


# ============================================================================
# Decorators
# ============================================================================


@overload
def profile_memory(func: Callable[P, R]) -> Callable[P, R]: ...


@overload
def profile_memory(
    *,
    output: str | Path | OutputBackend | None = None,
    every_n_calls: int | None = None,
    top: int | None = None,
    stop_after: int | None = None,
    label: str | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]: ...


def profile_memory(
    func: Callable[P, R] | None = None,
    *,
    output: str | Path | OutputBackend | None = None,
    every_n_calls: int | None = None,
    top: int | None = None,
    stop_after: int | None = None,
    label: str | None = None,
) -> Callable[P, R] | Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator for profiling memory usage of a function/method.

    Each call to the decorated function will be tracked.

    If any of output, every_n_calls, top, stop_after is set, the function
    gets its own profiler. Otherwise the global profiler is used.

    Examples:
        # Own profiler
        @profile_memory(output="mem.log", every_n_calls=5)
        async def process_batch(data):
            ...

        # Global profiler
        @profile_memory
        def process_item(item):
            ...

        # Global profiler too
        @profile_memory(label="items")
        def process_item(item):
            ...

    Args:
        func: Function to decorate
        output: File path or OutputBackend
        every_n_calls: Snapshot interval (in function calls), 1 by default
        top: Number of top allocations, 25 by default
        stop_after: Stop after N iterations
        label: Label for snapshots (defaults to function name)
    """
    own_settings: dict[str, Any] = {
        name: value
        for name, value in (
            ("output", output),
            ("every_n_calls", every_n_calls),
            ("top", top),
            ("stop_after", stop_after),
        )
        if value is not None
    }

    def decorator(fn: Callable[P, R]) -> Callable[P, R]:
        get_profiler: Callable[[], MemoryProfiler]
        if not own_settings:
            # not global_profiler() here - decorators run at import time, before
            # the entry point configures the global profiler
            get_profiler = global_profiler
        else:
            own_profiler = MemoryProfiler.create(**own_settings)
            own_profiler.start()
            get_profiler = lambda: own_profiler
        fn_label = label or fn.__qualname__

        if asyncio.iscoroutinefunction(fn):

            @wraps(fn)
            async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                result = await fn(*args, **kwargs)
                get_profiler().track(fn_label)
                return result

            return async_wrapper  # type: ignore
        else:

            @wraps(fn)
            def sync_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                result = fn(*args, **kwargs)
                get_profiler().track(fn_label)
                return result

            return sync_wrapper  # type: ignore

    if func is not None:
        return decorator(func)
    return decorator


# ============================================================================
# Context managers
# ============================================================================


@contextmanager
def memory_snapshot(
    label: str = "",
    *,
    output: str | Path | OutputBackend | None = None,
    top: int = 15,
) -> Iterator[MemoryProfiler]:
    """
    Context manager for measuring memory usage of a code block.

    Examples:
        with memory_snapshot("heavy operation"):
            do_something_heavy()

        with memory_snapshot("db query", output="mem.log") as profiler:
            result = db.query(...)
            # profiler.snapshot_now("after query")  # additional snapshot
    """
    profiler = MemoryProfiler.create(output=output, top=top)
    profiler.start()

    try:
        yield profiler
    finally:
        profiler.snapshot_now(label or "block exit")
        profiler.stop()


@asynccontextmanager
async def async_memory_snapshot(
    label: str = "",
    *,
    output: str | Path | OutputBackend | None = None,
    top: int = 15,
) -> AsyncIterator[MemoryProfiler]:
    """Async version of memory_snapshot."""
    profiler = MemoryProfiler.create(output=output, top=top)
    profiler.start()

    try:
        yield profiler
    finally:
        profiler.snapshot_now(label or "block exit")
        profiler.stop()


# ============================================================================
# Convenience functions
# ============================================================================


def get_current_memory() -> tuple[float, float]:
    """
    Get current memory consumption.

    Returns:
        (current_mb, peak_mb) - current and peak memory in MB

    Note:
        If tracemalloc is not running, it will be started automatically
    """
    if not tracemalloc.is_tracing():
        _tracemalloc_acquire(1)

    current, peak = tracemalloc.get_traced_memory()
    return current / (1024 * 1024), peak / (1024 * 1024)


def format_memory(bytes_value: int) -> str:
    """Format bytes to human-readable format."""
    for unit in ("B", "KiB", "MiB", "GiB"):
        if abs(bytes_value) < 1024:
            return f"{bytes_value:,.1f} {unit}"
        bytes_value //= 1024
    return f"{bytes_value:,.1f} TiB"
