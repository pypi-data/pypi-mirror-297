URL for GitHub repository: https://github.com/kkruzel/graphs_kkruzel

The Dijkstra Algorithm works to find the shortest paths from a starting node to all other nodes in a weighted graph. The algorithm ensures that the shortest path to each node is found, considering the total weight of edges. It follows the following steps:
    1. It initializes an array's values to each node's distance to the starting node to infinity (except for the starting node which is 0). Infinity is represented by sys.maxsize.
    2. The algorithm repeatedly selects the node with the smallest known distance (starting with the starting node). For each neighbor of the current  node, it calculates the distance from the source by adding the distance to the current node and the edge weight to the neighbor.
    3. If  the new calculated distance to a neighbor is smaller than the previously recorded distance, update the neighbor's distance and add it to the priority queue.
    4. This process continues until all nodes have been visited and the queue is empty.
The result the algorithm provides is the shortest distance to each node from the starting node and the path to reach each node.