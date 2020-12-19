#!/usr/bin/env python
"""
Tests for `qubo_proto` package.
"""
import operator
import numpy as np

import dimod
import dwavebinarycsp

import qubo_proto


def test_backend_quantum():
    """
    Simple test function for QUANTUM backend
    """
    result = qubo_proto.QSolver(
        backend=qubo_proto.BACKEND_QUANTUM
    ).solve(
        qubo_proto.PROBLEM_QUBO,
        data=np.random.rand(5, 5)
    )

    assert isinstance(result, list)


def _test_backend_remote_simulator():
    """
    Simple test function for REMOTE SIMULATOR backend

    Warning: uncomment after filling of [sw-solver] section
    """
    result = qubo_proto.QSolver(
        backend=qubo_proto.BACKEND_REMOTE_SIMULATOR
    ).solve(
        qubo_proto.PROBLEM_QUBO,
        data=np.random.rand(10, 10))

    assert isinstance(result, list)


def test_backend_local_simulator():
    """
    Simple test function for LOCAL SIMULATOR backend
    """
    result = qubo_proto.QSolver(
        backend=qubo_proto.BACKEND_LOCAL_SIMULATOR
    ).solve(
        qubo_proto.PROBLEM_QUBO,
        data=np.random.rand(10, 10))

    assert isinstance(result, list)


def test_backend_classic():
    """
    Simple test function for CLASSIC backend
    """
    result = qubo_proto.QSolver(
        backend=qubo_proto.BACKEND_CLASSIC
    ).solve(
        qubo_proto.PROBLEM_QUBO,
        data=np.random.rand(5, 5))

    assert isinstance(result, list)


def test_backend_unknown():
    """
    Simple test function for unknown backend
    """
    try:
        qubo_proto.QSolver(
            backend='unknown'
        ).solve(
            qubo_proto.PROBLEM_QUBO,
            data=np.random.rand(5, 5))
    except BaseException as e:
        assert isinstance(e, NotImplementedError)


def test_problem_unknown():
    """
    Simple test function for unknown problem
    """
    try:
        qubo_proto.QSolver(
            backend=qubo_proto.BACKEND_LOCAL_SIMULATOR
        ).solve(
            'unknown',
            data=np.random.rand(5, 5))
    except BaseException as e:
        assert isinstance(e, NotImplementedError)


def test_ising():
    """
    Simple test function for Ising problem

    When
        h = {0: -1, 1: -1}
        J = {(0, 1): -1}
    :
        data=({0: -1, 1: -1}, {(0, 1): -1})
    """
    result = qubo_proto.QSolver(
        backend=qubo_proto.BACKEND_LOCAL_SIMULATOR
    ).solve(
        qubo_proto.PROBLEM_QUBO,
        data=({0: -1, 1: -1}, {(0, 1): -1})
    )

    assert isinstance(result, list)


def test_qubo():
    """
    Simple test function for QUBO
    """
    result = qubo_proto.QSolver(
        backend=qubo_proto.BACKEND_LOCAL_SIMULATOR
    ).solve(
        qubo_proto.PROBLEM_QUBO,
        data={(0, 0): -1, (1, 1): -1, (0, 1): 2}
    )

    assert isinstance(result, list)


def test_bqm():
    """
    Simple test function for BinaryQuadraticModel
    """
    result = qubo_proto.QSolver(
        backend=qubo_proto.BACKEND_LOCAL_SIMULATOR
    ).solve(
        qubo_proto.PROBLEM_QUBO,
        data=dimod.BinaryQuadraticModel(
            {0: 1, 1: -1, 2: .5},
            {(0, 1): .5, (1, 2): 1.5},
            1.4,
            dimod.Vartype.SPIN
        )
    )

    assert isinstance(result, list)


def test_results_is_equal():
    """
    Checks whether the results from different backends are equal
    """
    model = dimod.BinaryQuadraticModel(
        {0: 1, 1: -1, 2: .5},
        {(0, 1): .5, (1, 2): 1.5},
        1.4,
        dimod.Vartype.SPIN
    )

    result_q = qubo_proto.QSolver(
        backend=qubo_proto.BACKEND_QUANTUM
    ).solve(
        qubo_proto.PROBLEM_QUBO,
        data=model
    )

    result_s = qubo_proto.QSolver(
        backend=qubo_proto.BACKEND_LOCAL_SIMULATOR
    ).solve(
        qubo_proto.PROBLEM_QUBO,
        data=model
    )

    result_c = qubo_proto.QSolver(
        backend=qubo_proto.BACKEND_CLASSIC
    ).solve(
        qubo_proto.PROBLEM_QUBO,
        data=model
    )

    assert result_q == result_s
    assert result_q == result_c


def test_convert_ising_to_qubo():
    """
    Checks ising to qubo convertation
    """
    h = {0: -1, 1: -1}
    J = {(0, 1): -1}
    Q, offset = dimod.ising_to_qubo(h, J, 0.5)
    h1, J1, offset = dimod.qubo_to_ising(Q, offset)
    assert h == h1
    assert J == J1

    result_qubo = qubo_proto.QSolver(
        backend=qubo_proto.BACKEND_LOCAL_SIMULATOR
    ).solve(
        qubo_proto.PROBLEM_QUBO,
        data=Q,
        offset=offset
    )

    result_ising = qubo_proto.QSolver(
        backend=qubo_proto.BACKEND_LOCAL_SIMULATOR
    ).solve(
        qubo_proto.PROBLEM_QUBO,
        data=(h, J),
        offset=offset
    )

    assert result_ising == result_qubo


def test_constraint_satisfaction_problem():
    """
    Checks Constraint Satisfaction Problems solving
    """

    # Constraint 1
    #
    # for solution:
    #   the element with index 0 must be less then
    #   the element with index 1
    #   and
    #   the element with index 1 must be not equal to
    #   the element with index 2
    csp = dwavebinarycsp.ConstraintSatisfactionProblem('BINARY')
    csp.add_constraint(operator.lt, [0, 1])
    csp.add_constraint(operator.ne, [1, 2])

    assert csp.check({0: 0, 1: 1, 2: 0})
    assert not csp.check({0: 1, 1: 1, 2: 1})

    result_csp = qubo_proto.QSolver(
        backend=qubo_proto.BACKEND_LOCAL_SIMULATOR
    ).solve(
        qubo_proto.PROBLEM_QUBO,
        data=dwavebinarycsp.stitch(csp)  # getting BinaryQuadraticModel
                                         # as input
    )

    assert csp.check(result_csp)

    # Constraint 2
    #
    # for solution s:
    #   s * A <= b
    # where
    #   A is nxn matrix;
    #   b is vector with size n
    csp = dwavebinarycsp.ConstraintSatisfactionProblem('BINARY')

    csp.add_constraint(
        lambda a, b, c: all(np.array(
            [a, b, c]
        ).T.dot(np.random.rand(3, 3)) < np.random.rand(3)),
        ['a', 'b', 'c'])

    result_csp = qubo_proto.QSolver(
        backend=qubo_proto.BACKEND_LOCAL_SIMULATOR
    ).solve(
        qubo_proto.PROBLEM_QUBO,
        data=dwavebinarycsp.stitch(csp),  # getting BinaryQuadraticModel
                                          # as input
        num_reads=5
    )

    assert isinstance(result_csp, list)

    if len(result_csp) > 1:
        for s in result_csp:
            assert type(
                csp.check(dict(zip(['a', 'b', 'c'], s)))) == bool
    else:
        assert type(
            csp.check(dict(zip(['a', 'b', 'c'], result_csp)))) == bool
