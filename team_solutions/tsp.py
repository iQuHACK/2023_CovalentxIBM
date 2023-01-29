import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

# Importing standard Qiskit libraries
from qiskit_aer import Aer
from qiskit.tools.visualization import plot_histogram
from qiskit.circuit.library import TwoLocal
from qiskit_optimization.applications import Maxcut, Tsp
from qiskit.algorithms.minimum_eigensolvers import SamplingVQE, NumPyMinimumEigensolver
from qiskit.algorithms.optimizers import SPSA
from qiskit.utils import algorithm_globals
from qiskit.primitives import Sampler
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit_optimization.algorithms import MinimumEigenOptimizer

@ct.electron
def sample_most_likely(
        state_vector: Union[QuasiDistribution, Statevector, np.ndarray, Dict]
    ) -> np.ndarray:
        """Compute the most likely binary string from state vector.

        Args:
            state_vector: state vector or counts or quasi-probabilities.

        Returns:
            binary string as numpy.ndarray of ints.

        Raises:
            ValueError: if state_vector is not QuasiDistribution, Statevector,
                np.ndarray, or dict.
        """
        if isinstance(state_vector, QuasiDistribution):
            probabilities = state_vector.binary_probabilities()
            binary_string = max(probabilities.items(), key=lambda kv: kv[1])[0]
            x = np.asarray([int(y) for y in reversed(list(binary_string))])
            return x
        elif isinstance(state_vector, Statevector):
            probabilities = state_vector.probabilities()
            n = state_vector.num_qubits
            k = np.argmax(np.abs(probabilities))
            x = np.zeros(n)
            for i in range(n):
                x[i] = k % 2
                k >>= 1
            return x
        elif isinstance(state_vector, (OrderedDict, dict)):
            # get the binary string with the largest count
            binary_string = max(state_vector.items(), key=lambda kv: kv[1])[0]
            x = np.asarray([int(y) for y in reversed(list(binary_string))])
            return x
        elif isinstance(state_vector, StateFn):
            binary_string = list(state_vector.sample().keys())[0]
            x = np.asarray([int(y) for y in reversed(list(binary_string))])
            return x
        elif isinstance(state_vector, np.ndarray):
            n = int(np.log2(state_vector.shape[0]))
            k = np.argmax(np.abs(state_vector))
            x = np.zeros(n)
            for i in range(n):
                x[i] = k % 2
                k >>= 1
            return x
        else:
            raise ValueError(
                "state vector should be QuasiDistribution, Statevector, ndarray, or dict. "
                f"But it is {type(state_vector)}."
            )
@ct.lattice
def tsp(A):
    G = nx.from_numpy_matrix(A)
    tsp = Tsp(G)     
    # Mapping to the Ising problem and creating a Hamiltonian to solve
    qp = tsp.to_quadratic_program()
    qp2qubo = QuadraticProgramToQubo()
    qubo = qp2qubo.convert(qp)
    qubitOp, offset = qubo.to_ising()

    # Making the Hamiltonian in its full form and getting the lowest eigenvalue and eigenvector
    ee = NumPyMinimumEigensolver()
    result = ee.compute_minimum_eigenvalue(qubitOp)
    x = sample_most_likely(result.eigenstate)
    
    order = tsp.interpret(x)
    cost = tsp.tsp_value(order, A)
    return order, cost
