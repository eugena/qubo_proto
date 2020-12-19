from abc import ABCMeta

from qubo_proto.backends.factory import BackendFactory


class ProblemSolver(metaclass=ABCMeta):
    """
    Abstract problem solver
    """
    def __init__(self, backend: str):
        self.backend = BackendFactory.factory_method(backend)

    def solve(self, *args, **kwargs):
        NotImplementedError("Method 'solve' have to be implemented in "
                            "child classes")
