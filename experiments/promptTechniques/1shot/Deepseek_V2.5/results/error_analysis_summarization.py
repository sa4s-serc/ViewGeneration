import pandas as pd

# 📁 Path to your CSV file
CSV_PATH = "one_shot_deepseek_error_analysis.csv"  

def main():
    # Read the CSV
    df = pd.read_csv(CSV_PATH)

    # Select only the numeric columns you want to analyze
    numeric_cols = [
        "hallucinated_components_count",
        "missing_components_count",
        "correct_components_count",
        "hallucinated_connectors_count",
        "missing_connectors_count",
        "correct_connectors_count"
    ]

    # Ensure numeric columns are correctly parsed (just in case)
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

    # Drop rows with NaN (if any) just for clean stats
    df_clean = df[numeric_cols].dropna()

    # Compute descriptive statistics
    stats = pd.DataFrame({
        "mean": df_clean.mean(),
        "median": df_clean.median(),
        "variance": df_clean.var(),
        "std_dev": df_clean.std(),
        "min": df_clean.min(),
        "max": df_clean.max(),
        "sum": df_clean.sum(),
        "count": df_clean.count()
    })

    # Round for readability
    stats = stats.round(3)

    # Print results to console
    print("\n📊 Statistics for Evaluation Metrics:\n")
    print(stats)

    # Save results to a new CSV file
    output_path = "one_shot_deepseek_evaluation_stats_summary.csv"
    stats.to_csv(output_path)
    print(f"\n✅ Statistics saved to: {output_path}")

if __name__ == "__main__":
    main()
