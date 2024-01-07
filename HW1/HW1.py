from Hanoi import hanoi3
from Jedi import tjp, tjp_num, tjp_num_opt
from Drones import drones, drones_opt

# Question 1: Tower of Hanoi [Classic]
print("Question 1 Solution: ")
hanoi3.main()

# Question 2.1: Travelling Jedi Problem [Classic]
print("\nQuestion 2.1 Solution: ")
tjp.main()

# Question 2.2: Travelling Jedi Problem [Numeric]
print("\nQuestion 2.2 Solution: ")
tjp_num.main()

# Question 2.3: Travelling Jedi Problem [Optimal Numeric]
print("\nQuestion 2.3 Solution: ")
tjp_num_opt.main()

# Question 3.1: Googazon Drone Delivery Service [Temporal]
print("\nQuestion 3.1 Solution: ")
drones.main()

# Question 3.2: Googazon Drone Delivery Service [Optimal Temporal]
print("\nQuestion 3.2 Solution: ")
drones_opt.main()