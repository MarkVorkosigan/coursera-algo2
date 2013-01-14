
def bellman_ford(graph, s, t):
    """Given a directed graph, find the shortest path
    between s and t.
    """

    mat = {}
    # init, path from a node to itself is 0
    for n in graph:
        if n == s:
            mat[n] = 0
        else:
            mat[n] = 1000000

    changed = True
    round = 1
    while changed and round <= len(graph):
        changed = False
        round += 1
        for es in graph:
            for et in graph[es]:
                edge_cost = graph[es][et]
                if mat[et] > mat[es] + edge_cost:
                    changed = True
                    mat[et] = mat[es] + edge_cost
                  
    for n in graph:
        print n, mat[n]
    if not changed:
        return mat[t]
    else:
        return 'negative cycle'


def main():

    g = {1: {2: 1, 3: 4}, 2: {3: 1}, 3:{}}
    assert bellman_ford(g, 1, 3) == 2

    g = {1: {2: -1}, 2: {1: -1}}
    assert bellman_ford(g, 1, 2) == 'negative cycle'

if __name__ == '__main__':
    main()
