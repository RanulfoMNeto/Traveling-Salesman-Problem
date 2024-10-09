import time
import tsplib95 # Import TSPLIB95 to load standard TSP problem instances

# Importing custom modules
import solver
import distances
import algorithms
import visualization

# Function to measure the performance of the recursive TSP solver with different M and k values
def measure_performance(file_path, M, k):
    global all_nodes, all_centroid_path # Use global variables to store nodes and centroid paths for visualization
    costs = []
    times = []

    # Load the TSP problem from the file
    problem = tsplib95.load(file_path)
    # Convert the nodes from the problem to Node objects, using their coordinates
    nodes = [solver.Node(node_id, *coords) for node_id, coords in problem.node_coords.items()]

    try:
        # Try to get the optimal tour from the problem, if available
        tour_optimal = problem.tours[0]
    except IndexError:
        # If no optimal tour is available, set to None
        tour_optimal = None
    
    # Create an Instance object to represent the problem, with all relevant details
    instance = solver.Instance(problem.name, "", "", len(nodes), problem.edge_weight_type, nodes, tour_optimal)
    all_nodes = nodes # Assign all nodes to the global variable for visualization
    
    # Iterate over each M value in the given list
    for m in M:
        all_centroid_path = [] # Reset the global centroid path list for each M
        print(f"Testing with M={m}, k={k}")
        
        # Start the timer to measure the execution time
        start_time = time.time()

        # Solve the problem using the recursive solver with the current M and k values
        tour, cluster_paths, centroid_path = solver.recursive_solver(instance.nodes, m, k)
        tour.append(tour[0]) # Append the starting node to complete the tour
        
        # Calculate the cost of the tour before optimization
        print(f"Otimizado Cost: {distances.cost_path(tour)}")
        # Optimize the tour using the 2-opt algorithm
        tour_optimized = algorithms.two_opt(tour)
        
        # Stop the timer after the optimization
        end_time = time.time()
        
        # Store the optimized tour cost and the time taken to compute the tour
        costs.append(distances.cost_path(tour_optimized))
        times.append(end_time - start_time)

    return costs, times # Return the lists of costs and times

if __name__ == "__main__":
    # Set the file path for the TSP problem
    file_path = './tsplib/berlin52.tsp'
    # Define a range of k values to test
    k_values = list(range(2, 3))
    costs = {}
    times = {}
    M_values = {}

    # Iterate over each k value
    for k in k_values:

        # Generate values of M starting from k and going up to 20
        M = list(range(10, 13))

        # Measure the performance (cost and time) for the current k and M values
        cost, duration = measure_performance(file_path, M, k)
        costs[k] = cost
        times[k] = duration
        M_values[k] = M

        # Print the results for the current k value
        print(f"Results for k={k}:")
        for m, c, t in zip(M, cost, duration):
            # Print the cost and time for each M value
            print(f"  M={m}, Cost={c:.4f}, Time={t:.4f}")
        print()

    # Print aggregated results for all k values
    print("Aggregated Results:")
    for k in k_values:
        print(f"\nFor k={k}:")
        M = M_values[k]
        cost = costs[k]
        time = times[k]
        for m, c, t in zip(M, cost, time):
            # Print the cost and time for each M value in an aggregated view
            print(f"  M={m}, Cost={c:.4f}, Time={t:.4f}")

    # Call the visualization function to plot the performance results
    visualization.plot_performance(M_values, k_values, costs, times)
