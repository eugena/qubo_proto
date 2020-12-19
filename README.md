QUBO solving prototype
======================

[![License: GPL v3](https://img.shields.io/badge/license-GPL%20v3-blue.svg)](LICENSE)

This is a prototype for solving [QUBO](https://en.wikipedia.org/wiki/Quadratic_unconstrained_binary_optimization) problem
using several backends.

Currently, tested for Python 3.6, 3.7, 3.8.

Features
--------
1. Can use several backends:
    * Adiabatic quantum computer
    * Quantum simulator
    * Classic backend
2. Can translate input into the QUBO basis
3. Can convert a basis from Ising to QUBO and vise versa
4. Can consider additional restrictions

Quick start
-----------

In terminal:

```shell
git clone https://github.com/eugena/qubo_proto.git

cd qubo_proto

virtualenv .qubo

source .qubo/bin/activate

pip install -r requirements_dev.txt
````

Then fill **tokens** and **endpoints** in [dwave.conf](dwave.conf).


Then:
```shell
python
````

And in python:

```python
import numpy as np
import qubo_proto

qubo_proto.QSolver(
    backend=qubo_proto.BACKEND_QUANTUM
).solve(
    qubo_proto.PROBLEM_QUBO,
    data=np.random.rand(5, 5)
)
```
You should get a list like this as a solution:
```python
[1, 0, 0, 1, 1]
```

Testing
-------

Test coverage:

```shell
coverage run -m pytest && coverage report
```

Running tests:

```shell
tox
```

Please, see [tox project](https://tox.readthedocs.io/en/latest/) and [tox.ini](tox.ini) for more details.
