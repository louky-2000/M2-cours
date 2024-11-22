# coding: utf-8 # NE PAS SUPPRIMER CETTE LIGNE

import copy

class Multigraph:
    """
        A class representing an undirected multigraph, where each node can be an arbitrary set of integers,
        and multiple edges can exist between the same pair of nodes. This implementation allows for isolated nodes.

        Attributes:
            graph (dict): A dictionary where each key is a frozenset representing a node, and each value is another dictionary where keys are neighboring frozensets and values are integers representing the count of edges between nodes.
            m (int): The total number of edges in the multigraph.
            n (int): The total number of unique nodes in the multigraph.
    """
    
    def __init__(self):
        """
        Initializes an empty multigraph with no nodes or edges.
        """
        self.graph = {}
        self.m = 0  # Total number of edges
        self.n = 0  # Total number of unique nodes

    def add_edge(self, u, v):
        """
            Adds an undirected edge between nodes u and v. If an edge already exists, increments the count,
            allowing for multiple edges between the same nodes.

            Parameters:
                u (set): A set of integers representing the first node.
                v (set): A set of integers representing the second node.
            
            Side Effects:
                Updates the multigraph structure to add the edge and modifies the edge count `m`.
        """
        u, v = frozenset(u), frozenset(v)

        # if u not in self.graph:
        #     self.graph[u] = {}
        #     self.n += 1  # New node added
        # if v not in self.graph:
        #     self.graph[v] = {}
        #     self.n += 1  # New node added

        if v not in self.graph[u]:
            self.graph[u][v] = 0
        if u not in self.graph[v]:
            self.graph[v][u] = 0

        self.graph[u][v] += 1
        self.graph[v][u] += 1
        self.m += 1  # Increment the global edge count

    def remove_edge(self, u, v):
        """
            Removes one instance of an edge between nodes u and v. If multiple edges exist,
            only one instance is removed. Does nothing if no edge exists.

            Parameters:
                u (set): A set of integers representing the first node.
                v (set): A set of integers representing the second node.
            
            Side Effects:
                Updates the multigraph structure to remove the edge and modifies the edge count `m`.
        """
        u, v = frozenset(u), frozenset(v)

        if u in self.graph and v in self.graph[u] and self.graph[u][v] > 0:
            self.graph[u][v] -= 1
            self.graph[v][u] -= 1
            self.m -= 1  # Decrement the global edge count

            if self.graph[u][v] == 0:
                del self.graph[u][v]
            if self.graph[v][u] == 0:
                del self.graph[v][u]

    def add_node(self, u):
        """
            Adds an isolated node to the multigraph if it does not already exist.

            Parameters:
                u (set): A set of integers representing the node to add.
            
            Side Effects:
                Updates the node count `n` if the node is added.
        """
        u = frozenset(u)
        if u not in self.graph:
            self.graph[u] = {}
            self.n += 1  # Increment the node count

    def remove_node(self, u):
        """
            Removes a node and all its associated edges from the multigraph.

            Parameters:
                u (set): A set of integers representing the node to remove.
            
            Side Effects:
                Updates the multigraph structure to remove the node and modifies the node count `n`
                and edge count `m` to reflect the removed edges.
        """
        u = frozenset(u)
        if u in self.graph:
            self.m -= sum(self.graph[u].values())
            
            for v in list(self.graph[u].keys()):
                del self.graph[v][u]
            
            del self.graph[u]
            self.n -= 1  # Decrement the node count

    def neighbors(self, u):
        """
            Returns a dictionary of neighboring nodes and the edge count to each neighbor.

            Parameters:
                u (set): A set of integers representing the node for which neighbors are requested.
            
            Returns:
                dict: A dictionary where keys are neighboring frozensets and values are the edge counts to each neighbor.
                Returns an empty dictionary if the node does not exist in the graph.
        """
        u = frozenset(u)
        return self.graph.get(u, {})

    def display(self):
        """
            Displays the graph along with the total counts of nodes and edges.
            
            Side Effects:
                Prints the node and edge counts, followed by each edge with its multiplicity.
        """
        print(f"\tNumber of nodes (n): {self.n}")
        print(f"\tNumber of edges (m): {self.m}")
        for u, neighbors in self.graph.items():
            for v, count in neighbors.items():
                print(f"\t{set(u)} <--> {set(v)} ({count} edges)")

    def deep_copy(self):
        """
        Creates a deep copy of the multigraph, including all nodes, edges, and counts.

        Returns:
            Multigraph: A new instance of `Multigraph` with a deep copy of the original graph's structure.
        """
        copy_graph = Multigraph()
        copy_graph.graph = copy.deepcopy(self.graph)
        copy_graph.m = self.m
        copy_graph.n = self.n
        return copy_graph
