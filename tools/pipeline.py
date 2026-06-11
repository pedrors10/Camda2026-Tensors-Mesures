import numpy as np
import pandas as pd
import networkx as nx

from .metrics import chi2_distance


def network_distance_pipeline(
    data,
    metadata,
    disease_column="disease",
    sample_column="sample_id",
    metric="pearson",
    threshold=0.7,
    abs_corr=True,
    min_samples=2,
    distance="chi2"
):

    counts = metadata[disease_column].value_counts()

    valid_classes = counts[
        counts >= min_samples
    ].index.tolist()

    classes = sorted(valid_classes)

    submatrices = {}

    feature_column = data.columns[0]

    for cls in classes:

        samples = metadata.loc[
            metadata[disease_column] == cls,
            sample_column
        ].tolist()

        cols = [
            feature_column,
            *[s for s in samples if s in data.columns]
        ]

        submatrices[cls] = data[cols]

    correlations = {}
    adjacency = {}

    for cls, df in submatrices.items():

        X = df.iloc[:, 1:]

        corr = X.T.corr(method=metric)

        if abs_corr:

            adj = (
                np.abs(corr) >= threshold
            ).astype(int)

        else:

            adj = (
                corr >= threshold
            ).astype(int)

        np.fill_diagonal(adj.values, 0)

        correlations[cls] = corr
        adjacency[cls] = adj

    degree_distributions = {}

    max_degree = 0

    for cls, adj in adjacency.items():

        G = nx.from_pandas_adjacency(adj)

        deg = np.array(
            [d for _, d in G.degree()]
        )

        degree_distributions[cls] = deg

        max_degree = max(
            max_degree,
            deg.max()
        )

    histograms = {}

    for cls, deg in degree_distributions.items():

        hist = np.bincount(
            deg,
            minlength=max_degree + 1
        )

        hist = hist / hist.sum()

        histograms[cls] = hist

    D = pd.DataFrame(
        index=classes,
        columns=classes,
        dtype=float
    )

    for c1 in classes:
        for c2 in classes:

            if distance == "chi2":

                D.loc[c1, c2] = chi2_distance(
                    histograms[c1],
                    histograms[c2]
                )

            else:

                raise ValueError(
                    f"Unknown distance '{distance}'"
                )

    return {
        "classes": classes,
        "submatrices": submatrices,
        "correlations": correlations,
        "adjacency": adjacency,
        "degree_distributions": degree_distributions,
        "histograms": histograms,
        "distance_matrix": D
    }
