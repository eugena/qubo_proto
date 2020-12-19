from abc import ABCMeta


class Backend(metaclass=ABCMeta):
    """
    Abstract backend
    """
    def get_solver(self, problem: str):
        """
        Returns a solver object for selected backend
        """
        raise NotImplementedError(f"An object for solving {problem} problem "
                                  f"have to be defined in child classes")
