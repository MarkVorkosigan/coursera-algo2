from dijstra import dijstra

def johnson(graph):
    """Given a graph, find shortest distance between all pairs."""

    # 1. Run bellman-ford to get node shift value
    # assume a artifical node, with edge cost 0 to all other nodes
    mat = {}
    for n in graph:
        mat[n] = 0

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

    if changed:
        return 'negative cycle'

    # 2. Build a graph with edge cost shifted as:
    # new_cost = old_cost + mat[start] - mat[end]
    new_graph = {}
    for es in graph:
        new_graph[es] = {}
        for et in graph[es]:
            new_graph[es][et] = graph[es][et] + mat[es] - mat[et]
            assert new_graph[es][et] >= 0

    # 3. Run dijstra n times
    result = []
    for es in graph:
        costs = dijstra(new_graph, es)
        for et, dist in costs:
            result.append((es, et, dist - mat[es] + mat[et]))

    return result

def main():

    g = {1: {2: 1, 3: 4}, 2: {3: 1}, 3:{}}

    assert johnson(g) == [
        (1, 2, 1),
        (1, 3, 2),
        (2, 3, 1)]

    g = {1: {2: -1}, 2: {1: -1}}
    assert johnson(g) == 'negative cycle'

    g = {1: {2: 1, 3: 4}, 2: {4: 1}, 3: {4:-4}, 4:{}}
    assert johnson(g) == [
        (1, 2, 1),
        (1, 3, 4),
        (1, 4, 0),
        (2, 4, 1),
        (3, 4, -4)]

if __name__ == '__main__':
    main()
            
