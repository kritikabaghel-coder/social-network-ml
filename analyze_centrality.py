"""
Network Centrality Analysis - Beginner's Guide
==============================================
Learn what centrality measures mean and how to interpret them:
- Degree Centrality: "How many connections does a node have?"
- PageRank: "How important is this node based on connections?"
- Closeness Centrality: "How close is this node to all others?"
- Betweenness Centrality: "How often is this node on shortest paths?"
"""

import pandas as pd
import networkx as nx
from networkx.algorithms import community
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings

warnings.filterwarnings("ignore")


def load_and_build_graph(df_path: str, similarity_threshold: float = 0.3) -> tuple:
    """Load data and build the similarity graph."""
    df = pd.read_csv(df_path)
    
    # Create synthetic text
    def create_text(row):
        suspicious_level = "safe" if row['suspicious_word_count'] < 3 else "suspicious"
        engagement_level = ["low", "medium", "high"][min(2, row['likes'] // 50)]
        text_category = ["short", "medium", "long"][min(2, row['text_length'] // 100)]
        return f"{suspicious_level} {engagement_level} {text_category} article"
    
    df['article_text'] = df.apply(create_text, axis=1)
    
    # Build graph
    vectorizer = TfidfVectorizer(analyzer='word', lowercase=True)
    tfidf_matrix = vectorizer.fit_transform(df['article_text'])
    similarity_matrix = cosine_similarity(tfidf_matrix)
    
    graph = nx.Graph()
    for idx, row in df.iterrows():
        node_id = int(row['post_id'])
        graph.add_node(
            node_id,
            is_fake=row['fake_label'],
            likes=row['likes'],
            suspicious_words=row['suspicious_word_count']
        )
    
    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            if similarity_matrix[i, j] > similarity_threshold:
                node_i = int(df['post_id'].iloc[i])
                node_j = int(df['post_id'].iloc[j])
                graph.add_edge(node_i, node_j, weight=similarity_matrix[i, j])
    
    return graph, df


def explain_centrality_concept(measure_name: str, explanation: str) -> None:
    """Display explanation of a centrality measure."""
    print("\n" + "=" * 70)
    print(f"📘 {measure_name}")
    print("=" * 70)
    print(explanation)
    print()


def analyze_degree_centrality(graph: nx.Graph) -> pd.DataFrame:
    """Analyze degree centrality - how many connections each node has."""
    explain_centrality_concept(
        "DEGREE CENTRALITY",
        """
What it measures:
  Simply: "How many connection does this article have?"
  
How to interpret:
  - The proportion of other articles this article is connected to
  - Ranges from 0 (isolated) to 1 (connected to all others)
  - Higher = more influential/popular in the network
  
Real-world meaning:
  - A news article with high degree centrality shares similar words with many
    other articles, making it a "common topic"
  - Useful for finding trending or mainstream articles
        """
    )

    degree_centrality = nx.degree_centrality(graph)
    
    # Convert to DataFrame for better display
    results = pd.DataFrame(list(degree_centrality.items()), columns=['article_id', 'degree_centrality'])
    results['article_label'] = results['article_id'].apply(lambda x: "FAKE" if graph.nodes[x]['is_fake'] else "REAL")
    results = results.sort_values('degree_centrality', ascending=False)
    
    print("Top 10 Articles by Degree Centrality:")
    print("-" * 70)
    print(results.head(10).to_string(index=False))
    
    print("\n\nInterpretation of Top Results:")
    for idx, row in results.head(3).iterrows():
        node_id = row['article_id']
        centrality = row['degree_centrality']
        degree = graph.degree(node_id)
        label = row['article_label']
        print(f"\n  Post {node_id} ({label}):")
        print(f"    - Degree Centrality: {centrality:.3f}")
        print(f"    - Direct connections: {degree} articles")
        print(f"    - Meaning: This article shares words with {centrality*100:.1f}% of all articles")
    
    return results


def analyze_pagerank(graph: nx.Graph) -> pd.DataFrame:
    """Analyze PageRank - importance based on connection structure."""
    explain_centrality_concept(
        "PAGERANK",
        """
What it measures:
  "How important is this node based on what's connected to it?"
  
  Think of it like this: Your importance depends on WHO connects to you.
  Being connected to important nodes makes YOU more important.
  
How to interpret:
  - Unlike degree centrality, it considers QUALITY of connections
  - Nodes connected to important nodes get higher scores
  - Ranges from near 0 to some positive value (depends on graph size)
  - Higher = more influential in the network structure
  
Real-world meaning:
  - A news article about a topic that other important articles mention
    will have high PageRank
  - It's like a "recommendation score" from other articles
  - Used by Google to rank web pages!
        """
    )

    pagerank = nx.pagerank(graph)
    
    results = pd.DataFrame(list(pagerank.items()), columns=['article_id', 'pagerank'])
    results['article_label'] = results['article_id'].apply(lambda x: "FAKE" if graph.nodes[x]['is_fake'] else "REAL")
    results = results.sort_values('pagerank', ascending=False)
    
    print("Top 10 Articles by PageRank:")
    print("-" * 70)
    print(results.head(10).to_string(index=False))
    
    print("\n\nInterpretation of Top Results:")
    for idx, row in results.head(3).iterrows():
        node_id = row['article_id']
        pr_score = row['pagerank']
        neighbors = list(graph.neighbors(node_id))
        neighbor_labels = [f"{'FAKE' if graph.nodes[n]['is_fake'] else 'REAL'}" for n in neighbors]
        
        print(f"\n  Post {node_id} ({row['article_label']}):")
        print(f"    - PageRank Score: {pr_score:.6f}")
        print(f"    - Neighbors ({len(neighbors)}): {neighbors[:5]}{'...' if len(neighbors) > 5 else ''}")
        print(f"    - Neighbor types: {pd.Series(neighbor_labels).value_counts().to_dict()}")
        print(f"    - Meaning: Important because it connects to important articles")
    
    return results


def analyze_closeness_centrality(graph: nx.Graph) -> pd.DataFrame:
    """Analyze closeness centrality - how close to all other nodes."""
    explain_centrality_concept(
        "CLOSENESS CENTRALITY",
        """
What it measures:
  "How close is this node to all other nodes on average?"
  
How to interpret:
  - Measures the average shortest path distance to all other nodes
  - Ranges from 0 (far from others) to 1 (close to all)
  - Higher = more "central" in the network structure
  
Real-world meaning:
  - An article with high closeness centrality can "reach" other articles
    through fewer intermediate connections
  - Useful for finding articles that are in the middle of the network
  - Lower values mean the article is more "isolated" or in a cluster
        """
    )

    closeness_centrality = nx.closeness_centrality(graph)
    
    results = pd.DataFrame(list(closeness_centrality.items()), columns=['article_id', 'closeness_centrality'])
    results['article_label'] = results['article_id'].apply(lambda x: "FAKE" if graph.nodes[x]['is_fake'] else "REAL")
    results = results.sort_values('closeness_centrality', ascending=False)
    
    print("Top 10 Articles by Closeness Centrality:")
    print("-" * 70)
    print(results.head(10).to_string(index=False))
    
    print("\n\nInterpretation of Top Results:")
    for idx, row in results.head(3).iterrows():
        node_id = row['article_id']
        closeness = row['closeness_centrality']
        print(f"\n  Post {node_id} ({row['article_label']}):")
        print(f"    - Closeness Centrality: {closeness:.3f}")
        print(f"    - Meaning: On average, only {1/closeness:.2f} steps away from any other article")
    
    return results


def analyze_betweenness_centrality(graph: nx.Graph) -> pd.DataFrame:
    """Analyze betweenness centrality - how often on shortest paths."""
    explain_centrality_concept(
        "BETWEENNESS CENTRALITY",
        """
What it measures:
  "How often does this node appear on the shortest path between other nodes?"
  
How to interpret:
  - Counts how many shortest paths pass through this node
  - Ranges from 0 (never) to 1 (always in the middle)
  - Higher = acts as a "bridge" connecting different parts of network
  
Real-world meaning:
  - Articles with high betweenness centrality are "gatekeepers"
  - They connect different clusters or communities in the network
  - Removing them would disconnect part of the network
  - Important for information flow and network resilience
        """
    )

    betweenness_centrality = nx.betweenness_centrality(graph)
    
    results = pd.DataFrame(list(betweenness_centrality.items()), columns=['article_id', 'betweenness_centrality'])
    results['article_label'] = results['article_id'].apply(lambda x: "FAKE" if graph.nodes[x]['is_fake'] else "REAL")
    results = results.sort_values('betweenness_centrality', ascending=False)
    
    print("Top 10 Articles by Betweenness Centrality:")
    print("-" * 70)
    print(results.head(10).to_string(index=False))
    
    print("\n\nInterpretation of Top Results:")
    for idx, row in results.head(3).iterrows():
        node_id = row['article_id']
        betweenness = row['betweenness_centrality']
        print(f"\n  Post {node_id} ({row['article_label']}):")
        print(f"    - Betweenness Centrality: {betweenness:.3f}")
        if betweenness > 0:
            print(f"    - Meaning: Acts as a BRIDGE between article clusters")
        else:
            print(f"    - Meaning: Not a bridge; articles can bypass it")
    
    return results


def compare_measures(graph: nx.Graph, df: pd.DataFrame) -> None:
    """Compare different centrality measures on the same articles."""
    print("\n" + "=" * 70)
    print("📊 COMPARING ALL CENTRALITY MEASURES")
    print("=" * 70)
    
    degree = nx.degree_centrality(graph)
    pagerank = nx.pagerank(graph)
    closeness = nx.closeness_centrality(graph)
    betweenness = nx.betweenness_centrality(graph)
    
    comparison = pd.DataFrame({
        'article_id': list(graph.nodes()),
        'degree': [degree[n] for n in graph.nodes()],
        'pagerank': [pagerank[n] for n in graph.nodes()],
        'closeness': [closeness[n] for n in graph.nodes()],
        'betweenness': [betweenness[n] for n in graph.nodes()],
    })
    
    comparison['label'] = comparison['article_id'].apply(
        lambda x: "FAKE" if graph.nodes[x]['is_fake'] else "REAL"
    )
    
    # Normalize to 0-1 for comparison
    for col in ['degree', 'pagerank', 'closeness', 'betweenness']:
        max_val = comparison[col].max()
        if max_val > 0:
            comparison[col + '_norm'] = comparison[col] / max_val
    
    print("\nTop 5 Articles Across ALL Measures:")
    print("-" * 70)
    top_articles = comparison.nlargest(5, 'degree')[['article_id', 'label', 'degree', 'pagerank', 'closeness', 'betweenness']]
    print(top_articles.to_string(index=False))
    
    print("\n\nKey Observations:")
    print("-" * 70)
    
    # Check fake vs real patterns
    fake_comparison = comparison[comparison['label'] == 'FAKE']
    real_comparison = comparison[comparison['label'] == 'REAL']
    
    print(f"\nFAKE ARTICLES (n={len(fake_comparison)}):")
    print(f"  Average Degree:       {fake_comparison['degree'].mean():.3f}")
    print(f"  Average PageRank:     {fake_comparison['pagerank'].mean():.6f}")
    print(f"  Average Closeness:    {fake_comparison['closeness'].mean():.3f}")
    print(f"  Average Betweenness:  {fake_comparison['betweenness'].mean():.3f}")
    
    print(f"\nREAL ARTICLES (n={len(real_comparison)}):")
    print(f"  Average Degree:       {real_comparison['degree'].mean():.3f}")
    print(f"  Average PageRank:     {real_comparison['pagerank'].mean():.6f}")
    print(f"  Average Closeness:    {real_comparison['closeness'].mean():.3f}")
    print(f"  Average Betweenness:  {real_comparison['betweenness'].mean():.3f}")
    
    print(f"\n💡 Insight:")
    if fake_comparison['degree'].mean() > real_comparison['degree'].mean():
        print(f"   Fake articles have MORE connections on average")
    else:
        print(f"   Real articles have MORE connections on average")


def save_centrality_analysis(graph: nx.Graph, output_file: str = "data/centrality_analysis.csv") -> None:
    """Save all centrality measures to a CSV file."""
    degree = nx.degree_centrality(graph)
    pagerank = nx.pagerank(graph)
    closeness = nx.closeness_centrality(graph)
    betweenness = nx.betweenness_centrality(graph)
    
    data = []
    for node in sorted(graph.nodes()):
        data.append({
            'post_id': node,
            'is_fake': graph.nodes[node]['is_fake'],
            'degree_centrality': degree[node],
            'pagerank': pagerank[node],
            'closeness_centrality': closeness[node],
            'betweenness_centrality': betweenness[node],
            'neighbors_count': graph.degree(node),
        })
    
    df_result = pd.DataFrame(data)
    df_result.to_csv(output_file, index=False)
    print(f"\n✓ Centrality analysis saved to {output_file}")


def main() -> None:
    """Run the complete centrality analysis."""
    print("\n" + "=" * 70)
    print("NETWORK CENTRALITY ANALYSIS")
    print("Understanding the importance and influence of articles in your network")
    print("=" * 70)
    
    # Load and build graph
    graph, df = load_and_build_graph("data/social_fake_news_sample.csv")
    
    print(f"\n✓ Graph loaded: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges")
    
    # Analyze each centrality measure
    degree_results = analyze_degree_centrality(graph)
    pagerank_results = analyze_pagerank(graph)
    closeness_results = analyze_closeness_centrality(graph)
    betweenness_results = analyze_betweenness_centrality(graph)
    
    # Compare all measures
    compare_measures(graph, df)
    
    # Save results
    save_centrality_analysis(graph)
    
    print("\n" + "=" * 70)
    print("✓ Analysis Complete!")
    print("=" * 70)
    print("\n📌 Summary:")
    print("  - Degree Centrality: Count connections (popularity)")
    print("  - PageRank: Quality of connections (importance)")
    print("  - Closeness: Distance to other nodes (centrality)")
    print("  - Betweenness: Acts as bridges (connectivity)")
    print("\n")


if __name__ == "__main__":
    main()
