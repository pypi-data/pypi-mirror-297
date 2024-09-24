def help():
    print("Welcome to QuCAT!")
    print("\n")
    print("You can provide the root of the configuration to run qucat.")
    print("Here is the template of the configuration file.")

    template = '''
[program]
root= 
;(Required)
;Description: The absolute root of your quantum program file.
num_qubit= 
;(Required)
;Description: The total number of qubit of your quantum program.
inputID= 
;(Required)
;Description: The IDs of input qubits.
;Format: A non-repeating sequence separated by commas.
outputID= 
;(Required)
;Description: The IDs of output qubits which are the qubits to be measured.
;Format: A non-repeating sequence separated by commas.

[qucat_configuration]
pict_root=
;(Required)
;Description: The root to run pict.
k=
;(Optional)
;Description: Order of combinations. In Functionality Two, it refers to the maximum value of strength. k = 2 by default. 
significance_level=
;(Optional)
;Description: The significance level for statistical test. significance_level = 0.01 by default.

[program_specification]
;Description: The program specification.
;Format:input string (binary),output string (binary)=probability
;Example:
;00,1=0.5
;00,0=0.5
;01,1=0.5
;01,0=0.5
;or
;0-,-=0.5
;Attention: '-' can refer to both '0' and '1'.
'''
    print(template)
    print('\n')

    print("Here is the example of the configuration file and the quantum program file.")

    example = '''
[program]
root=/User/entanglement.py
num_qubit=2
inputID=0,1
outputID=0,1

[qucat_configuration]
pict_root=.
k=2
significance_level=0.01

[program_specification]
00,00=0.5
00,11=0.5
01,00=0.5
01,11=0.5
10,01=0.5
10,10=0.5
11,01=0.5
11,10=0.5
'''
    program = '''
import math

def run(qc):
    qc.h(4)
    qc.p(math.pi/3, 4)
    qc.mct([5,7, 9,11],12)  # M3
    qc.h(4)

    qc.barrier()

    qc.cswap(4, 5, 9)
    qc.cswap(4, 6, 10)
    qc.cswap(4, 7, 11)
    qc.cswap(4, 8, 12)

    qc.barrier()

    qc.swap(0, 5)
    qc.swap(1, 6)
    qc.swap(2, 7)
    qc.swap(3, 8)

    qc.barrier()

    qc.mcx([0,1,2], 3)
    qc.mcx([0,1], 2)
    qc.cx(0, 1)
    qc.x(0)

    qc.barrier()

    qc.measure([0, 1, 2, 3], [0, 1, 2, 3])
    '''
    print(example)
    print("Here is the example of the quantum program file.")
    print(program)

if __name__ == '__main__':
    help()



