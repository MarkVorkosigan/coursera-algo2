from collections import namedtuple
from collections import defaultdict

def read_graph(filename):
    vs = defaultdict(dict)
    with open(filename) as f:
        f.readline()
        for line in f:
            snode, enode, cost = [int(a.strip()) for a in line.split(' ')]
            vs[snode][enode] = cost
            vs[enode][snode] = cost
    return vs

def min_span_tree(vs):
    init_node = vs.keys()[0]
    s1 = set([init_node])
    s2 = set(vs.keys()[1:])
    mst = []
    mst_cost = 0
    edges_to_s1 = [(init_node, v, cost) for v, cost in vs[init_node].items()]
    edges_to_s1.sort(key=lambda x: x[2])

    while s2:
        v1, v2, cost = get_best_next_edge(s1, s2, edges_to_s1)
        mst_cost += cost
        mst.append((v1, v2, cost))
        edges_to_s1 = adjust_edges_to_s1(vs, v1, v2, s1, s2, edges_to_s1)
        s1.add(v2)
        s2.remove(v2)

    return mst_cost, mst

def get_best_next_edge(s1, s2, edges_to_s1):
    return edges_to_s1[0]

def adjust_edges_to_s1(vs, v1, v2, s1, s2, edges_to_s1):
    """v1 was in s1, v2 was in s2 and moved to s1"""
    new_edges_to_s1 = []
    for edge in edges_to_s1:
        (s, t, cost) = edge
        if v2 not in (s, t):
            new_edges_to_s1.append(edge)

    for s in vs[v2]:
        if s in s2 and s != v2:
            new_edges_to_s1.append((v2, s, vs[v2][s]))

    return sorted(new_edges_to_s1, key=lambda x: x[2])


def main():
    vs = read_graph('edges.txt')
    mst_cost, mst = min_span_tree(vs)

    print mst_cost


if __name__ == '__main__':
    main()
            
    
