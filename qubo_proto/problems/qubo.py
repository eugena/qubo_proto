import numpy as np

import dimod
from networkx import nx

import qubo_proto
from qubo_proto.problems.base import ProblemSolver


class ProblemQUBO(ProblemSolver):
    """
    Concrete Class of solving QUBO problems
    """
    @staticmethod
    def prepare_model(*args, **kwargs) -> dimod.BinaryQuadraticModel:
        """
        Instantiate BinaryQuadraticModel according to received data
        """
        data = kwargs.pop('data')

        model = data

        if isinstance(data, nx.Graph):
            model = dimod.BinaryQuadraticModel.from_networkx_graph(
                data, **kwargs)
        elif isinstance(data, np.ndarray):
            model = dimod.BinaryQuadraticModel.from_numpy_matrix(
                data, **kwargs)
        elif isinstance(data, tuple):
            h, J = data
            model = dimod.BinaryQuadraticModel.from_ising(h, J, **kwargs)
        elif isinstance(data, dict):
            model = dimod.BinaryQuadraticModel.from_qubo(data, **kwargs)

        return model

    def solve(self, *args, **kwargs) -> list:
        """
        Solves the problem
        """
        sampler = self.backend.get_solver(qubo_proto.PROBLEM_QUBO)

        samples = sampler.sample(
            self.prepare_model(*args, **kwargs)
        ).samples(n=1)  # the best one

        try:
            solution = [v for k, v in samples[0].items()]
        except IndexError:
            solution = []
        return solution
