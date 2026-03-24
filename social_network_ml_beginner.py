import pandas as pd
import networkx as nx
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


def step_1_choose_dataset() -> str:
    dataset_path = "data/social_fake_news_sample.csv"
    print("STEP 1: Dataset chosen")
    print("Using a small social-media style fake-news dataset with 30 posts.")
    print(f"Dataset path: {dataset_path}\\n")
    return dataset_path


def step_2_load_and_explore(dataset_path: str) -> pd.DataFrame:
    print("STEP 2: Load and explore with pandas")
    df = pd.read_csv(dataset_path)

    print("First 5 rows:")
    print(df.head(), "\\n")

    print("Shape of dataset:", df.shape)
    print("Columns:", list(df.columns), "\\n")

    print("Missing values per column:")
    print(df.isna().sum(), "\\n")

    print("Fake label distribution (0=real, 1=fake):")
    print(df["fake_label"].value_counts(), "\\n")

    print("Numeric summary:")
    print(df.describe(numeric_only=True), "\\n")

    return df


def step_3_build_graph(df: pd.DataFrame) -> nx.DiGraph:
    print("STEP 3: Build a basic graph using NetworkX")
    graph = nx.DiGraph()

    for _, row in df.iterrows():
        source = row["author"]
        target = row["mentioned_user"]

        if graph.has_edge(source, target):
            graph[source][target]["weight"] += 1
        else:
            graph.add_edge(source, target, weight=1)

    print("Number of nodes:", graph.number_of_nodes())
    print("Number of edges:", graph.number_of_edges(), "\\n")
    return graph


def step_4_network_analysis(graph: nx.DiGraph, df: pd.DataFrame) -> pd.DataFrame:
    print("STEP 4: Simple network analysis (degree centrality + PageRank)")
    degree_centrality = nx.degree_centrality(graph)
    pagerank_scores = nx.pagerank(graph)

    top_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
    top_pagerank = sorted(pagerank_scores.items(), key=lambda x: x[1], reverse=True)[:5]

    print("Top 5 users by degree centrality:")
    print(pd.DataFrame(top_degree, columns=["user", "degree_centrality"]), "\\n")

    print("Top 5 users by PageRank:")
    print(pd.DataFrame(top_pagerank, columns=["user", "pagerank"]), "\\n")

    df = df.copy()
    df["author_degree_centrality"] = df["author"].map(degree_centrality)
    df["author_pagerank"] = df["author"].map(pagerank_scores)

    return df


def step_5_train_basic_model(df: pd.DataFrame) -> None:
    print("STEP 5: Train a basic ML model (Logistic Regression)")

    feature_columns = [
        "likes",
        "shares",
        "comments",
        "text_length",
        "suspicious_word_count",
        "author_degree_centrality",
        "author_pagerank",
    ]

    X = df[feature_columns]
    y = df["fake_label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.3,
        random_state=42,
        stratify=y,
    )

    model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=1000)),
        ]
    )

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    print("Accuracy:", round(accuracy_score(y_test, predictions), 3))
    print("Classification report:")
    print(classification_report(y_test, predictions))


def main() -> None:
    dataset_path = step_1_choose_dataset()
    df = step_2_load_and_explore(dataset_path)
    graph = step_3_build_graph(df)
    df_with_network_features = step_4_network_analysis(graph, df)
    step_5_train_basic_model(df_with_network_features)


if __name__ == "__main__":
    main()
