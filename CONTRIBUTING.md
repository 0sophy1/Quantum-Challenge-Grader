# Contributing

## Prerequisites

* [uv](https://docs.astral.sh/uv/getting-started/installation/)
* [Just](https://just.systems/man/en/)

## Installation

```sh
uv sync
```

(uv automatically creates and manages a virtual environment.)

## Format code

```
just fmt
```

## Lint

```
just lint
```

To run the individual linters:

* Ruff: `uv run ruff check`
* Ty (type check): `uv run ty check`

## Tests

```
just test
```

## Update dependencies

([Original documentation](https://docs.astral.sh/uv/concepts/projects/dependencies/))

Add a dependency:

```
uv add <dependency>
```

Add a dev dependency:

```
uv add <dependency> --dev
```

## Release a new version

You should release a new version any time you make user-facing changes.

Releasing is automated. To cut a release, update `__version__` in
[`qc_grader/__init__.py`](qc_grader/__init__.py) to **today's date** and merge to `main`.
A GitHub Actions workflow then builds the package, publishes it to PyPI, and creates a
GitHub Release whose notes link to the commits included in that release.

### Version format

Versions are date-based, written as **`YEAR.MONTH.DAY`** with **no leading zeros**:

* The year comes first, then the month, then the day (`YEAR.MONTH.DAY`).
* Do not pad with zeros: use `6`, not `06`.

For example, a release made on **18 June 2026** is version `2026.6.18`.

| Date           | Version     |
| -------------- | ----------- |
| 18 June 2026   | `2026.6.18` |
| 1 December 2026 | `2026.12.1` |
| 5 January 2027 | `2027.1.5`  |

If you need to release more than once on the same day, add a counter at the end, starting
at `.1`: the second release on 18 June 2026 is `2026.6.18.1`, the third is `2026.6.18.2`,
and so on.

Versions only ever move forward — we always release from the latest `main` and never
maintain older versions in parallel.

## Run the client

Use this workflow to test the Python client against the Grader server.

### Initial setup

You must create a Quantum API token for an account with at least one instance.
Set up the prod account below. The staging/local account is only needed if you
test the client against the staging or local development server (`STAGING=1` or
`DEV=1`) — skip it otherwise.

**Prod server** (default):

1. Use https://quantum.cloud.ibm.com to create the API key
2. Save the key by running `uv run python`, then this code:

```python
from qiskit_ibm_runtime import QiskitRuntimeService

QiskitRuntimeService.save_account(
    token="<your-api-key>",
    instance="<CRN>",
)
```
3. Close the REPL.

**Staging or local development server** (only if you use `STAGING=1` or `DEV=1`):

1. Use https://quantum.test.cloud.ibm.com to create the API key.
2. Save the key by running `uv run python`, then this code:

```python
from qiskit_ibm_runtime import QiskitRuntimeService

QiskitRuntimeService.save_account(
    token="<your-api-key>",
    instance="<CRN>",
    name="grader-staging",
)
```
3. Close the REPL.

### Manually testing your changes (before opening a PR)

This is a development phase check, not how the grader is normally used. End users
`pip install qc-grader` and call the grading functions from their challenge
notebooks; challenge owners just merge their labs and the published package is
used as-is. Before opening a PR, you can exercise your grading functions against
a running server from a REPL:

1. Launch a Python REPL:
  - Prod server: `uv run python`
  - Staging server: `STAGING=1 uv run python`
  - Local development server: `DEV=1 uv run python`
2. In the REPL, import and run your exercises. For example:

```python
>>> from qc_grader.challenges.challenge import grade_lab0_ex1
>>> grade_lab0_ex1()
```

For developers testing how the server behaves, you can use the files from `qc_grader.challenges.test_challenges`, such as `grade_success` from `qc_grader.challenges.test_challenges.individual`.

## Adding a new challenge

Create a new folder under `qc_grader/challenges` with the name of the challenge. This folder should contain:

* A file for each lab (such as `lab0.py`, `lab2.py`)
* An `__init__.py`, which imports and re-exports the grading functions from your labs.

  Every challenge must also export a `check_progress` function so users can see how far they've gotten. Add this to the same `__init__.py`:

  ```python
  from qc_grader.grader.grade import create_check_progress_function

  # Replace the string with the name of your challenge
  check_progress = create_check_progress_function("...")
  ```

  `create_check_progress_function` is a factory: it takes your challenge name and returns a ready-made `check_progress` function with that name baked in, so you don't have to write it out yourself. It runs once, at import time, and makes no network call — the request to the server only happens later, when a user actually calls `check_progress()`. That call prints a challenge-wide aggregate plus a per-lab and per-exercise breakdown of their submissions; they can also pass a lab name — `check_progress("lab1")` — to see just that lab.

  Only if your challenge is run as a team challenge, also export a `join_team` function in the same `__init__.py` (skip this entirely for individual challenges):

  ```python
  from qc_grader.grader.grade import create_join_team_function

  # Replace the string with the name of your challenge
  join_team = create_join_team_function("...")
  ```

  `create_join_team_function` works the same way — it binds your challenge name and returns a `join_team` function. When a participant calls `join_team("<team name>")`, their submissions are associated with that team; they can switch teams at any time.

You may find it easier to copy an existing challenge and modify it.

## Adding new labs

A *lab* is a single Python file corresponding to a Jupyter notebook that users receive. Each *challenge* has one or more labs. When you add new exercises to the server, add a matching Python file here so that users can call grading functions from their Jupyter notebooks.

Create `qc_grader/challenges/{challenge}/{lab}.py`, e.g. `qc_grader/challenges/challenge/lab1.py`.

The `_CHALLENGE` and `_LAB` constants, and each exercise string (e.g., `"ex1"`), must exactly match the identifiers configured on the server. These are permanent: once a challenge is live, changing them breaks existing notebook submissions. (The challenge, lab, and exercise identifiers, and the actual grading, are configured server-side by the IBM Quantum team; the client only forwards answers to them.)

A minimal lab file:

```python
# qc_grader/challenges/challenge/lab1.py
from typing import Any

from typeguard import typechecked

from qc_grader.grader.grade import grade_answer

_CHALLENGE = "challenge"
_LAB = "lab1"


def _grade(answer: Any, exercise: str) -> None:
    grade_answer(answer, lab=_LAB, exercise=exercise, challenge=_CHALLENGE)


@typechecked
def grade_lab1_ex1(answer: str) -> None:
    _grade(answer, "ex1")


@typechecked
def grade_lab1_ex2(answer: int) -> None:
    _grade(answer, "ex2")
```

Then, export every grading function from the challenge package's `__init__.py`:

```python
# qc_grader/challenges/challenge/__init__.py
from .lab1 import grade_lab1_ex1, grade_lab1_ex2

__all__ = ["grade_lab1_ex1", "grade_lab1_ex2"]
```

Users can then import your functions like this:

```python
from qc_grader.challenges.challenge import grade_lab1_ex1
```

### Type validation

All grading functions must use the `@typechecked` decorator from `typeguard` and precise type hints on the answer parameter. This lets the client reject submissions with the wrong data type before they reach the server.

Use the most specific type that describes what the user should submit — `QuantumCircuit`, `Statevector`, `int`, `float`, etc. Avoid `Any` or bare `dict` and bare `list`.

```python
from typeguard import typechecked

@typechecked
def grade_lab1_ex1(arg1: str, arg2: list[int], arg3: QuantumCircuit) -> None:
    ...
```

#### Dictionaries with required keys

If the user submits a dictionary with specific keys, use `typing.TypedDict` rather than a generic `dict`. `TypedDict` allows `typechecked` to validate each key's name and type:

```python
from typing import TypedDict

from typeguard import typechecked

Ex1Input = TypedDict("Ex1Input", {"0": int, "1": int})

@typechecked
def grade_lab0_ex1(counts: Ex1Input) -> None:
    ...
```

#### Multiple accepted types

Use a union (`|`) to accept more than one type:

```python
@typechecked
def grade_lab0_ex1(answer: int | float) -> None:
    ...
```

#### Flexible types with transformation

It is often helpful to accept a more flexible data type and transform it before sending to the server. When doing so, anticipate likely user mistakes and raise a `ValueError` if they violate your assumptions. For example, this accepts either a `float` or an `ndarray` (useful when users are working with NumPy) and validates that the array is a scalar:

```python
from typeguard import typechecked

@typechecked
def grade_lab0_ex1(exp_val: np.ndarray | float) -> None:
    arr = np.asarray(exp_val)
    if arr.ndim != 0 and arr.size != 1:
        raise ValueError(
            f"exp_val must be a scalar, got shape {arr.shape}. "
            f"Use result[0].data.evs (not result.data.evs) for a single expectation value."
        )
    exp_val = float(arr.flat[0])
    _grade(exp_val, "ex1")
```
