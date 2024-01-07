from unified_planning.shortcuts import *
from unified_planning.io import PDDLWriter

# TODO: Add any helper functions and libraries you need

def main():
    # TODO: Represent and solve the Googazon Drone Delivery Service (temporal) problem using the UPF
    problem_drones = None
    
    # Writing the PDDl files
    w = PDDLWriter(problem_drones)
    w.write_domain('Drones/domain_upf_drones.pddl')
    w.write_problem('Drones/problem_upf_drones.pddl')
    return

if __name__ == '__main__':
    main()