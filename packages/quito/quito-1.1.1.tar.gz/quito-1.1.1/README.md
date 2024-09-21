# Quito: a Coverage-Guided Test Generator for Quantum Programs

<img src="Logo.png" width="200">

## Description
Automation in quantum software testing is essential to support systematic and cost-effective testing. Towards this direction, we present a quantum software testing tool called Quito that can automatically generate test suites covering three coverage criteria defined on inputs and outputs of a quantum program coded in Qiskit, i.e., input coverage, output coverage, and input-output coverage. Quito also implements two types of test oracles based on program specifications, i.e., checking whether a quantum program produced a wrong output or checking a probabilistic test oracle with statistical test.


## Architecture of Quito


<!---
your comment goes here
and here
![Architecture](https://github.com/EnautMendi/QuantumMutationQiskit/blob/master/images/architecture.png)

-->

<img src="quito.png" width="1000">

## Testing Process

<img src="algorithm.png" width="600">


## How to use Quito?
### Quantum Program File
- The quantum program should be written with Qiskit.
- The code has to be structured in a function named as 'run' with one parameter that refers to the quantum circuit.
- Users only need to add gates to the circuit and measure output qubits to get the output. They don't need to set any register, initialize circuits, choose the simulation, or execute the circuits in 'run' function.

A sample quantum program:
```
def run(qc):
    qc.h(2)
    qc.cswap(2,0,1)
    qc.h(2)
    qc.x(2)

    qc.measure(2,0)
```


### Configuration File
The configuration file should be written in an INI file.
The configuration file is described below.
```
[program]
root=SWAP.py
;(Required)
;Description: The absolute root of your quantum program file.
num_qubit=3
;(Required)
;Description: The total number of qubits of your quantum program.
inputID=0,1
;(Required)
;Description: The ID of input qubits.
;Format: A non-repeating sequence separated by commas.
outputID=2
;(Required)
;Description: The ID of output qubits which are the qubits to be measured.
;Format: A non-repeating sequence separated by commas.

[program_specification_category]
ps_category=full
;(Required)
;Description: The category of your program specification.
;Choice: full/partial/no

[quito_configuration]
coverage_criterion=IC
;Description: The coverage criterion you choose.
;Choice: IC/OC/IOC
K=200
;(Optional)
;Description: The total number of test suites, K=200 by default.
M=20
;(Optional)
;Description: The number of test suite groups, M=20 by default.
BUDGET=20
;(Optional)
;Description: The budget of the number of test cases in one test suite, BUDGET=10*number of inputs by default.
confidence_level=0.01
;(Optional)
;Description: The confidence level for statistical test, confidence_level=0.01 by default.
statistical_test=one-sample Wilcoxon signed rank test   
;(Optional)
;Description: The statistical test for assessment, statistical_test=one-sample Wilcoxon signed rank test by default.

[program_specification]
;(Required for full and partial program specification)
;Description: The program specification.
;Format:input string,output string=probability
01,1=0.5
01,0=0.5
00,1=1
11,1=1
10,1=0.5
10,0=0.5
```

If users provide a full or partial program specification, Quito will assess the results according to the two test oracles that have been proposed in <a href="https://ieeexplore.ieee.org/abstract/document/9438603">this paper</a>:
- WOO: Whether an observed output is correct according to program specification. If not, the program is failed;
- OPO: If all the observed outputs corresponding to an input are valid, then it compares their observed probabilities with the ones specified in the Program Specification file. If the differences are statistically significant (i.e., a p-value lower than the chosen significance level), the program is failed.

You can provide the root of the configuration file and run Quito.

```
from quito.quito_coverage import quito

quito("configuration.ini")
```

After running, you get 3 text files (2 in case there is no program specification). They contain
- Test Suites
- Test Execution Results
- Assessment Results (for full and partial program specification)

You can also type in 'quito' at your terminal to see the help.

## Video Demonstration
A video demo is available <a href="https://www.youtube.com/watch?v=kuI9QaCo8A8" target=_blank>here</a>.

## Paper
X. Wang, P. Arcaini, T. Yue, and S. Ali. Quito: a Coverage-Guided Test Generator for Quantum Programs. In 36th IEEE/ACM International Conference on Automated Software Engineering - Tool Demonstrations track [[doi](https://doi.org/10.1109/ASE51524.2021.9678798)]