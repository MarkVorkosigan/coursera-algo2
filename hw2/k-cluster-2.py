import collections
import itertools

def read_graph(filename):
    nodes = []
    with open(filename) as f:
        n_of_nodes = f.readline()
        for line in f:
            nodes.append(tuple(line.strip().split(' ')))
    return nodes

def k_cluster(input_nodes):
    # assign eacho node as a single cluster
    clusters = {}
    nodes = {}
    for node in input_nodes:
        nodes[node] = node
        clusters[node] = [node]

    def combine_cluster_from_to(cl1, cl2):
        """Move all nodes in cluster1 to cluster2. And kill cluster1."""
        for node_id in clusters[cl1]:
            nodes[node_id] = cl2
            clusters[cl2].append(node_id)
        clusters.pop(cl1)

    def flip(bit):
        if int(bit) == 0:
            return '1'
        else:
            return '0'

    def get_2_step_neighbours(node):
        """get all neighbours that are 1 or 2 steps away from node."""
        for i in range(len(node)):
            yield node[0:i] + (flip(node[i]),) + node[i+1:]

        for i, j in itertools.permutations(range(len(node)), 2):
            if i < j:
                yield node[0:i] + (flip(node[i]),) + node[i+1:j] + (flip(node[j]),) + node[j+1:]

    # go through each node
    # for each of its neigbours within 2 steps
    # merge their clusters
    for node in nodes:
        cluster1 = nodes[node]
    
        for neighbour in get_2_step_neighbours(node):
            if neighbour not in nodes:
                continue
            cluster2 = nodes[neighbour]

            if cluster1 <> cluster2 and cluster1 in clusters and cluster2 in clusters:
                # combine the two clusters
                # move smaller cluster to the bigger one
                if len(clusters[cluster1]) < len(clusters[cluster2]):
                    combine_cluster_from_to(cluster1, cluster2)
                else:
                    combine_cluster_from_to(cluster2, cluster1)
                #print 'combine %s with %s, clusters left %s' % (''.join(cluster1), ''.join(cluster2), len(clusters))
    # what left is clusters where spacing between clusters is
    # at least 3
    return len(clusters)

def main():
    nodes = read_graph('clustering2.txt')
    clusters = k_cluster(nodes)
    print clusters

if __name__ == '__main__':
    main()
