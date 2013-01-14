
Inf = 1000000
def floyd_warshall(graph):
    """Given a graph, find shortest distance between all pairs."""
    nodes = dict(enumerate(graph.keys(), start=1))

    mat = {}

    for n1 in nodes:
        node1 = nodes[n1]
        for n2 in nodes:
            node2 = nodes[n2]
            if n1 == n2:
                mat[(n1, n2, 0)] = 0
            elif node2 in graph[node1]:
                mat[(n1, n2, 0)] = graph[node1][node2]
            else:
                mat[(n1, n2, 0)] = Inf

    for k in range(1, len(nodes) + 1):
        for n1 in nodes:
            for n2 in nodes:

                if mat[(n1, k, k-1)] != Inf and mat[(k, n2, k-1)] != Inf:
                    mat[(n1, n2, k)] = min(
                        mat[(n1, n2, k-1)],
                        mat[(n1, k, k-1)] + mat[(k, n2, k-1)])
                else:
                    mat[(n1, n2, k)] = mat[(n1, n2, k-1)]
    print mat
    result = []
    for n1 in nodes:
        node1 = nodes[n1]
        for n2 in nodes:
            node2 = nodes[n2]
            shortest_path = mat[(n1, n2, len(nodes))]
            if n1 == n2:
                if shortest_path < 0:
                    return 'negative cycle'
            if n1 != n2 and shortest_path != Inf:
                result.append((node1, node2, shortest_path))

    return result
    
def main():

    g = {1: {2: 1, 3: 4}, 2: {3: 1}, 3:{}}

    #assert floyd_warshall(g) == [(1, 2, 1), (1, 3, 2), (2, 3, 1)]

    g = {1: {2: -1}, 2: {1: -1}}
    #assert floyd_warshall(g) == 'negative cycle'

    g = {'1': {'4': 4, '3': 6},
         '4': {'1': 4, '2': 8},
         '2': {'4': 8, '5': 1},
         '5': {'1': -2},
         '3': {'2': -5, '1': 6},
         }
    #paths = floyd_warshall(g)
    #paths.sort()
    
    #assert paths == [
    #    ('1', '2', 1), ('1', '3', 6), ('1', '4', 4), ('1', '5', 2),
    #    ('2', '1', -1), ('2', '3', 5), ('2', '4', 3), ('2', '5', 1),
    #    ('3', '1', -6), ('3', '2', -5), ('3', '4', -2), ('3', '5', -4),
    #    ('4', '1', 4), ('4', '2', 5), ('4', '3', 10), ('4', '5', 6),
    #    ('5', '1', -2), ('5', '2', -1), ('5', '3', 4), ('5', '4', 2),
    #    ]
    
    g = {1: {2: -1, 3: -1}, 2: {2: -1, 3: -1, 1: -1}, 3: {1: -1, 2: -1}}
    print floyd_warshall(g)
if __name__ == '__main__':
    main()

