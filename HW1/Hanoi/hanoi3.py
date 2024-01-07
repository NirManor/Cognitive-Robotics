from unified_planning.shortcuts import *
from unified_planning.io import PDDLWriter

# TODO: Add any helper functions and libraries you need

def main():
    # TODO: Represent and solve the Tower of Hanoi problem (for N=3) using the UPF
    problem_hanoi = None

    # Writing the PDDl files
    w = PDDLWriter(problem_hanoi)
    w.write_domain('Hanoi/domain_upf_hanoi.pddl')
    w.write_problem('Hanoi/problem_upf_hanoi3.pddl')    
    return

if __name__ == '__main__':
    main()