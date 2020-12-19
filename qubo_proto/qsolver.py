from qubo_proto.problems.factory import ProblemFactory


class QSolver:
    """
    Class for solving problems using quantum computation
    """
    def __init__(self, backend: str):
        """
        Initializes an instance

        @param backend str
        """
        self.backend = backend

    def solve(self, problem: str, *args, **kwargs):
        """
        Solves a problems

        @param problem str
        """
        return ProblemFactory.factory_method(
            self.backend, problem).solve(*args, **kwargs)
