def held_karp(distance_matrix):
    n = len(distance_matrix)

    if n == 1:
        min_cost = 0
        path = [0]  # Adjusted to return a list with the single point
        return min_cost, path

    dp = [[float('inf')] * n for _ in range(1 << n)]
    parent = [[-1] * n for _ in range(1 << n)]
    dp[1][0] = 0

    for mask in range(1 << n):
        for i in range(n):
            if mask & (1 << i):
                for j in range(n):
                    if i != j and mask & (1 << j):
                        if dp[mask ^ (1 << i)][j] + distance_matrix[j][i] < dp[mask][i]:
                            dp[mask][i] = dp[mask ^ (1 << i)][j] + distance_matrix[j][i]
                            parent[mask][i] = j

    min_cost = float('inf')
    last = -1
    for i in range(1, n):
        if dp[(1 << n) - 1][i] + distance_matrix[i][0] < min_cost:
            min_cost = dp[(1 << n) - 1][i] + distance_matrix[i][0]
            last = i

    path = []
    mask = (1 << n) - 1
    while last != -1:
        path.append(last)
        next_last = parent[mask][last]
        mask ^= (1 << last)
        last = next_last

    path = path[::-1]

    return min_cost, path

import numpy as np
from sklearn.cluster import KMeans

def clustering(nodes, n_clusters):
    coordinates = np.array([[node.x, node.y] for node in nodes])
    kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init=10, init='k-means++').fit(coordinates)
    labels = kmeans.labels_
    centroids = kmeans.cluster_centers_
    inertia = kmeans.inertia_

    for node, label in zip(nodes, labels):
        node.cluster = label

    clusters = [[] for _ in range(n_clusters)]
    for node in nodes:
        clusters[node.cluster].append(node)

    return clusters, centroids, inertia

import distances

def two_opt(path):

    improved = True
    while improved:
        improved = False
        for i in range(1, len(path) - 1):
            for j in range(i + 1, len(path)):
                if j - i == 1: 
                    continue
                new_path = path[:i] + path[i:j][::-1] + path[j:]
                if distances.cost_path(new_path) < distances.cost_path(path):
                    path = new_path
                    improved = True
    return path

def best_join2(path_a, path_b, centroid_a, centroid_b):
    # Encontrar o ponto mais próximo de cada caminho para os centróides
    closest_point_a = min(path_a, key=lambda node: distances.euclidean(node, centroid_b))
    closest_point_b = min(path_b, key=lambda node: distances.euclidean(node, centroid_a))
    
    index_a = path_a.index(closest_point_a)
    index_b = path_b.index(closest_point_b)

    # 1. Junção A + B
    path1 = path_a[:index_a+1] + path_b[index_b:] + path_b[:index_b] + path_a[index_a+1:]

    # 2. Junção B + A
    path2 = path_b[:index_b+1] + path_a[index_a:] + path_a[:index_a] + path_b[index_b+1:]

    # 3. Junção A + B, mas começando pelo ponto B mais próximo
    path3 = path_b[index_b:] + path_a[index_a:] + path_a[:index_a] + path_b[:index_b]

    # 4. Junção B + A, mas começando pelo ponto A mais próximo
    path4 = path_a[index_a:] + path_b[index_b:] + path_b[:index_b] + path_a[:index_a]

    # Otimização dos caminhos
    two_opt_path1 = two_opt(path1)
    two_opt_path2 = two_opt(path2)
    two_opt_path3 = two_opt(path3)
    two_opt_path4 = two_opt(path4)
    
    # Calcula o custo de cada caminho
    cost1 = distances.cost_path(two_opt_path1)
    cost2 = distances.cost_path(two_opt_path2)
    cost3 = distances.cost_path(two_opt_path3)
    cost4 = distances.cost_path(two_opt_path4)
    
    # Seleciona o caminho com menor custo
    costs = [cost1, cost2, cost3, cost4]
    best_path_index = np.argmin(costs)
    best_path = [two_opt_path1, two_opt_path2, two_opt_path3, two_opt_path4][best_path_index]
    
    return best_path