"""
Social Network Graph Building using NetworkX
=============================================
Creates a graph where:
- Each news article is a node
- Edges connect articles that share similar words
- Includes analysis and basic visualization
"""

import pandas as pd
import networkx as nx
from networkx.algorithms import community
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings

warnings.filterwarnings("ignore")


def load_data(path: str) -> pd.DataFrame:
    """Load the dataset."""
    df = pd.read_csv(path)
    print(f"✓ Loaded {len(df)} articles\n")
    return df


def create_synthetic_text(row: pd.DataFrame) -> str:
    """
    Create synthetic text from article features.
    (In a real scenario, you'd have actual article text)
    
    For this dataset, we create text based on engagement metrics
    to simulate article content similarity.
    """
    suspicious_level = ["safe", "warning"] if row['suspicious_word_count'] < 3 else ["suspicious"]
    engagement_level = ["low", "medium", "high"][min(2, row['likes'] // 50)]
    text_category = ["short", "medium", "long"][min(2, row['text_length'] // 100)]

    # Create synthetic text representing article type
    text = f"{suspicious_level[0]} {engagement_level} {text_category} article"
    return text


def build_similarity_graph(df: pd.DataFrame, similarity_threshold: float = 0.3) -> tuple:
    """
    Build a social network graph based on article similarity.
    
    Parameters:
    - df: The dataframe with articles
    - similarity_threshold: Minimum similarity to create an edge (0 to 1)
    
    Returns:
    - graph: NetworkX graph object
    - similarity_matrix: Cosine similarity between all articles
    """
    print("=" * 60)
    print("STEP 1: Generate Article Similarity")
    print("=" * 60)

    # Create text representation for each article
    df = df.copy()
    df['article_text'] = df.apply(create_synthetic_text, axis=1)

    print("Sample article representations:")
    for i in range(min(3, len(df))):
        print(f"  Article {df['post_id'].iloc[i]}: {df['article_text'].iloc[i]}")

    # Calculate TF-IDF vectors
    vectorizer = TfidfVectorizer(analyzer='word', lowercase=True)
    tfidf_matrix = vectorizer.fit_transform(df['article_text'])

    # Calculate cosine similarity between all articles
    similarity_matrix = cosine_similarity(tfidf_matrix)

    print(f"\n✓ Calculated similarity matrix ({similarity_matrix.shape})")
    print(f"✓ Similarity range: {similarity_matrix.min():.3f} to {similarity_matrix.max():.3f}\n")

    # Build NetworkX graph
    print("=" * 60)
    print("STEP 2: Build NetworkX Graph")
    print("=" * 60)

    graph = nx.Graph()

    # Add nodes (one per article)
    for idx, row in df.iterrows():
        node_id = int(row['post_id'])
        is_fake = row['fake_label']
        
        graph.add_node(
            node_id,
            label=f"Post {node_id}",
            is_fake=is_fake,
            likes=row['likes'],
            suspicious_words=row['suspicious_word_count']
        )

    # Add edges based on similarity threshold
    edge_count = 0
    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            similarity_score = similarity_matrix[i, j]

            if similarity_score > similarity_threshold:
                node_i = int(df['post_id'].iloc[i])
                node_j = int(df['post_id'].iloc[j])

                graph.add_edge(
                    node_i,
                    node_j,
                    weight=similarity_score
                )
                edge_count += 1

    print(f"Similarity threshold: {similarity_threshold}")
    print(f"✓ Created graph with {graph.number_of_nodes()} nodes")
    print(f"✓ Created graph with {edge_count} edges")
    print(f"✓ Graph density: {nx.density(graph):.3f}\n")

    return graph, similarity_matrix, df


def analyze_graph(graph: nx.Graph) -> None:
    """Analyze and display network statistics."""
    print("=" * 60)
    print("STEP 3: Network Analysis")
    print("=" * 60)

    # Basic statistics
    print(f"\n📊 BASIC STATISTICS:")
    print(f"  Nodes: {graph.number_of_nodes()}")
    print(f"  Edges: {graph.number_of_edges()}")
    print(f"  Average degree: {sum(dict(graph.degree()).values()) / graph.number_of_nodes():.2f}")

    # Connected components
    n_components = nx.number_connected_components(graph)
    print(f"  Connected components: {n_components}")

    if n_components > 1:
        print("\n  [Note: Graph has disconnected clusters of articles]")

    # Centrality measures
    print(f"\n🎯 DEGREE CENTRALITY (Most connected articles):")
    degree_centrality = nx.degree_centrality(graph)
    top_central = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]

    for node, centrality in top_central:
        degree = graph.degree(node)
        is_fake = "FAKE" if graph.nodes[node]['is_fake'] else "REAL"
        print(f"  Post {node} ({is_fake}): {centrality:.3f} centrality, {degree} connections")

    # Betweenness centrality
    print(f"\n🌉 BETWEENNESS CENTRALITY (Bridge articles):")
    betweenness = nx.betweenness_centrality(graph)
    top_between = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:5]

    for node, bet_score in top_between:
        is_fake = "FAKE" if graph.nodes[node]['is_fake'] else "REAL"
        print(f"  Post {node} ({is_fake}): {bet_score:.3f} betweenness")

    # Fake vs Real distribution
    print(f"\n⚠️  FAKE vs REAL IN NETWORK:")
    fake_nodes = [n for n, attr in graph.nodes(data=True) if attr.get('is_fake') == 1]
    real_nodes = [n for n, attr in graph.nodes(data=True) if attr.get('is_fake') == 0]

    print(f"  Real articles: {len(real_nodes)}")
    print(f"  Fake articles: {len(fake_nodes)}")

    if fake_nodes:
        avg_fake_degree = np.mean([graph.degree(n) for n in fake_nodes])
        avg_real_degree = np.mean([graph.degree(n) for n in real_nodes]) if real_nodes else 0
        print(f"  Avg connections per fake article: {avg_fake_degree:.2f}")
        print(f"  Avg connections per real article: {avg_real_degree:.2f}")

    print()


def community_detection(graph: nx.Graph) -> dict:
    """Detect communities using greedy modularity optimization."""
    print("=" * 60)
    print("STEP 4: Community Detection")
    print("=" * 60)

    if graph.number_of_edges() == 0:
        print("\n⚠️  No edges in graph. Cannot detect communities.\n")
        return {}

    detected_communities = community.greedy_modularity_communities(graph)

    print(f"\n✓ Detected {len(detected_communities)} community/communities:")
    community_dict = {}

    for i, comm in enumerate(detected_communities):
        print(f"\n  Community {i + 1} ({len(comm)} articles):")
        community_nodes = sorted(list(comm))
        community_dict[i] = community_nodes
        print(f"    Nodes: {community_nodes[:10]}", end="")
        if len(community_nodes) > 10:
            print(f" ... and {len(community_nodes) - 10} more")
        else:
            print()

        # Count fake vs real in this community
        fake_count = sum(1 for n in comm if graph.nodes[n]['is_fake'] == 1)
        print(f"    Fake articles: {fake_count}/{len(comm)}")

    print()
    return community_dict


def save_graph_info(graph: nx.Graph, output_file: str = "data/graph_info.txt") -> None:
    """Save graph information to a text file."""
    with open(output_file, 'w') as f:
        f.write("SOCIAL NETWORK GRAPH INFORMATION\n")
        f.write("=" * 60 + "\n\n")

        f.write(f"Nodes: {graph.number_of_nodes()}\n")
        f.write(f"Edges: {graph.number_of_edges()}\n")
        f.write(f"Density: {nx.density(graph):.3f}\n")
        f.write(f"Connected Components: {nx.number_connected_components(graph)}\n\n")

        f.write("NODE INFORMATION:\n")
        f.write("-" * 60 + "\n")
        for node in sorted(graph.nodes()):
            data = graph.nodes[node]
            is_fake = "FAKE" if data['is_fake'] else "REAL"
            degree = graph.degree(node)
            f.write(f"Post {node} ({is_fake}): {degree} connections\n")

    print(f"✓ Graph info saved to {output_file}\n")


def main() -> None:
    """Main execution pipeline."""
    print("\n" + "=" * 60)
    print("SOCIAL NETWORK GRAPH BUILDER")
    print("=" * 60 + "\n")

    # Load data
    df = load_data("data/social_fake_news_sample.csv")

    # Build graph
    graph, similarity_matrix, df_with_text = build_similarity_graph(
        df,
        similarity_threshold=0.3
    )

    # Analyze graph
    analyze_graph(graph)

    # Detect communities
    communities = community_detection(graph)

    # Save results
    save_graph_info(graph)

    print("=" * 60)
    print("✓ Graph building complete!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
