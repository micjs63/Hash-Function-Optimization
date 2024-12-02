# Overview
Implement a hash function and optimize the function's performance to reduce the need for rehashing when inserting elements. Hill Climbing, Simulated Annealing, and Nelder-Mead are the optimization techniques that will be used to find an optimal set of parameters for the hash function to reduce collisions and improve efficiency.

# Comparing the Optimization Techniques
* With the parameters (a=1, b=0, m=11) for hill climbing, simulated annealing, and nelder-mead no collisions are recorded at all from any of the optimization techniques and the output is the same for all (a=1, b=0, m=11)
* As long as a=1 and m=11, it does not matter what b is. No collisions are recorded and the initial parameters are outputted.
* Once a is assigned a large number (i.e. a=5000) that is when all optimization techniques begin to produce different outputs for a, b, and m.

* # Nelder-mead differs
* However, by increasing each initial parameter by 1 (i.e. a=2, b=1, m=12) for all optimization techniques causes nelder-mead to have 53 collisions  and output (a=3, b=2, m=13)
	* Hill climbing and simulated annealing do not record any collisions and produce the same output as each other. (a=2, b=1, m=12)



# Author
Michael Jaldin-Soto
email: jaldinsotom@g.cofc.edu

