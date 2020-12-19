from dwave.cloud.config import load_config
from dwave.system import DWaveSampler, EmbeddingComposite
from neal import SimulatedAnnealingSampler
from tabu import TabuSampler

import qubo_proto
from qubo_proto.backends.base import Backend


class QuantumBackend(Backend):
    """
    Quantum computer
    """
    def get_solver(self, problem: str):
        """
        Returns a solver object for backend
        """
        if problem == qubo_proto.PROBLEM_QUBO:
            return EmbeddingComposite(
                DWaveSampler(**load_config(profile='defaults'))
            )
        else:
            raise NotImplementedError(f"Object for solving {problem} problem "
                                      f"have to be defined")


class RemoteSimulatorBackend(Backend):
    """
    Remote quantum simulator
    """
    def get_solver(self, problem: str):
        """
        Returns a solver object for backend
        """
        if problem == qubo_proto.PROBLEM_QUBO:
            return DWaveSampler(**load_config(profile='sw-solver'))
        else:
            raise NotImplementedError(f"Object for solving {problem} problem "
                                      f"have to be defined")


class LocalSimulatorBackend(Backend):
    """
    Local quantum simulator
    """
    def get_solver(self, problem: str):
        """
        Returns a solver object for backend
        """
        if problem == qubo_proto.PROBLEM_QUBO:
            return SimulatedAnnealingSampler()
        else:
            raise NotImplementedError(f"Object for solving {problem} problem "
                                      f"have to be defined")


class ClassicBackend(Backend):
    """
    Classic backend
    """
    def get_solver(self, problem: str):
        """
        Returns a solver object for backend
        """
        if problem == qubo_proto.PROBLEM_QUBO:
            return TabuSampler()
        else:
            raise NotImplementedError(f"Object for solving {problem} problem "
                                      f"have to be defined")
