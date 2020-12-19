import qubo_proto

from qubo_proto.backends.base import Backend
from qubo_proto.backends.backend import (
    QuantumBackend, RemoteSimulatorBackend, LocalSimulatorBackend,
    ClassicBackend
)


class BackendFactory:
    """
    Backend Factory
    """
    @staticmethod
    def factory_method(backend: str) -> Backend:
        if backend == qubo_proto.BACKEND_QUANTUM:
            return QuantumBackend()
        elif backend == qubo_proto.BACKEND_LOCAL_SIMULATOR:
            return LocalSimulatorBackend()
        elif backend == qubo_proto.BACKEND_REMOTE_SIMULATOR:
            return RemoteSimulatorBackend()
        elif backend == qubo_proto.BACKEND_CLASSIC:
            return ClassicBackend()
        else:
            raise NotImplementedError(f"Backend {backend} "
                                      f"is not implemented yet")
