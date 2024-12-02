import math
import random
from scipy.optimize import minimize

# 1. Hash function implementation
def hash_func(x, a, b, m):
    return (a * x + b) % m

class HashTable:
    # A list 'table' with 'initial_size' elements all set to None
    def __init__(self, initial_size=10, load_factor=0.75):
        self.table = [None] * initial_size
        # Initialize self.size to 0
        self.size = 0
        # Assign load_factor to the given load_factor
        self.load_factor = load_factor

    def insert(self, key, a, b):
        if self.size / len(self.table) > self.load_factor:
            self.rehash(a, b)
        # Computing index using 'hash_func(key, a, b, len(self.table))'
        index = hash_func(key, a, b, len(self.table))
        # If table[index] is None, set table[index] to an empty list
        if self.table[index] is None:
            self.table[index] = []

        if key not in self.table[index]:    # To avoid duplicates
            self.table[index].append(key)  
            self.size += 1

    def rehash(self, a, b):
        old_table = self.table  # Assign 'self.table' to 'old_table'
        new_size = len(self.table) * 2  #size is doubled for new_size
        self.table = [None] * new_size  # List 'self.table' is created with 'new_size' elements, all set to None.
        self.size = 0 # Set 'self.size' to 0

        for cell in old_table:
            if cell is not None:
                for key in cell:
                    # Compute a new index using 'hash_func' with 'new_size'
                    index = hash_func(key, a, b, new_size)
                    # If table[index] is None, set table[index] to an empty list
                    if self.table[index] is None:
                        self.table[index] = []
                    # Key is appended to table[index]
                    self.table[index].append(key)
                    # Incrementing size
                    self.size += 1

def evaluate_hash_table(keys, a, b, m):
    # Instantiate 'hash_table' as a new HashTable with 'initial_size' set to 'm'
    hash_table = HashTable(initial_size=m)
    # Initializing collisions and rehash_count
    collisions = 0
    rehash_count = 0

    # For each 'key' in 'keys'
    for key in keys:
        # Compute load factor before insert
        load_factor_before_insert = hash_table.size / len(hash_table.table)
        # Call 'hash_table.insert(key, a, b)
        hash_table.insert(key, a, b)
        # Compute load factor after insert
        load_factor_after_insert = hash_table.size / len(hash_table.table)

        # Checking for new collisions created after insert
        index = hash_func(key, a, b, len(hash_table.table))
        if len(hash_table.table[index]) > 1:
            collisions += len(hash_table.table[index]) - 1

        # Checking if a rehash occured
        if load_factor_before_insert <= hash_table.load_factor < load_factor_after_insert:
            rehash_count += 1
    return collisions, rehash_count
    
# 3. Optimization techniques
def hill_climbing_optimization(keys, initial_a=1, initial_b=0, initial_m=11, steps=100):
    # Initializing best_a, best_b, best_m to initial_a, initial_b, initial_m
    best_a, best_b, best_m = initial_a, initial_b, initial_m
    # Evaluate with the intial parameters to find 'best_cost'
    best_cost = evaluate_hash_table(keys, best_a, best_b, best_m)[0]

    # In this for loop, we increment 'a', 'b', 'm', by 1
    for _ in range(steps):
        a, b, m = best_a + 1, best_b + 1, best_m + 1
        # Find cost by evaluating the hash table with the new 'a', 'b', 'm'
        cost = evaluate_hash_table(keys, a, b, m)[0]
        # Update 'best_a', 'best_b', 'best_m' with 'a', 'b', 'm'
        # Update 'best_cost' with 'cost'
        if cost < best_cost:
            best_a, best_b, best_m = a, b, m
            best_cost = cost

    return best_a, best_b, best_m, best_cost

def simulated_annealing_optimization(keys, initial_a=1, initial_b=0, initial_m=11, steps=100, initial_temp=100, cooling_rate=0.99):
    # Set 'best_a', 'best_b', 'best_m' with the initial values
    best_a, best_b, best_m = initial_a, initial_b, initial_m
    # Set 'current_a', 'current_b', 'current_m' with the best values
    current_a, current_b, current_m = best_a, best_b, best_m
    # Evaluate the best cost using the current parameters
    best_cost = evaluate_hash_table(keys, best_a, best_b, best_m)[0]

    # Initialize temp
    temp = initial_temp

    # For loop to randomly choose neighbor alterations for neighbor_a, neighbor_b, and neighbor_m
    for step in range(steps):
        # Generating neighbor solution
        neighbor_a = current_a + random.choice([-1, 1])
        neighbor_b = current_b + random.choice([-1, 1])
        neighbor_m = current_m + random.choice ([-1, 1])

        # Evaluating neighbor solution to find cost
        cost = evaluate_hash_table(keys, neighbor_a, neighbor_b, neighbor_m)[0]

        if (cost < best_cost):
            # Update best_a, best_b, and best_m
            best_a, best_b, best_m = neighbor_a, neighbor_b, neighbor_m
            # Update best_cost
            best_cost = cost

        # Compute acceptance probability if neighbor cost is worse
        if (cost < evaluate_hash_table(keys, current_a, current_b, current_m)[0] or 
            random.uniform(0, 1) < math.exp((evaluate_hash_table(keys, current_a, current_b, current_m)[0] - cost) / temp)):
            # Update current_a, current_b, and current_m
            current_a, current_b, current_m = neighbor_a, neighbor_b, neighbor_m

            # Temp cool down
            temp *= cooling_rate

    return best_a, best_b, best_m, best_cost

def cost_func(params, keys):
    # convert params into integers for a, b, m
    a, b, m = int(params[0]), int(params[1]), int(params[2])
    # call 'evaluate_hash_table(keys, a, b, m)'
    collisions, _ = evaluate_hash_table(keys, a, b, m)
    # return number of collisions
    return collisions

def nelder_mead_optimization(keys, initial_a=1, initial_b=0, initial_m=11):
    # Using a numeric optimizer on 'cost_func'
    # Pass initial parameters and record the best estimates for a, b, m
    result = minimize(
        cost_func,
        x0=[initial_a, initial_b, initial_m],
        args=(keys,),
        method='Nelder-mead',
        options={'maxiter': 100}
    )
    best_a, best_b, best_m = map(int, result.x)
    best_cost, _ = evaluate_hash_table(keys, best_a, best_b, best_m)
    return best_a, best_b, best_m, best_cost

def main():
    # Example keys are a list of numbers from 0 to 99
    keys = list(range(100))

    #'hc' = hill climbing
    print("Running Hill Climbing Optimization")
    hc_a, hc_b, hc_m, hc_cost = hill_climbing_optimization(keys)
    print(f"Best parameters found using Hill Climbing: a={hc_a}, b={hc_b}, m={hc_m}, collisions={hc_cost}")

    # 'sa' = simulated annealing
    print("\nRunning Simulated Annealing Optimization")
    sa_a, sa_b, sa_m, sa_cost = simulated_annealing_optimization(keys)
    print(f"Best parameter found using Simulated Annealing: a={sa_a}, b={sa_b}, m={sa_m}, collisions={sa_cost}")

    # 'nm' = nelder-mead
    print("\nRunning Nelder-Mead Optimization")
    nm_a, nm_b, nm_m, nm_cost = nelder_mead_optimization(keys)
    print(f"Best parameters found using Nelder-Mead Optimization: a={nm_a}, b={nm_b}, m={nm_m}, collisions={nm_cost}")


# If the script is run as the main program, then the main function will be called
if __name__ == "__main__":
    main()




    

    

                



