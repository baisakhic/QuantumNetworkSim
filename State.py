from qiskit.quantum_info import DensityMatrix, partial_trace
import qiskit.quantum_info as qi
import numpy as np
import math

# state label = 0: |PHI+> = 1/sqrt(2) * [1, 0, 0, 1]
# state label = 1: 0.7*|PHI+><PHI+| + 0.15*|01><01| + 0.15*|10><10|
# state label = 2: |phi> = 1/sqrt(5)|00> + 2/sqrt(5)|11>
# state label = 3: 0.7*|phi><phi| + 0.15*|01><01| + 0.15*|10><10|

dm0 = DensityMatrix([1/np.sqrt(2), 0, 0, 1/np.sqrt(2)])
dm1 = 0.7*dm0 + (0.15*DensityMatrix([0, 1, 0, 0])) + (0.15*DensityMatrix([0, 0, 1, 0]))
dm2 = DensityMatrix([1/np.sqrt(5), 0, 0, 2/np.sqrt(5)])
dm3 = 0.7*dm2 + (0.15*DensityMatrix([0, 1, 0, 0])) + (0.15*DensityMatrix([0, 0, 1, 0]))

STATE_MAP = {0: dm0, 1: dm1, 2: dm2, 3: dm3}


array_zero = np.array([1, 0])
array_one = np.array([0, 1])


BASIS_MAP = {"H": array_zero, "V": array_one}
RESULT_MAP = {0: array_zero, 1: array_one}
BASIS_STATE_MAP = {"H": 0, "V": 1, "Z": 0, "X": 1}

I = qi.Operator.from_label("I")
H = qi.Operator.from_label("H")

def rotation_operator(theta):
    return qi.Operator(np.array([[np.cos(theta/2), -np.sin(theta/2)],[np.sin(theta/2), np.cos(theta/2)]]))

class State:

    def __init__(self, label: int=0):
        self.label = label
        self.dm = STATE_MAP[self.label]

        self.alice_dm = None
        self.bob_dm = None

        self.alice_measure_val = None
        self.bob_measure_val = None

    def measure(self, receiver, basis, angle=None):
        if receiver == "A":
            return self.alice_measure(basis, angle)
        else:
            return self.bob_measure(basis, angle)

    def alice_measure(self, basis, angle):
        if self.bob_dm != None:
            # This will only happen if Bob's Density Matrix is set, which will only happen (code-wise) if Bob has measured. 
            # print(F"Full DM: {self.dm}")
            # self.alice_dm = DensityMatrix(qi.Operator(np.kron(I.data, BASIS_MAP[basis])) @ self.dm @ qi.Operator(np.kron(I.data, BASIS_MAP[basis].reshape((2, 1)))))/np.trace(qi.Operator(np.kron(DensityMatrix(BASIS_MAP[basis]), I))@self.dm)
            # print(self.alice_dm.probabilities_dict())
            # print(F"Alice's DM: {self.alice_dm}, basis: {basis}")
            self.alice_measure_val = result = int(self.alice_dm.measure()[0])
            # print("Measuring Alice")
            # print("Alice = " + str(self.alice_measure_val) + " :: Bob = " + str(self.bob_measure_val))
            # print("Basis = " + basis + " :: Basis Value = " + str(BASIS_STATE_MAP[basis]))
            # print("Result = " + str(result))
            # print("T/F = " + str(result == BASIS_STATE_MAP[basis]))
            if str(result) in self.alice_dm.probabilities_dict().keys() \
                and not math.isnan(self.alice_dm.probabilities_dict()[str(result)]) \
                and self.alice_dm.probabilities_dict()[str(result)] > 0:
                return True
            else:
                return False
        else:
            # This will only happen if nothing has been done to this state - the Density Matrix is as created by the ES
            if angle != None:
                # perform bell inequality test if this angle is given:
                # Apply rotation gate (tensored with Identity) before measuring 
                # Also, if measuring in X basis, apply Hadamard before measuring
                rotation = rotation_operator(angle)
                self.dm = self.dm.evolve(rotation ^ I)
                if basis == "X":
                    self.dm = self.dm.evolve(H^I)
                # print("we are performing bell inequality test")
            # Partial_trace(dm, [0]) = Alice's PRE-measurement density matrix
            self.alice_dm = partial_trace(self.dm, [0])
            # This value will hold the measurement Alice's qubit - (note: measure()[1] is Alice's POST-measurement DM)
            self.alice_measure_val = result = int(self.alice_dm.measure()[0])
            # After measurement, the State's original DM (created by ES) collapses to a 1-qubit state held by Bob.
            # This State object needs to know what the 1-qubit state held by Bob looks like AFTER Alice measures her qubit
            # We find that using rho_b = (<x|_A ^ I_B)@rho_dm@(|x>_A ^ I_B) / trace(|x><x| ^ I @ rho_dm)
            # where x = {0, 1} according to Alice's measurement, thus trace(|x><x| ^ I @ rho_dm) = probability of measuring |x> and (<x|_A ^ I_B)@rho_dm@(|x>_A ^ I_B) is almost a "partial"-partial trace
            self.bob_dm = DensityMatrix(qi.Operator(np.kron(RESULT_MAP[self.alice_measure_val], I.data)) @ self.dm @ qi.Operator(np.kron(RESULT_MAP[self.alice_measure_val].reshape((2, 1)), I.data)))/np.trace(qi.Operator(np.kron(DensityMatrix(RESULT_MAP[self.alice_measure_val]), I))@self.dm)

            # Now, this state has Alice's measurement result, Alice's PRE-measurement DM and Bob's POST-measurement DM
            
            # print(F"In else of alice_measure, bobs's dm: {self.bob_dm}")
            # print(F"Alice's DM: {self.alice_dm}")
            # print("Alice = " + str(self.alice_measure_val) + " :: Bob = " + str(self.bob_measure_val))
            # print(F"Basis: {basis}")
            if str(result) in self.alice_dm.probabilities_dict().keys() \
                    and not math.isnan(self.alice_dm.probabilities_dict()[str(result)]) \
                    and self.alice_dm.probabilities_dict()[str(result)] > 0:
                return True
            else:
                return False


    def bob_measure(self, basis, angle):
        if self.alice_dm != None:
            # print(F"Full DM: {self.dm}")
            # self.bob_dm = DensityMatrix(qi.Operator(np.kron(BASIS_MAP[basis], I.data)) @ self.dm @ qi.Operator(np.kron(BASIS_MAP[basis].reshape((2, 1)), I.data)))/np.trace(qi.Operator(np.kron(DensityMatrix(BASIS_MAP[basis]), I))@self.dm)
            # print(F"Bob's DM: {self.bob_dm}, basis: {basis}")
            # print(F"bob_measure_val = {int(self.bob_dm.measure()[0])}")
            self.bob_measure_val = result = int(self.bob_dm.measure()[0])
            # print(F"Value of result variable: {result}")
            # print(self.bob_dm.probabilities_dict())
            # print("Measuring Bob")
            # print("Alice = " + str( self.alice_measure_val) + " :: Bob = " +  str(self.bob_measure_val))
            # print("Basis = " + basis + " :: Basis Value = " + str(BASIS_STATE_MAP[basis]))
            # print("Result = " + str(result))
            # print("T/F = " + str(int(result) == int(BASIS_STATE_MAP[basis])))
            # print(F"Bob's DM: {self.bob_dm}")
            # print(F"Alice's DM: {self.alice_dm}")

            if str(result) in self.bob_dm.probabilities_dict().keys() \
                    and not math.isnan(self.bob_dm.probabilities_dict()[str(result)]) \
                    and self.bob_dm.probabilities_dict()[str(result)] > 0:
                return True
            else:
                return False
        else:
            # if measuring in X basis, apply Hadamard before measuring
            if basis == "X":
                self.dm = self.dm.evolve(I^H)
            self.bob_dm = partial_trace(self.dm, [0])
            self.bob_measure_val = result = int(self.bob_dm.measure()[0])
            self.alice_dm = DensityMatrix(qi.Operator(np.kron(I.data, RESULT_MAP[self.bob_measure_val])) @ self.dm @ qi.Operator(np.kron(I.data, RESULT_MAP[self.bob_measure_val].reshape((2, 1)))))/np.trace(qi.Operator(np.kron(DensityMatrix(RESULT_MAP[self.bob_measure_val]), I))@self.dm)
            # print(F"In else of bob_measure, alice's dm: {self.alice_dm}")
            # print("Alice = " + str(self.alice_measure_val) + " :: Bob = " + str(self.bob_measure_val))
            if str(result) in self.bob_dm.probabilities_dict().keys() \
                    and not math.isnan(self.bob_dm.probabilities_dict()[str(result)]) \
                    and self.bob_dm.probabilities_dict()[str(result)] > 0:
                return True
            else:
                return False



    
