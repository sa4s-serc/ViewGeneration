import os
import json
import csv

# 📁 Set your static folder path here
FOLDER_PATH = "LLM_as_a_Judge_openai_outputs"   # <-- change this to your folder name

def evaluate_from_comparison(file_path: str):
    """Extract evaluation metrics from the 'comparison' field of a JSON file."""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    comparison = data.get("comparison", {})

    # Components
    hallucinated_components = comparison.get("unique_to_GeneratedImage", [])
    missing_components = comparison.get("unique_to_GroundTruth", [])
    common_components = comparison.get("common_components", [])

    # Connectors
    hallucinated_connectors = comparison.get("unique_connectors_GeneratedImage", [])
    missing_connectors = comparison.get("unique_connectors_GroundTruth", [])
    common_connectors = comparison.get("common_connectors", [])

    return {
        "file": os.path.basename(file_path),
        # Components
        "hallucinated_components_count": len(hallucinated_components),
        "missing_components_count": len(missing_components),
        "correct_components_count": len(common_components),
        "hallucinated_components": hallucinated_components,
        "missing_components": missing_components,
        "correct_components": common_components,
        # Connectors
        "hallucinated_connectors_count": len(hallucinated_connectors),
        "missing_connectors_count": len(missing_connectors),
        "correct_connectors_count": len(common_connectors),
        "hallucinated_connectors": hallucinated_connectors,
        "missing_connectors": missing_connectors,
        "correct_connectors": common_connectors,
    }
def stringify_components(comp_list):
    result = []
    for c in comp_list:
        if isinstance(c, dict):
            result.append(c.get("name", json.dumps(c)))  # Use 'name' if exists
        else:
            result.append(str(c))
    return "; ".join(result)
def stringify_connectors(conn_list):
    result = []
    for c in conn_list:
        if isinstance(c, dict):
            src = c.get("source", "?")
            tgt = c.get("target", "?")
            lbl = c.get("label", "")
            result.append(f"{src}->{tgt} ({lbl})")
        else:
            result.append(str(c))
    return "; ".join(result)
def main():
    results = []

    for filename in os.listdir(FOLDER_PATH):
        if filename.endswith(".json"):
            file_path = os.path.join(FOLDER_PATH, filename)
            print(f"Processing: {filename}")
            result = evaluate_from_comparison(file_path)
            results.append(result)

    # 📊 Print summary
    print("\n📊 Evaluation Results:")
    print(f"{'File':30s} {'Halluc(C)':>10s} {'Missing(C)':>10s} {'Correct(C)':>10s} {'Halluc(Conn)':>14s} {'Missing(Conn)':>14s} {'Correct(Conn)':>14s}")
    print("-" * 110)
    for r in results:
        print(
            f"{r['file']:30s} "
            f"{r['hallucinated_components_count']:>10d} "
            f"{r['missing_components_count']:>10d} "
            f"{r['correct_components_count']:>10d} "
            f"{r['hallucinated_connectors_count']:>14d} "
            f"{r['missing_connectors_count']:>14d} "
            f"{r['correct_connectors_count']:>14d}"
        )

    # 💾 Save results to CSV
    csv_path = os.path.join("few_shot_claude_error_analysis.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "file",
            "hallucinated_components_count",
            "missing_components_count",
            "correct_components_count",
            "hallucinated_connectors_count",
            "missing_connectors_count",
            "correct_connectors_count",
            "hallucinated_components",
            "missing_components",
            "correct_components",
            "hallucinated_connectors",
            "missing_connectors",
            "correct_connectors",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for r in results:
            # Convert lists to strings for CSV storage
            r["hallucinated_components"] = stringify_components(r["hallucinated_components"])
            r["missing_components"] = stringify_components(r["missing_components"])
            r["correct_components"] = stringify_components(r["correct_components"])
            r["hallucinated_connectors"] = stringify_connectors(r["hallucinated_connectors"])
            r["missing_connectors"] = stringify_connectors(r["missing_connectors"])
            r["correct_connectors"] = stringify_connectors(r["correct_connectors"])
            writer.writerow(r)

    print(f"\n✅ CSV report saved to: {csv_path}")

if __name__ == "__main__":
    main()
