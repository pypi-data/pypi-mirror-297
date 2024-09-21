import matplotlib.pyplot as plt


def create_chart(data: dict):
    categories = list(data.keys())
    values = list(data.values())

    plt.figure(figsize=(10, 6))
    bars = plt.bar(categories, values)

    plt.title("RAG Metrics Calculations", fontsize=16)
    plt.xlabel("Metrics", fontsize=12)
    plt.ylabel("Scores", fontsize=12)
    plt.ylim(0, 1.1)

    plt.xticks(rotation=45, ha="right")

    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"{height:.4f}",
            ha="center",
            va="bottom",
        )

    plt.tight_layout()
    plt.show()
