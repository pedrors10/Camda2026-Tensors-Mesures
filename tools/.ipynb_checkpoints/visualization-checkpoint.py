import matplotlib.pyplot as plt
import seaborn as sns


def plot_distance_matrix(
    D,
    title="Distance Matrix",
    cmap="plasma",
    figsize=(12,10),
    annot=False,
    fmt=".2f",
    save_path=None
):

    plt.figure(figsize=figsize)

    sns.heatmap(
        D,
        cmap=cmap,
        annot=annot,
        fmt=fmt
    )

    plt.title(title)

    plt.tight_layout()

    if save_path is not None:

        plt.savefig(
            save_path,
            dpi=300,
            bbox_inches="tight"
        )

    plt.show()
