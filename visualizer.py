import matplotlib.pyplot as plt

def visualize_synthetic_vs_structural(synthetic_similarity, structural_similarity, output_path="synthetic_vs_structural.png"):
    """Visualizes a bar chart comparing Synthetic and Structural Similarity."""
    
    categories = ["Synthetic Similarity", "Structural Similarity"]
    values = [synthetic_similarity, structural_similarity]

    # Create a bar chart
    plt.figure(figsize=(5, 5))
    plt.bar(categories, values, color=["#3498db", "#e74c3c"])  # Blue & Red colors
    plt.ylim(0, 1)  # Similarity values range from 0 to 1
    plt.ylabel("Similarity Score")
    plt.title("Comparison: Synthetic vs Structural Similarity")

    # Save the visualization
    plt.savefig(output_path, format="png", dpi=300)
    print(f"✅ Visualization saved as '{output_path}'")

    plt.close()
def visualize_similarity(results, final_score, output_path="similarity_report.png"):
    """Visualizes similarity results as a bar chart and saves it."""
    
    # Categories and corresponding values
    categories = [
        "AST Match",
        "CFG Match",
        "Token Match",
        "Text Similarity Score",
        "Hash Match",
        "Synthetic Similarity",
        "Structural Similarity",
        "Final Score",
    ]
    
    # Extracting similarity scores
    values = [
        int(results["AST Match"]),
        int(results["CFG Match"]),
        int(results["Token Match"]),
        results["Text Similarity Score"],
        int(results["Hash Match"]),
        results["Synthetic Similarity"],
        results["Structural Similarity"],
        final_score,
    ]

    # Check lengths to prevent mismatch error
    if len(categories) != len(values):
        raise ValueError(
            f"Shape mismatch: categories ({len(categories)}) and values ({len(values)})"
        )

    # Create a bar chart
    plt.figure(figsize=(12, 7))
    plt.bar(categories, values, color=["#4caf50", "#f44336", "#2196f3", "#ffeb3b", "#9c27b0", "#ff9800", "#00bcd4", "#8bc34a"])
    plt.xlabel("Techniques")
    plt.ylabel("Scores")
    plt.title("Code Similarity Analysis Report")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    # Save the visualization
    try:
        plt.savefig(output_path, format="png", dpi=300)
        print(f"✅ Visualization saved as '{output_path}'")
    except Exception as e:
        print(f"❌ Error while saving visualization: {e}")

    plt.close()


def visualize_synthetic_similarity(synthetic_score, output_path="synthetic_similarity.png"):
    """Visualizes synthetic similarity as a bar chart."""
    plt.figure(figsize=(6, 4))
    plt.bar(["Synthetic Similarity"], [synthetic_score], color="#2196f3")
    plt.ylabel("Score")
    plt.title("Synthetic Similarity Analysis")
    plt.ylim(0, 1)

    # Save as PNG
    plt.savefig(output_path, format="png", dpi=300)
    print(f"✅ Synthetic similarity visualization saved as '{output_path}'")
    plt.close()


def visualize_structural_similarity(structural_score, output_path="structural_similarity.png"):
    """Visualizes structural similarity as a bar chart."""
    plt.figure(figsize=(6, 4))
    plt.bar(["Structural Similarity"], [structural_score], color="#4caf50")
    plt.ylabel("Score")
    plt.title("Structural Similarity Analysis")
    plt.ylim(0, 1)

    # Save as PNG
    plt.savefig(output_path, format="png", dpi=300)
    print(f"✅ Structural similarity visualization saved as '{output_path}'")
    plt.close()
    

def visualize_behavioral_similarity(behavioral_similarity, output_path="behavioral_similarity.png"):
    """Visualizes the behavioral similarity score."""
    categories = ["Behavioral Similarity"]
    values = [behavioral_similarity]

    plt.figure(figsize=(6, 5))
    plt.bar(categories, values, color=["#8e44ad"])
    plt.ylim(0, 1)
    plt.ylabel("Similarity Score")
    plt.title("Behavioral Similarity Analysis")

    plt.savefig(output_path, format="png", dpi=300)
    print(f"✅ Behavioral similarity visualization saved as '{output_path}'")

    plt.close()


def visualize_synthetic_vs_structural_vs_behavioral(synthetic_similarity, structural_similarity, behavioral_similarity, output_path="synthetic_structural_behavioral.png"):
    """Visualizes comparison of Synthetic, Structural, and Behavioral Similarities."""
    categories = ["Synthetic", "Structural", "Behavioral"]
    values = [synthetic_similarity, structural_similarity, behavioral_similarity]

    plt.figure(figsize=(8, 5))
    plt.bar(categories, values, color=["#3498db", "#e74c3c", "#8e44ad"])
    plt.ylim(0, 1)
    plt.ylabel("Similarity Score")
    plt.title("Comparison: Synthetic, Structural & Behavioral Similarity")

    plt.savefig(output_path, format="png", dpi=300)
    print(f"✅ Synthetic, Structural & Behavioral visualization saved as '{output_path}'")

    plt.close()
