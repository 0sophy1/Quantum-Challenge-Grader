# Quantum Challenge Grader

Grading client for the IBM Quantum Challenge grading service.


## Requirements

- [IBM Quantum Platform account](https://quantum.cloud.ibm.com/)
- [Python](https://www.python.org/) 3.10 or later, with a
  [Jupyter Notebook](https://jupyter.org/install) or
  [JupyterLab](https://jupyterlab.readthedocs.io/en/stable/getting_started/installation.html)
  environment
- Qiskit 2.x (installed automatically as a dependency)


## Installation

Install the grading client into your Python environment:

```sh
pip install qc-grader
```


## Authentication

The grader authenticates with your IBM Quantum Platform API key. You can provide
it in either of two ways.

### Option 1 — Save your account (recommended)

If you already use `QiskitRuntimeService` and have saved your account by
following the
[setup instructions](https://quantum.cloud.ibm.com/docs/en/guides/hello-world#install-and-authenticate),
the grader reuses that saved account automatically — no extra configuration
needed.

To save your account:

```python
from qiskit_ibm_runtime import QiskitRuntimeService

QiskitRuntimeService.save_account(
    channel="ibm_quantum_platform",
    token="<YOUR_API_KEY>",
    set_as_default=True,
    overwrite=True,
)
```

Your API key is available on your
[IBM Quantum Platform account page](https://quantum.cloud.ibm.com/).

### Option 2 — Set the `QC_API_KEY` environment variable

From a terminal, before launching Jupyter:

```sh
export QC_API_KEY=your_api_key
```

Alternatively, run this at the top of a notebook (re-run whenever you
start/restart the kernel):

```python
%set_env QC_API_KEY=your_api_key
```

> **Note:** You can confirm the environment variable is set by running the
> following in a notebook cell:
>
> ```python
> import os
> print(os.getenv("QC_API_KEY"))
> ```


## Usage

1. Open an exercise notebook for the challenge you are participating in.

2. Run the notebook cells, completing the exercises. Each exercise has a grading
   function that you import and call with your solution. Grading functions
   follow the pattern `grade_<module>_ex<n>` and live under
   `qc_grader.challenges.<challenge>`. For example:

   ```python
   from qc_grader.challenges.<challenge> import grade_<module>_ex1

   grade_<module>_ex1(answer_1)
   ```

   Replace `<challenge>` with the challenge you are working on (e.g.
   `fallfest_2026`, `qgss_2026`), and `<module>`/`ex<n>` with the exercise you
   are submitting. The specific imports are given in each notebook.

3. To review how many exercises you have completed so far, use the
   `check_progress` helper exposed by each challenge:

   ```python
   from qc_grader.challenges.<challenge> import check_progress

   check_progress()
   ```


## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup (`uv`, `just`),
linting, tests, and the release process.
