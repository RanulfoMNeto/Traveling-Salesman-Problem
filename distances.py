import utils
import math
import numpy as np

def euclidean(start, end, round=utils.nint):
    """Return the Euclidean distance between start and end.

    This is capable of performing distance calculations for EUC_2D and
    EUC_3D problems. If ``round_func=math.ceil`` is passed, this is suitable for
    CEIL_2D problems as well.

    :param tuple start: *n*-dimensional coordinate
    :param tuple end: *n*-dimensional coordinate
    :param callable round_func: function to use to round the result
    :return: rounded distance
    :rtype: float
    """
    
    # Extract coordinates from Node objects
    start_coords = (start.x, start.y, getattr(start, 'z', None))
    end_coords = (end.x, end.y, getattr(end, 'z', None))
    
    # Filter out None values if 'z' is not present
    start_coords = tuple(coord for coord in start_coords if coord is not None)
    end_coords = tuple(coord for coord in end_coords if coord is not None)
    
    # if len(start) != len(end):
    #     raise ValueError('Dimension mismatch between start and end')

    # Calculate squared distances
    square_distance = sum(d * d for d in utils.deltas(start_coords, end_coords))
    distance = math.sqrt(square_distance)

    return round(distance)

def compute_distance_matrix(nodes):
    num_nodes = len(nodes)
    distance_matrix = np.zeros((num_nodes, num_nodes))
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j:
                distance_matrix[i][j] = euclidean(nodes[i], nodes[j])
    return distance_matrix

def cost_path(path):
    aux = path + [path[0]]
    total_cost = 0.0
    n = len(aux)
    for i in range(n):
        next_node = aux[(i + 1) % n]
        total_cost += euclidean(aux[i], next_node)
    return total_cost