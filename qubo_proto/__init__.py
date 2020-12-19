"""
Top-level package for qubo-proto.
"""

__author__ = """Eugena A. Mihailikova"""
__email__ = 'eugena.mihailikova@gmail.com'
__version__ = '0.1.0'

PROBLEM_QUBO = 'QUBO'

BACKEND_QUANTUM = 'quantum'
BACKEND_REMOTE_SIMULATOR = 'remote_simulator'
BACKEND_LOCAL_SIMULATOR = 'local_simulator'
BACKEND_CLASSIC = 'classic'

from qubo_proto.qsolver import QSolver
