from johnson import johnson
from floyd_warshall import floyd_warshall


def read_input(filename):
    items = []
    node_cnt, edge_cnt = 0, 0
    with open(filename) as f:
        first_line = f.readline().strip().split(' ')
        node_cnt, edge_cnt = int(first_line[0]), int(first_line[1])
        for line in f:
            n1, n2, cost = line.strip().split(' ')
            items.append((int(n1), int(n2), int(cost)))

    return items

def build_graph(edges):
    graph = {}
    for n1, n2, cost in edges:
        if n1 not in graph:
            graph[n1] = {}
        graph[n1][n2] = cost
        if n2 not in graph:
            graph[n2] = {}

    return graph

def main():
    import sys
    filename = sys.argv[1]
    method = sys.argv[2]

    edges = read_input(filename)
    graph = build_graph(edges)
    print 'a graph with %s nodes, %s edges' % (len(graph), len(edges))

    if method in ('johnson', 'both'):
        paths1 = johnson(graph)
        paths = paths1
    if method in ('floyd_warshall', 'both'):
        paths2 = floyd_warshall(graph)
        paths = paths2

    if method == 'both':
        assert paths1 == paths2
    
    if paths == 'negative cycle':
        print paths
    else:
        print min(paths, key=lambda x: x[2])

if __name__ == '__main__':
    main()
