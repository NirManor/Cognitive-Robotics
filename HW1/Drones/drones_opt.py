from unified_planning.shortcuts import *

# TODO: Add any helper functions and libraries you need

def main():
    goal1 = ['C1','milk'] # Customer 1 wants milk
    goal2 = ['C5','sugar'] # Customer 5 wants sugar
    best_duration = 1000 # Initiate at an arbitrarily high value
    best_solution = None # This should be a dictionary with the drones as keys and the goals as values
    
    # TODO: Write an optimization process that will return the shortest duration possible for
    ## any plan and a dictionary containing the drones+goals combo that produces the optimal plan
    
    print(f"\nMinimal Time Found: {best_duration} minutes")
    print("Best Solution:")
    print(best_solution)
    return

if __name__ == '__main__':
    main()