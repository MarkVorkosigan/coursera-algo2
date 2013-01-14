import collections

Edge = collections.namedtuple('Edge', ['node1', 'node2', 'cost'])
Graph = collections.namedtuple('Graph', ['edges', 'nodes'])

def read_graph(filename):
    edges = []
    nodes = set()
    with open(filename) as f:
        n_of_edges = f.readline()
        for line in f:
            n1, n2, cost = line.split(' ')
            edges.append(Edge(n1, n2, int(cost)))
            nodes.add(n1)
            nodes.add(n2)
    return Graph(edges, nodes)

def k_cluster(k, graph):
    # assign each node as a single cluster
    clusters = {} # clusters[i] contains nodes in this cluster
    nodes = {} # node[i] is the cluster that node i belongs to
    for node_id in graph.nodes:
        # name the cluster with its first node
        clusters[node_id] = [node_id]
        nodes[node_id] = node_id

    # sort the edges by length
    edges = sorted(graph.edges, key=lambda e: e.cost)

    def combine_cluster_from_to(cl1, cl2):
        """Move all nodes in cluster1 to cluster2. And kill cluster1."""
        for node_id in clusters[cl1]:
            nodes[node_id] = cl2
            clusters[cl2].append(node_id)
        clusters.pop(cl1)

    # combine clusters until get k clusters
    while len(clusters) > k:
        # take the first edge
        edge = edges.pop(0)
        
        n1 = edge.node1
        n2 = edge.node2
        cluster1 = nodes[n1]
        cluster2 = nodes[n2]

        if cluster1 <> cluster2 and cluster1 in clusters and cluster2 in clusters:
            # combine the two clusters
            # move smaller cluster to the bigger one
            if len(clusters[cluster1]) < len(clusters[cluster2]):
                combine_cluster_from_to(cluster1, cluster2)
            else:
                combine_cluster_from_to(cluster2, cluster1)
        
    # what left in 'clusters' is the k-clusters with max-min
    # spacing, find out the min spacing between the clusters
    spacings = []
    while len(spacings) < len(clusters):
        edge = edges.pop(0)
        n1, n2, cost = edge.node1, edge.node2, edge.cost
        cluster1 = nodes[n1]
        cluster2 = nodes[n2]
        if cluster1 <> cluster2:
            spacings.append((cluster1, cluster2, cost))

    return (spacings, clusters)

def main():
    graph = read_graph('clustering1.txt')
    spacings, clusters = k_cluster(4, graph)
    print spacings

if __name__ == '__main__':
    main()
