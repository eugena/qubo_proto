import qubo_proto

from qubo_proto.problems.qubo import (
    ProblemSolver, ProblemQUBO
)


class ProblemFactory:
    """
    Problems Factory
    """
    @staticmethod
    def factory_method(backend: str, problem: str) -> ProblemSolver:
        """
        Factory method

        @param backend str
        @param problem str
        """
        if problem == qubo_proto.PROBLEM_QUBO:
            return ProblemQUBO(backend)
        else:
            raise NotImplementedError(f"A solver of {problem} "
                                      f"is not implemented yet")
