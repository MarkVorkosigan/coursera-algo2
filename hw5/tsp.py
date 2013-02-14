"""Traveling Sales man problem"""

import itertools
import gc
gc.enable()

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
        result = 0
        for i in s:
            result += 1 << i
        return result 
        #return ','.join(sorted([str(i) for i in s]))

    def get_sub_set_size(S):
        return len([s for s in bin(S) if s == '1'])

    # Init 1: cost 0 from start_node to start_node, with no other nodes
    mat[(get_set_hash({start_node}), start_node)] = 0

    # Init 2: cost inf from start_node to other nodes with no other nodes
    for other_node in other_nodes:
        mat[(get_set_hash({start_node}), other_node)] = Inf

    # Init 3: cost = start to j for sub problems with size 2
    for other_node in other_nodes:
        mat[(get_set_hash({start_node, other_node}), other_node)] = g[start_node][other_node]

    # for problem size from 3 to n
    for m in range(3, len(g.keys()) + 1):
        # for each sub-set with size m
        import datetime
        print '%s: sub problem size %s' % (datetime.datetime.now(), m)
        sub_set_cnt = 0
        mat2 = {}
        for sub_set in itertools.combinations(other_nodes, m - 1):

            set_with_start = {start_node} | set(sub_set)
            # for each node (that is not start_node) in sub_set
            for j in sub_set:
                # A[S', j] = min(A[S' - {j}, k] + Ckj for k in S' and k <> 1, j
                best_cost = Inf
                sub_set_cnt += 1
                for k in sub_set:
                    if k == j: continue
                    old_cost = mat[(get_set_hash(set_with_start - {j}), k)]
                    cost = old_cost + g[k][j]
                    if cost < best_cost:
                        mat2[(get_set_hash(set_with_start), j)] = cost
                        best_cost = cost
        mat = mat2
        print 'subset cnt: %s, mat size: %s' % (sub_set_cnt, len(mat))
    gc.collect()

    # Find the min cost of A[S, j] + cost from j to start_node
    # where S is size n
    result = Inf

    for S, j in mat:
        cost = mat[(S, j)]
        sub_set_size = get_sub_set_size(S)
        if sub_set_size != len(g): continue
        new_cost = cost + g[j][start_node]
        if new_cost < result:
            result = new_cost

    return result, 0

def tsp_dp2(g):
    """Use dynamic programming to solve TSP.
    
    Use array instead of map to save the intermidiate result.

    for m = 2, ...n:
        for S' is a sub-set of input set S with size m
        (S' contains node 1):
            for j in S':
               A[S', j] = min(A[S' - {j}, k] + Ckj for k in S' and k <> 1, j
    """
    start_node = g.keys()[0]
    other_nodes = g.keys()[1:]

    import numpy as np

    def get_set_index(s):
        result = 0
        for i in s:
            result += 1 << (i - 1)
        return result
    def get_node_index(n):
        return n - 1

    def get_sub_set_size(S):
        return len([s for s in bin(S) if s == '1'])

    def get_init_array():
        return [Inf] * n_of_nodes
            
    n_of_nodes = len(g)
    mat = {}
    # Init: cost = start to j for sub problems with size 2
    for other_node in other_nodes:
        mat[get_set_index({start_node, other_node})] = get_init_array()
        mat[get_set_index({start_node, other_node})][get_node_index(other_node)] = g[start_node][other_node]

    # for problem size from 3 to n
    for m in range(3, len(g.keys()) + 1):
        # for each sub-set with size m
        import datetime
        print '%s: sub problem size %s' % (datetime.datetime.now(), m)
        sub_set_cnt = 0
        mat2 = {}
        for sub_set in itertools.combinations(other_nodes, m - 1):

            set_with_start = {start_node} | set(sub_set)
            mat2[get_set_index(set_with_start)] = get_init_array()
            # for each node (that is not start_node) in sub_set
            for j in sub_set:
                # A[S', j] = min(A[S' - {j}, k] + Ckj for k in S' and k <> 1, j
                best_cost = Inf
                sub_set_cnt += 1
                for k in sub_set:
                    if k == j: continue
                    old_cost = mat[get_set_index(set_with_start - {j})][get_node_index(k)]
                    cost = old_cost + g[k][j]
                    if cost < best_cost:
                        mat2[get_set_index(set_with_start)][get_node_index(j)] = cost
                        best_cost = cost
        mat = mat2
    gc.collect()

    # Find the min cost of A[S, j] + cost from j to start_node
    # where S is size n
    result = Inf

    for S in mat:
        for j, cost in enumerate(mat[S]):
            node_j = j + 1
            if node_j == start_node: continue
            #sub_set_size = get_sub_set_size(S)
            #if sub_set_size != len(g): continue
            new_cost = cost + g[node_j][start_node]
            if new_cost < result:
                result = new_cost

    return result

def tsp_dp_bkup(g):
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
        sub_set_cnt = 0
        for sub_set in itertools.combinations(other_nodes, m - 1):

            set_with_start = {start_node} | set(sub_set)
            # for each node (that is not start_node) in sub_set
            for j in sub_set:
                # A[S', j] = min(A[S' - {j}, k] + Ckj for k in S' and k <> 1, j
                mat[(get_set_hash(set_with_start), j)] = (Inf, [Inf]*m)
                sub_set_cnt += 1
                for k in sub_set:
                    if k == j: continue
                    old_cost, old_route = mat[(get_set_hash(set_with_start - {j}), k)]
                    cost = old_cost + g[k][j]
                    new_cost, _ = mat[(get_set_hash(set_with_start), j)]
                    if cost < new_cost:
                        mat[(get_set_hash(set_with_start), j)] = (cost, old_route + [j])
        # clean up cached solution with size m - 1
        size_before = len(mat)
        for key in mat.keys():
            cost, route = mat[key]
            if len(route) < m:
                del mat[key]
        size_after = len(mat)
        print 'subset cnt: %s, mat size (before, after) cleaning: %s, %s' % (sub_set_cnt, size_before, size_after)

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
    d2_cost = tsp_dp2(g)
    print d2_cost
    assert d2_cost == 6.0

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
    d2_cost = tsp_dp2(g)
    assert d2_cost == 9

    for _ in range(200):
        size = random.randint(2,10)
        g = gen_problem(size)
        print 'generated problem with size %s' % size
        print g
        b_sol, b_route = tsp_bruteforce(g)
        print 'brute force sol: %s, %s' % (b_sol, b_route)
        d_sol, d_route = tsp_dp(g)
        print 'dp sol: %s, %s' % ( d_sol, d_route)
        assert b_sol == d_sol

        d2_sol = tsp_dp2(g)
        print 'dp2 sol: %s' % d2_sol
        assert d2_sol == d_sol

    g = gen_problem(16, (1,1))
    print tsp_dp(g)

if __name__ == '__main__':
    main()
