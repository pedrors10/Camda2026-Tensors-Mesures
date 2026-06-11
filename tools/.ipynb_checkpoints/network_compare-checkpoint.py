import networkx as nx


def adjacency_to_graph(adj):

    G = nx.from_pandas_adjacency(adj)

    isolated = list(nx.isolates(G))

    G.remove_nodes_from(isolated)

    return G

def compare_networks(
    results,
    class_A,
    class_B
):

    adj_A = results["adjacency"][class_A]
    adj_B = results["adjacency"][class_B]

    G_A = adjacency_to_graph(adj_A)
    G_B = adjacency_to_graph(adj_B)

    nodes_A = set(G_A.nodes())
    nodes_B = set(G_B.nodes())

    common_nodes = nodes_A & nodes_B
    only_A_nodes = nodes_A - nodes_B
    only_B_nodes = nodes_B - nodes_A

    edges_A = {
        tuple(sorted(e))
        for e in G_A.edges()
    }

    edges_B = {
        tuple(sorted(e))
        for e in G_B.edges()
    }

    common_edges = edges_A & edges_B
    only_A_edges = edges_A - edges_B
    only_B_edges = edges_B - edges_A

    return {

        "class_A": class_A,
        "class_B": class_B,

        "taxa_shared": sorted(common_nodes),
        "taxa_only_A": sorted(only_A_nodes),
        "taxa_only_B": sorted(only_B_nodes),

        "common_edges": sorted(common_edges),
        "only_A_edges": sorted(only_A_edges),
        "only_B_edges": sorted(only_B_edges),

        "summary": {

            "n_common_nodes": len(common_nodes),
            "n_only_A_nodes": len(only_A_nodes),
            "n_only_B_nodes": len(only_B_nodes),

            "n_common_edges": len(common_edges),
            "n_only_A_edges": len(only_A_edges),
            "n_only_B_edges": len(only_B_edges)

        }

    }

from itertools import combinations

from itertools import combinations

def compare_all_networks(results):

    classes = results["classes"]

    comparisons = {}

    for A, B in combinations(classes, 2):

        cmp = compare_networks(
            results,
            A,
            B
        )

        comparisons[(A, B)] = cmp
        comparisons[(B, A)] = {

            **cmp,
            "class_A": B,
            "class_B": A,

            "taxa_only_A": cmp["taxa_only_B"],
            "taxa_only_B": cmp["taxa_only_A"],

            "only_A_edges": cmp["only_B_edges"],
            "only_B_edges": cmp["only_A_edges"]
        }

    return comparisons