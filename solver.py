import numpy as np # Import NumPy for numerical operations, particularly for handling arrays

import os # Import os to set environment variables
os.environ["OMP_NUM_THREADS"] = "1" # Limit the number of threads used by OpenMP to 1

# Importing custom modules
import visualization
import distances
import algorithms

# Class definition for Node, representing a point in space with x, y coordinates
class Node:
    def __init__(self, node_id, x, y):
        # Initialize the node attributes
        self.id = node_id
        self.x = x
        self.y = y
        self.cluster = None # Cluster is initialized to None and can be set later

    # Method to return a string representation of the node, useful for debugging and logging
    def __repr__(self):
        return f"Node(id={self.id}, x={self.x}, y={self.y}, cluster={self.cluster})"
    
    # Static method to extract coordinates from a list of nodes and return them as a NumPy array
    @staticmethod
    def to_coordinates(nodes):
        return np.array([[node.x, node.y] for node in nodes])

# Class definition for Instance, representing a problem instance with multiple properties like nodes and tour
class Instance:
    def __init__(self, name, variation, comment, dimension, edge_weight_type, nodes, tour):
        # Initialize the instance with provided attributes
        self.name = name
        self.variation = variation
        self.comment = comment
        self.dimension = dimension
        self.edge_weight_type = edge_weight_type
        self.nodes = nodes # List of Node objects
        self.tour = tour # Precomputed tour for this instance (if any)

    # Method to display the instance details, printing only a subset of nodes for brevity
    def display(self):
        print(f"Name: {self.name}")
        print(f"Variation: {self.variation}")
        print(f"Comment: {self.comment}")
        print(f"Dimension: {self.dimension}")
        print(f"Edge Weight Type: {self.edge_weight_type}")
        print(f"Nodes: {self.nodes[:10]}...")  # Display only the first 10 nodes for brevity
        print(f"Tour: {self.tour}")

# Global variables for storing all nodes and centroid paths, likely for visualization purposes
all_nodes = []
all_centroid_path = []

# Recursive function to solve the Traveling Salesman Problem (TSP) using clustering and recursive subproblems
def recursive_solver(nodes, M, k, depth=0):
    # Base case: If the number of nodes is less than or equal to M, solve TSP directly
    if len(nodes) <= M:
        print(f"{' - ' * depth}Solving TSP directly for {len(nodes)} nodes")
        # Compute distance matrix and solve the TSP using Held-Karp algorithm
        distance_matrix = distances.compute_distance_matrix(nodes)
        tour_length, tour_indices = algorithms.held_karp(distance_matrix)
        # Construct the tour based on the node indices returned
        tour = [nodes[index] for index in tour_indices]
        return tour, [], []  # Return the tour, but no clusters or centroid paths in the base case

    # Otherwise, perform clustering and recursively solve the TSP for each cluster
    clusters, centroids, _ = algorithms.clustering(nodes, n_clusters=k) # Cluster nodes into k clusters
    # Solve TSP recursively for each cluster
    cluster_paths = [] # List to store the paths for each cluster
    for i, cluster in enumerate(clusters):
        print(f"{' - ' * depth}Recursively solving cluster {i} with {len(cluster)} nodes")
        # Recursively solve TSP for the current cluster
        cluster_path = recursive_solver(cluster, M, k, depth + 1)
        cluster_paths.append(cluster_path[0])  # Append only the tour part

    # Convert centroid coordinates into Node objects for further processing
    centroids_as_nodes = [Node(node_id=i, x=centroid[0], y=centroid[1]) for i, centroid in enumerate(centroids)]

    # Solve the TSP for the centroids recursively
    print(f"{' - ' * depth}Recursively solving TSP for centroids")
    centroid_path = recursive_solver(centroids_as_nodes, M, k, depth + 1)[0] # Get the tour for centroids

    # Store the centroid path for later visualization
    all_centroid_path.append(centroid_path)

    # Merge the cluster paths according to the order defined by the centroid TSP solution
    joined_path = cluster_paths[centroid_path[0].id]  # Start with the first centroid's corresponding cluster path
    centroid_joined_path = centroid_path[0]
    for centroid in centroid_path[1:]:  # Iterate over remaining centroids
        centroid_index = centroid.id
        path = cluster_paths[centroid_index] # Get the path for the current centroid's cluster
        centroid = centroids_as_nodes[centroid_index] # Get the corresponding centroid node

        # Join the current path with the previously joined path using a merging algorithm
        joined_path = algorithms.best_join2(joined_path, path, centroid_joined_path, centroid)
        centroid_joined_path = centroid # Update centroid_joined_path to the current centroid

    # Visualize the current paths and centroids
    # This step requires the instance to have a solution tour (i.e., the TSP has been solved for the instance)
    visualization.plot_path_nodes_and_path_centroids(all_nodes, cluster_paths, all_centroid_path, joined_path, depth, M)

    # Return the final joined path, the cluster paths, and the centroid path
    return joined_path, cluster_paths, centroid_path
