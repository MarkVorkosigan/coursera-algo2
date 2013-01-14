import heapq

class Node:
    def __init__(self, node, visited, cur_cost):
        self.node = node
        self.visited = visited
        self.cur_cost = cur_cost


Inf = 100000000
def dijstra(graph, start_node):
    """return shortest distance from start_node to all other nodes in graph."""

    node_dict = {}
    for n in graph:
        if n == start_node:
            cost = 0
        else:
            cost = Inf
        node_dict[n] = Node(node=n, visited=False, cur_cost=cost)

    unvisited_nodes = []
    for n in node_dict:
        node = node_dict[n]
        unvisited_nodes.append((node.cur_cost, n))

    unvisited_nodes.sort()

    while unvisited_nodes:
        cur_cost, cur_node = heapq.heappop(unvisited_nodes)
        # the node has been updated since cur_node was pushed
        if cur_cost != node_dict[cur_node].cur_cost: continue
        if node_dict[cur_node].visited: continue

        for et in graph[cur_node]:
            if node_dict[et].visited: continue
            
            edge_cost = graph[cur_node][et]
            new_cost = cur_cost + edge_cost
            if new_cost < node_dict[et].cur_cost:
                node_dict[et].cur_cost = new_cost
                heapq.heappush(unvisited_nodes, (new_cost, et))
        node_dict[cur_node].visited = True

    result = []
    for n in node_dict:
        if n != start_node and node_dict[n].cur_cost < Inf:
            result.append((n, node_dict[n].cur_cost))
    return result


def main():

    g = {1:{2:1, 3:2}, 2:{}, 3:{}}
    assert dijstra(g, 1) == [(2, 1),
                             (3, 2)]

    g = {1: {2: 1, 4: 2}, 2: {3: 1},
         3: {}, 4: {3: 1}}

    assert dijstra(g, 1) == [(2, 1), (3, 2), (4, 2)]


if __name__ == '__main__':
    main()
