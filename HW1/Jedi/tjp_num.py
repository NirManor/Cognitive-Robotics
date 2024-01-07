from unified_planning.shortcuts import *
from unified_planning.io import PDDLWriter

# TODO: Add any helper functions and libraries you need

def main():
    # TODO: Represent and solve the numeric Travelling Jedi Problem using the UPF
    problem_tjp_num = None

    # Writing the PDDl files
    w = PDDLWriter(problem_tjp_num)
    w.write_domain('Jedi/domain_upf_tjp_num.pddl')
    w.write_problem('Jedi/problem_upf_tjp_num.pddl')
    return

if __name__ == '__main__':
    main()