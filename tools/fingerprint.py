from collections import Counter
import pandas as pd
import networkx as nx


def weighted_degree(G):
    """
    Strength centrality:
    suma de pesos de las aristas incidentes.
    """
    return dict(G.degree(weight="weight"))


def unweighted_degree(G):
    """
    Degree clásico.
    """
    return dict(G.degree())


def rank_nodes(scores, nodes_subset=None):

    s = pd.Series(scores)

    if nodes_subset is not None:
        s = s.loc[list(nodes_subset)]

    return s.sort_values(ascending=False)


def build_weighted_graph(corr, adj):

    G = nx.Graph()

    nodes = adj.index
    G.add_nodes_from(nodes)

    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):

            if adj.iloc[i, j] == 1:

                w = abs(corr.iloc[i, j])

                G.add_edge(
                    nodes[i],
                    nodes[j],
                    weight=w
                )

    isolated = list(nx.isolates(G))
    G.remove_nodes_from(isolated)

    return G


def compute_master_importance(
    results,
    master
):

    master_importance = {}

    classes = results["classes"]

    for A in classes:

        print(f"Processing {A}")

        corr_A = results["correlations"][A]
        adj_A = results["adjacency"][A]

        G = build_weighted_graph(
            corr_A,
            adj_A
        )

        degree_scores = unweighted_degree(G)

        strength_scores = weighted_degree(G)

        global_degree = rank_nodes(degree_scores)

        global_strength = rank_nodes(strength_scores)

        master_importance[A] = {

            "global": {

                "degree": global_degree,
                "strength": global_strength

            },

            "histogram": {

                "degree": Counter(),
                "strength": Counter()

            },

            "vs": {}

        }

    for A in classes:

        for B in classes:

            if A == B:
                continue

            exclusive_nodes = master[(A, B)]["taxa_only_A"]
            
            degree_rank = (
                master_importance[A]["global"]["degree"]
                .reindex(exclusive_nodes)
                .dropna()
                .sort_values(ascending=False)
            )
            
            strength_rank = (
                master_importance[A]["global"]["strength"]
                .reindex(exclusive_nodes)
                .dropna()
                .sort_values(ascending=False)
            )

            master_importance[A]["vs"][B] = {

                "degree": degree_rank,

                "strength": strength_rank

            }

    return master_importance