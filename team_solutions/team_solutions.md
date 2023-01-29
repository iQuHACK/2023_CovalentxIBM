# List of Projects

### Qoalas

- [Code] Qoalas
- [Documentation](https://url_to_documentation.com)

## Repository Directory

#### qRandom
Publishes qoalarandom python library to pyTest 
#### qoalasFlask
Flask application that is deployed to AWS and runs Covalent to generate random numbers between 0-1
#### qraps 
Implementation of the game craps that utilizes the qoalarandom library
#### farqle
Implementation of the game farqle that utilizes the qoalarandom library

# Write Up 
At priori Qoalas is able to adapt to any quantum computer (in particular IBM ones) and to generate random numbers to arbitrary precision, using the best qubits available in the device.

Although, to enhance UX and improve fluidity we offer the option to limit some parameters. For instance, as suggested in the task, there is a protocol to restrict the number of qubits qoalas will use to 7, and the coupling mapping to that of ibm_nairobi.

We selected 4 different ways to implement the random number generator. The first two of which are the most standard methods of number sampling, already present in qiskit.circuit.library; uniform distribution and normal distribution. We adapted these functionalities to work better within Qoalas. The final two on the other hand, are a bit more involved. They use various recent advances in quantum simulation algorithms to construct what is known as a Haar-random state. Essentially, these circuits sample an $n$-qubit state vector from the generalised Bloch sphere for $n$ qubits.

The first of these is the simpler of the two. It uses a circuit inspired by the Google ‘supremacy’ experiments, optimised for IBM hardwares. This algorithm mimics sampling from the Haar measure up to the 2nd moment of the distribution. 	The second method is more deeply connected to quantum simulation and thermodynamics. It involves using maximally entangling 2-qubit interactions in order to spread correlations through the device at the speed of light as it pertains to the circuit (all correlations lie exclusively on the edge of the light cone). We then trace out at least half of the system in order to make use of the resulting projected ensembles of pure states. These states replicate the Haar distribution up to the $k$th moment - so long as we apply at least $k$ layers of these fast scrambling gates. This method is extremely new, and has been named by the community as ‘deep thermalisation’. The resultant distribution of bitstrings in the measurement follow what is known as the Porter-Thompson distribution, which is classically hard to sample from for considering higher moments, as was the intention of the aforementioned claim Google made to quantum supremacy.