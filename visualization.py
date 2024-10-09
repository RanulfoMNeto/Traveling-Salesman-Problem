import matplotlib.pyplot as plt

def plot_nodes_and_paths(nodes, joined_path):
    x = [node.x for node in nodes]
    y = [node.y for node in nodes]
    path_x = [node.x for node in joined_path]
    path_y = [node.y for node in joined_path]
    
    plt.figure(figsize=(10, 8))
    plt.scatter(x, y, c='blue', marker='o', label='Nodes')
    plt.plot(path_x, path_y, c='red', linestyle='-', marker='o', label='Path')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Nodes and TSP Path')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_path_nodes_and_path_centroids(nodes, cluster_paths, all_centroid_path, tour, depth, M):
    fig, axs = plt.subplots(1, 2, figsize=(18, 6))

    # 1st subplot: Scatter plot all nodes, cluster paths and centroids path
    axs[0].scatter([node.x for node in nodes], [node.y for node in nodes], color='grey', marker='o', s=50)
    for node in nodes:
        axs[0].text(node.x, node.y, f'{node.id}', fontsize=9, ha='right', color='blue')
    
    # Add the starting node to the end of each cluster path
    for idx, path in enumerate(cluster_paths):
        path = path + [path[0]]  # Add the first node to the end of the path
        axs[0].plot([node.x for node in path], [node.y for node in path], label=f'Cluster {idx} Path')
        for node in path:
            axs[0].text(node.x, node.y, f'{node.id}', fontsize=9, ha='right')
    
    for centroid_path in all_centroid_path:
        centroid_path = centroid_path + [centroid_path[0]]  # Add the first centroid to the end of the path
        axs[0].plot([centroid.x for centroid in centroid_path], [centroid.y for centroid in centroid_path], 'r--', label='Centroid Path')
        for centroid in centroid_path:
            axs[0].text(centroid.x, centroid.y, f'{centroid.id}', fontsize=10, ha='left', color='red')

    axs[0].set_title(f'Cluster Paths (Depth: {depth}, M: {M})')
    axs[0].set_xlabel('X')
    axs[0].set_ylabel('Y')
    axs[0].legend()

    # 2nd subplot: Plot all nodes and tour
    axs[1].scatter([node.x for node in nodes], [node.y for node in nodes], color='grey', marker='o', s=50)
    for node in nodes:
        axs[1].text(node.x, node.y, f'{node.id}', fontsize=9, ha='right', color='blue')
    
    # Add the starting node to the end of the tour
    tour = tour + [tour[0]]  # Add the first node to the end of the tour
    axs[1].plot([node.x for node in tour], [node.y for node in tour], 'g--', label='Tour')
    for node in tour:
        axs[1].text(node.x, node.y, f'{node.id}', fontsize=9, ha='right', color='green')

    axs[1].set_title(f'Tour (Depth: {depth}, M: {M})')
    axs[1].set_xlabel('X')
    axs[1].set_ylabel('Y')
    axs[1].legend()

    plt.tight_layout()
    plt.show()

import numpy as np

def plot_performance(M_values, k_values, costs, times):
    # Check if there is only one subplot or multiple subplots
    if len(k_values) == 1:
        fig, axs = plt.subplots(2, 1, figsize=(15, 10))
        axs = np.array(axs).reshape(2, 1)  # Ensure axs is always a 2D array
    else:
        fig, axs = plt.subplots(2, len(k_values), figsize=(15, 10))

    for i, k in enumerate(k_values):
        M = M_values[k]
        cost = costs[k]
        time = times[k]

        # Plot Costs
        axs[0, i].plot(M, cost, marker='o', linestyle='-', color='b')
        axs[0, i].set_title(f'Costs for k={k}')
        axs[0, i].set_xlabel('M')
        axs[0, i].set_ylabel('Cost')
        axs[0, i].grid(True)

        # Plot Times
        axs[1, i].plot(M, time, marker='o', linestyle='-', color='r')
        axs[1, i].set_title(f'Time for k={k}')
        axs[1, i].set_xlabel('M')
        axs[1, i].set_ylabel('Time (seconds)')
        axs[1, i].grid(True)

    plt.tight_layout()
    plt.show()