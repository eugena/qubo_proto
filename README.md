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
    * Local quantum simulator
    * Remote quantum simulator
    * Classic backend
2. Can translate input into the QUBO basis
3. Can convert a basis from Ising to QUBO and vise versa
4. Can solve Constraint Satisfaction Problem

Quick Start
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

More Cases
----------

```python
import dimod

import qubo_proto

# dimod.BinaryQuadraticModel as input
model = dimod.BinaryQuadraticModel(
    {0: 1, 1: -1, 2: .5},
    {(0, 1): .5, (1, 2): 1.5},
    1.4,
    dimod.Vartype.SPIN
)

# solution using Quantum computer
result_q = qubo_proto.QSolver(
    backend=qubo_proto.BACKEND_QUANTUM
).solve(
    qubo_proto.PROBLEM_QUBO,
    data=model
)

# solution using Local simulator
result_s = qubo_proto.QSolver(
    backend=qubo_proto.BACKEND_LOCAL_SIMULATOR
).solve(
    qubo_proto.PROBLEM_QUBO,
    data=model
)

# solution using Classic backend
result_c = qubo_proto.QSolver(
    backend=qubo_proto.BACKEND_CLASSIC
).solve(
    qubo_proto.PROBLEM_QUBO,
    data=model
)

# Ising problem to QUBO
h0 = {0: -1, 1: -1}
J0 = {(0, 1): -1}

Q, offset = dimod.ising_to_qubo(h0, J0, 0.5)

result_qubo = qubo_proto.QSolver(
    backend=qubo_proto.BACKEND_LOCAL_SIMULATOR
).solve(
    qubo_proto.PROBLEM_QUBO,
    data=Q,
    offset=offset
)

h, J, offset = dimod.qubo_to_ising(Q, offset)

result_ising = qubo_proto.QSolver(
    backend=qubo_proto.BACKEND_LOCAL_SIMULATOR
).solve(
    qubo_proto.PROBLEM_QUBO,
    data=(h, J),
    offset=offset
)
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
