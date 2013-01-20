"""Traveling Sales man problem"""

import itertools

Inf = 10000000
def tsp_bruteforce(g):
    """Using brute force to sovle the problem."""
    best_result = Inf
    best_route = []
    start_node = g.keys()[0]
    other_nodes = g.keys()[1:]

    for route in itertools.permutations(other_nodes):
        length = 0
        cur_node = start_node
        cur_route = []
        for next_node in route:
            length += g[cur_node][next_node]
            cur_node = next_node
            cur_route.append(cur_node)

        # last leg back to start point
        length += g[cur_node][start_node]
        if length < best_result:
            best_result = length
            best_route = [start_node] + cur_route + [start_node]
    return best_result, best_route

def tsp_dp(g):
    """Use dynamic programming to solve TSP.

    for m = 2, ...n:
        for S' is a sub-set of input set S with size m
        (S' contains node 1):
            for j in S':
               A[S', j] = min(A[S' - {j}, k] + Ckj for k in S' and k <> 1, j
    """
    start_node = g.keys()[0]
    other_nodes = g.keys()[1:]

    mat = {}
    def get_set_hash(s):
        return ','.join(sorted([str(i) for i in s]))

    # Init 1: cost 0 from start_node to start_node, with no other nodes
    mat[(get_set_hash({start_node}), start_node)] = (0, [start_node])

    # Init 2: cost inf from start_node to other nodes with no other nodes
    for other_node in other_nodes:
        mat[(get_set_hash({start_node}), other_node)] = (Inf, [start_node])

    # Init 3: cost = start to j for sub problems with size 2
    for other_node in other_nodes:
        mat[(get_set_hash({start_node, other_node}), other_node)] = (g[start_node][other_node], [start_node, other_node])

    # for problem size from 3 to n
    for m in range(3, len(g.keys()) + 1):
        # for each sub-set with size m
        import datetime
        print '%s: sub problem size %s' % (datetime.datetime.now(), m)
        for sub_set in itertools.combinations(other_nodes, m - 1):
            set_with_start = {start_node} | set(sub_set)
            # for each node (that is not start_node) in sub_set
            for j in sub_set:
                # A[S', j] = min(A[S' - {j}, k] + Ckj for k in S' and k <> 1, j
                mat[(get_set_hash(set_with_start), j)] = (Inf, [Inf]*m)
                for k in sub_set:
                    if k == j: continue
                    old_cost, old_route = mat[(get_set_hash(set_with_start - {j}), k)]
                    cost = old_cost + g[k][j]
                    new_cost, _ = mat[(get_set_hash(set_with_start), j)]
                    if cost < new_cost:
                        mat[(get_set_hash(set_with_start), j)] = (cost, old_route + [j])
        # clean up cached solution with size m - 2
        for key in mat.keys():
            cost, route = mat[key]
            if len(route) < m - 2:
                del mat[key]

    # Find the min cost of A[S, j] + cost from j to start_node
    # where S is size n
    result = Inf
    result_route = []
    for S, j in mat:
        cost, route = mat[(S, j)]
        if len(route) != len(g): continue
        new_cost = cost + g[j][start_node]
        new_route = route + [start_node]
        if new_cost < result:
            result = new_cost
            result_route = new_route
    return result, result_route


def fill_graph(g):
    """make a direct graph to undirect by add edges for the other direction."""
    for s in g:
        for t in g[s]:
            if s not in g[t]:
                g[t][s] = g[s][t]

import random
def gen_problem(size, edge_cost=(1, 20)):
    g = {}
    cost_lb, cost_up = edge_cost
    for i in range(1, size + 1):
        g[i] = {}
        for j in range(i + 1, size + 1):
            g[i][j] = random.randint(cost_lb, cost_up)
    fill_graph(g)
    return g

def main():
    g = {1: {2: 1}, 2: {3: 2}, 3: {1: 3}}
    fill_graph(g)
    b_cost, b_route = tsp_bruteforce(g)
    d_cost, d_route = tsp_dp(g)
    print g
    print 'brute force sol: %s, %s' % (b_cost, b_route)
    print 'dp sol: %s, %s' % (d_cost, d_route)
    assert b_cost == 6
    assert d_cost == 6

    g = {1: {2: 1, 3: 2, 4: 4},
         2: {3: 2, 4: 3},
         3: {4: 3},
         4: {}}
    fill_graph(g)
    b_cost, b_route = tsp_bruteforce(g)
    d_cost, d_route = tsp_dp(g)
    print g
    print 'brute force sol: %s, %s' % (b_cost, b_route)
    print 'dp sol: %s, %s' % (d_cost, d_route)
    assert b_cost == 9
    assert d_cost == 9

    for _ in range(200):
        size = random.randint(2,11)
        g = gen_problem(size)
        print 'generated problem with size %s' % size
        print g
        b_sol, b_route = tsp_bruteforce(g)
        print 'brute force sol: %s, %s' % (b_sol, b_route)
        d_sol, d_route = tsp_dp(g)
        print 'dp sol: %s, %s' % ( d_sol, d_route)
        assert b_sol == d_sol

    g = gen_problem(25, (1,1))
    print tsp_dp(g)

if __name__ == '__main__':
    main()
