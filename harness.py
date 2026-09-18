"""Shared test harness for every problem in this repo.

Each problem keeps its solutions in ``<problem>/solutions/*.py`` and its tests in
``<problem>/tests/``. :func:`load_solutions` bridges the two: a test file asks for the
solutions sitting beside it and gets back one pytest param per solution module. Dropping
a new file into ``solutions/`` is therefore the only step needed to put it under test --
no test file has to change, and CI picks it up on the next push.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from collections.abc import Callable
from pathlib import Path

import pytest


def _module_name(problem: str, stem: str) -> str:
    """Build a sys.modules key that is unique per problem.

    Two problems may both hold a ``hash_map.py``; without the problem folder in the key
    the second import would silently return the first one's module.
    """
    return "leetcode_" + re.sub(r"\W", "_", f"{problem}_{stem}")


def _load(path: Path, problem: str, method: str) -> Callable:
    """Import one solution module and return ``Solution().<method>`` bound."""
    spec = importlib.util.spec_from_file_location(_module_name(problem, path.stem), path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot build an import spec for {path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    solution_cls = getattr(module, "Solution", None)
    if solution_cls is None:
        raise AttributeError(f"{path.name} defines no `Solution` class")

    bound = getattr(solution_cls(), method, None)
    if bound is None:
        raise AttributeError(f"{path.name}: `Solution` has no method `{method}`")

    return bound


def _broken(path: Path, error: Exception) -> Callable:
    """Stand in for a solution that would not load, failing when the test calls it.

    Returning a failing callable rather than raising here keeps one bad solution from
    aborting collection for its siblings -- only its own params go red.
    """

    def fail(*_args, **_kwargs):
        pytest.fail(f"could not load solution `{path.name}`: {type(error).__name__}: {error}")

    return fail


def load_solutions(test_file: str, method: str) -> list:
    """Return one pytest param per solution module beside ``test_file``.

    Args:
        test_file: pass ``__file__`` from the problem's test module.
        method: the LeetCode method name each ``Solution`` class exposes, e.g. ``"twoSum"``.

    Each param carries the bound method, with the module stem as its test id, so a failure
    reads as ``test_two_sum[hash_map]``.
    """
    problem_dir = Path(test_file).resolve().parent.parent
    solutions_dir = problem_dir / "solutions"

    if not solutions_dir.is_dir():
        raise FileNotFoundError(f"no solutions directory at {solutions_dir}")

    params = []
    for path in sorted(solutions_dir.glob("*.py")):
        if path.name.startswith("_"):
            continue
        try:
            solution = _load(path, problem_dir.name, method)
        except Exception as error:  # noqa: BLE001 - surfaced by the failing param below
            solution = _broken(path, error)
        params.append(pytest.param(solution, id=path.stem))

    if not params:
        raise FileNotFoundError(f"no solution modules found in {solutions_dir}")

    return params
