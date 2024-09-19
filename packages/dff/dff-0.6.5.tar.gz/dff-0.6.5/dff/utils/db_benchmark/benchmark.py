"""
Context storage benchmarking
----------------------------
This module contains functions for context storages benchmarking.

The basic function is :py:func:`~.time_context_read_write` but it has a low level interface.

Higher level wrappers of the function provided by this module are:

- :py:func:`~.save_results_to_file` -- saves results for a list of benchmark cases.
- :py:func:`~.benchmark_all` -- a wrapper of `save_results_to_file`. Creates cases from configs.

Wrappers use :py:class:`~.BenchmarkConfig` interface to configure benchmarks.
A simple configuration class as well as a configuration set are provided by
:py:mod:`dff.utils.db_benchmark.basic_config`.

To view files generated by :py:func:`~.save_results_to_file` use either
:py:func:`~dff.utils.db_benchmark.report.report` or
`our streamlit app <../_misc/benchmark_streamlit.py>`_.
"""
from uuid import uuid4
from pathlib import Path
from time import perf_counter
from typing import Tuple, List, Dict, Union, Optional, Callable, Any
import json
import importlib
from statistics import mean
import abc
from traceback import extract_tb, StackSummary

from pydantic import BaseModel, Field
from tqdm.auto import tqdm

from dff.context_storages import DBContextStorage
from dff.script import Context


def time_context_read_write(
    context_storage: DBContextStorage,
    context_factory: Callable[[], Context],
    context_num: int,
    context_updater: Optional[Callable[[Context], Optional[Context]]] = None,
) -> Tuple[List[float], List[Dict[int, float]], List[Dict[int, float]]]:
    """
    Benchmark `context_storage` by writing and reading `context`\\s generated by `context_factory`
    into it / from it `context_num` times.
    If `context_updater` is not `None` it is used to update `context`\\s and benchmark update operation.

    This function clears `context_storage` before and after execution.

    :param context_storage: Context storage to benchmark.
    :param context_factory: A function that creates contexts which will be written into context storage.
    :param context_num: A number of times the context will be written and read.
    :param context_updater:
        None or a function.
        If not None, function should accept :py:class:`~.Context` and return an updated :py:class:`~.Context`.
        The updated context can be either the same object (at the same pointer) or a different object (e.g. copied).
        The updated context should have a higher dialog length than the received context
        (to emulate context updating during dialog).
        The function should return `None` to stop updating contexts.
        For an example of such function, see implementation of
        :py:meth:`dff.utils.db_benchmark.basic_config.BasicBenchmarkConfig.context_updater`.

        To avoid keeping many contexts in memory,
        this function will be called repeatedly at least `context_num` times.
    :return:
        A tuple of 3 elements.

        The first element -- a list of write times. Its length is equal to `context_num`.

        The second element -- a list of dictionaries with read times.
        Each dictionary maps from int to float. The key in the mapping is the `dialog_len` of the context and the
        values are the read times for the corresponding `dialog_len`.
        If `context_updater` is None, all dictionaries will have only one key --
        dialog length of the context returned by `context_factory`.
        Otherwise, the dictionaries will also have a key for each updated context.

        The third element -- a list of dictionaries with update times.
        Structurally the same as the second element, but none of the elements here have a key for
        dialog_len of the context returned by `context_factory`.
        So if `context_updater` is None, all dictionaries will be empty.
    """
    context_storage.clear()

    write_times: List[float] = []
    read_times: List[Dict[int, float]] = []
    update_times: List[Dict[int, float]] = []

    for _ in tqdm(range(context_num), desc=f"Benchmarking context storage:{context_storage.full_path}", leave=False):
        context = context_factory()

        ctx_id = uuid4()

        # write operation benchmark
        write_start = perf_counter()
        context_storage[ctx_id] = context
        write_times.append(perf_counter() - write_start)

        read_times.append({})
        update_times.append({})

        # read operation benchmark
        read_start = perf_counter()
        _ = context_storage[ctx_id]
        read_time = perf_counter() - read_start
        read_times[-1][len(context.labels)] = read_time

        if context_updater is not None:
            updated_context = context_updater(context)

            while updated_context is not None:
                update_start = perf_counter()
                context_storage[ctx_id] = updated_context
                update_time = perf_counter() - update_start
                update_times[-1][len(updated_context.labels)] = update_time

                read_start = perf_counter()
                _ = context_storage[ctx_id]
                read_time = perf_counter() - read_start
                read_times[-1][len(updated_context.labels)] = read_time

                updated_context = context_updater(updated_context)

        context_storage.clear()
    return write_times, read_times, update_times


class DBFactory(BaseModel):
    """
    A class for storing information about context storage to benchmark.
    Also used to create a context storage from the configuration.
    """

    uri: str
    """URI of the context storage."""
    factory_module: str = "dff.context_storages"
    """A module containing `factory`."""
    factory: str = "context_storage_factory"
    """Name of the context storage factory. (function that creates context storages from URIs)"""

    def db(self):
        """
        Create a context storage using `factory` from `uri`.
        """
        module = importlib.import_module(self.factory_module)
        return getattr(module, self.factory)(self.uri)


class BenchmarkConfig(BaseModel, abc.ABC, frozen=True):
    """
    Configuration for a benchmark.

    Defines methods and parameters required to run :py:func:`~.time_context_read_write`.
    Also defines a method (`info`) for displaying information about this configuration.

    A simple way to configure benchmarks is provided by
    :py:class:`~.dff.utils.db_benchmark.basic_config.BasicBenchmarkConfig`.

    Inherit from this class only if `BasicBenchmarkConfig` is not enough for your benchmarking needs.
    """

    context_num: int = 30
    """
    Number of times the contexts will be benchmarked.
    Increasing this number decreases standard error of the mean for benchmarked data.
    """

    @abc.abstractmethod
    def get_context(self) -> Context:
        """
        Return context to benchmark read and write operations with.

        This function will be called `context_num` times.
        """
        ...

    @abc.abstractmethod
    def info(self) -> Dict[str, Any]:
        """
        Return a dictionary with information about this configuration.
        """
        ...

    @abc.abstractmethod
    def context_updater(self, context: Context) -> Optional[Context]:
        """
        Update context with new dialog turns or return `None` to stop updates.

        This function is used to benchmark update and read operations.

        This function will be called AT LEAST `context_num` times.

        :return: Updated context or `None` to stop updating context.
        """
        ...


class BenchmarkCase(BaseModel):
    """
    This class represents a benchmark case and includes
    information about it, its configuration and configuration of a context storage to benchmark.
    """

    name: str
    """Name of a benchmark case."""
    db_factory: DBFactory
    """DBFactory that specifies context storage to benchmark."""
    benchmark_config: BenchmarkConfig
    """Benchmark configuration."""
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    """Unique id of the case. Defaults to a random uuid."""
    description: str = ""
    """Description of the case. Defaults to an empty string."""

    @staticmethod
    def set_average_results(benchmark):
        """
        Modify `benchmark` dictionary to include averaged benchmark results.

        Add field "average_results" to the benchmark that contains the following fields:

            - average_write_time
            - average_read_time
            - average_update_time
            - read_times_grouped_by_context_num -- a list of read times.
              Each element is the average of read times with the same context_num.
            - read_times_grouped_by_dialog_len -- a dictionary of read times.
              Its values are the averages of read times with the same dialog_len,
              its keys are dialog_len values.
            - update_times_grouped_by_context_num
            - update_times_grouped_by_dialog_len
            - pretty_write -- average write time with only 3 significant digits.
            - pretty_read
            - pretty_update
            - pretty_read+update -- sum of average read and update times with only 3 significant digits.

        :param benchmark:
            A dictionary returned by `BenchmarkCase._run`.
            Should include a "success" and "result" fields.
            "success" field should be true.
            "result" field should be a dictionary with the values returned by
            :py:func:`~.time_context_read_write` and keys
            "write_times", "read_times" and "update_times".
        :return: None
        """
        if not benchmark["success"] or isinstance(benchmark["result"], str):
            return

        def get_complex_stats(results):
            if len(results) == 0 or len(results[0]) == 0:
                return [], {}, None

            average_grouped_by_context_num = [mean(times.values()) for times in results]
            average_grouped_by_dialog_len = {key: mean([times[key] for times in results]) for key in results[0].keys()}
            average = float(mean(average_grouped_by_context_num))
            return average_grouped_by_context_num, average_grouped_by_dialog_len, average

        read_stats = get_complex_stats(benchmark["result"]["read_times"])
        update_stats = get_complex_stats(benchmark["result"]["update_times"])

        result = {
            "average_write_time": mean(benchmark["result"]["write_times"]),
            "average_read_time": read_stats[2],
            "average_update_time": update_stats[2],
            "read_times_grouped_by_context_num": read_stats[0],
            "read_times_grouped_by_dialog_len": read_stats[1],
            "update_times_grouped_by_context_num": update_stats[0],
            "update_times_grouped_by_dialog_len": update_stats[1],
        }
        result["pretty_write"] = (
            float(f'{result["average_write_time"]:.3}') if result["average_write_time"] is not None else None
        )
        result["pretty_read"] = (
            float(f'{result["average_read_time"]:.3}') if result["average_read_time"] is not None else None
        )
        result["pretty_update"] = (
            float(f'{result["average_update_time"]:.3}') if result["average_update_time"] is not None else None
        )
        result["pretty_read+update"] = (
            float(f'{result["average_read_time"] + result["average_update_time"]:.3}')
            if result["average_read_time"] is not None and result["average_update_time"] is not None
            else None
        )

        benchmark["average_results"] = result

    def _run(self):
        try:
            write_times, read_times, update_times = time_context_read_write(
                self.db_factory.db(),
                self.benchmark_config.get_context,
                self.benchmark_config.context_num,
                self.benchmark_config.context_updater,
            )
            return {
                "success": True,
                "result": {
                    "write_times": write_times,
                    "read_times": read_times,
                    "update_times": update_times,
                },
            }
        except Exception as e:
            return {
                "success": False,
                "result": {
                    "type": e.__class__.__name__,
                    "msg": getattr(e, "message", str(e)),
                    "traceback": "\n".join(StackSummary.from_list(extract_tb(e.__traceback__)).format()),
                },
            }

    def run(self):
        """
        Run benchmark, return results.

        :return:
            A dictionary with 3 keys: "success", "result", "average_results".

            Success is a bool value. It is false if an exception was raised during benchmarking.

            Result is either an exception message or a dictionary with 3 keys
            ("write_times", "read_times", "update_times").
            Values of those fields are the values returned by :py:func:`~.time_context_read_write`.

            Average results field is as described in :py:meth:`~.BenchmarkCase.set_average_results`.
        """
        benchmark = self._run()
        BenchmarkCase.set_average_results(benchmark)
        return benchmark


def save_results_to_file(
    benchmark_cases: List[BenchmarkCase],
    file: Union[str, Path],
    name: str,
    description: str,
    exist_ok: bool = False,
):
    """
    Benchmark all `benchmark_cases` and save results to a file.

    Result are saved in json format with this schema:
    `utils/db_benchmark/benchmark_schema.json <../_misc/benchmark_schema.json>`_.

    Files created by this function cen be viewed either by using :py:func:`~dff.utils.db_benchmark.report.report` or
    streamlit app located in the utils directory:
    `utils/db_benchmark/benchmark_streamlit.py <../_misc/benchmark_streamlit.py>`_.

    :param benchmark_cases: A list of benchmark cases that specify benchmarks.
    :param file: File to save results to.
    :param name: Name of the benchmark set.
    :param description: Description of the benchmark set.
    :param exist_ok: Whether to continue if the file already exists.
    """
    with open(file, "w" if exist_ok else "x", encoding="utf-8") as fd:
        uuid = str(uuid4())
        result: Dict[str, Any] = {
            "name": name,
            "description": description,
            "uuid": uuid,
            "benchmarks": [],
        }
        cases = tqdm(benchmark_cases, leave=False)
        case: BenchmarkCase
        for case in cases:
            cases.set_description(f"Benchmarking: {case.name}")
            result["benchmarks"].append(
                {
                    **case.model_dump(exclude={"benchmark_config"}),
                    "benchmark_config": case.benchmark_config.info(),
                    **case.run(),
                }
            )

        json.dump(result, fd)


def benchmark_all(
    file: Union[str, Path],
    name: str,
    description: str,
    db_uri: str,
    benchmark_configs: Dict[str, BenchmarkConfig],
    exist_ok: bool = False,
):
    """
    A wrapper for :py:func:`~.save_results_to_file`.

    Generates `benchmark_cases` from `db_uri` and `benchmark_configs`:
    `db_uri` is used to initialize :py:class:`~.DBFactory` instance
    which is then used along with `benchmark_configs` to initialize :py:class:`~.BenchmarkCase` instances.

    :param file: File to save results to.
    :param name: Name of the benchmark set.
    :param description: Description of the benchmark set. The same description is used for benchmark cases.
    :param db_uri: URI of the database to benchmark
    :param benchmark_configs: Mapping from case names to configs.
    :param exist_ok: Whether to continue if the file already exists.
    """
    save_results_to_file(
        [
            BenchmarkCase(
                name=case_name,
                description=description,
                db_factory=DBFactory(uri=db_uri),
                benchmark_config=benchmark_config,
            )
            for case_name, benchmark_config in benchmark_configs.items()
        ],
        file,
        name,
        description,
        exist_ok=exist_ok,
    )
