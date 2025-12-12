import json
import csv
import os
from pathlib import Path
from collections import Counter

# ✅ Optional: for pretty terminal tables
try:
    from tabulate import tabulate
except ImportError:
    tabulate = None


def extract_ratings_from_json(json_file_path):
    """Extract ratings from a JSON file."""
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        clarity = data.get('Clarity', {}).get('rating', 'N/A')
        completeness = data.get('Completeness', {}).get('rating', 'N/A')
        consistency = data.get('Consistency', {}).get('rating', 'N/A')
        
        return {
            'filename': os.path.basename(json_file_path),
            'clarity': clarity,
            'completeness': completeness,
            'consistency': consistency
        }
    except Exception as e:
        print(f"Error processing {json_file_path}: {e}")
        return None


def print_terminal_analysis(results):
    """Print rating statistics directly in the terminal."""
    print("\n📊 Summary of Extracted Ratings:\n")
    headers = ["Filename", "Clarity", "Completeness", "Consistency"]
    rows = [[r['filename'], r['clarity'], r['completeness'], r['consistency']] for r in results]
    
    if tabulate:
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    else:
        # Simple fallback
        print(f"{'Filename':30s} | {'Clarity':25s} | {'Completeness':25s} | {'Consistency':25s}")
        print("-" * 115)
        for r in results:
            print(f"{r['filename']:30s} | {r['clarity']:25s} | {r['completeness']:25s} | {r['consistency']:25s}")
    
    # --- Summary Statistics ---
    clarity_ratings = [r['clarity'] for r in results if r['clarity'] != 'N/A']
    completeness_ratings = [r['completeness'] for r in results if r['completeness'] != 'N/A']
    consistency_ratings = [r['consistency'] for r in results if r['consistency'] != 'N/A']

    rating_order = [
        'Exceeds Expectations',
        'Meets Expectations',
        'Partially Meets Expectations',
        'Does Not Meet Expectations'
    ]

    clarity_counts = Counter(clarity_ratings)
    completeness_counts = Counter(completeness_ratings)
    consistency_counts = Counter(consistency_ratings)

    print("\n📈 Rating Distribution Summary:\n")
    summary_table = []
    for rating in rating_order:
        summary_table.append([
            rating,
            clarity_counts.get(rating, 0),
            completeness_counts.get(rating, 0),
            consistency_counts.get(rating, 0)
        ])

    if tabulate:
        print(tabulate(summary_table, headers=["Rating", "Clarity", "Completeness", "Consistency"], tablefmt="fancy_grid"))
    else:
        print(f"{'Rating':35s} | {'Clarity':10s} | {'Completeness':15s} | {'Consistency':15s}")
        print("-" * 85)
        for row in summary_table:
            print(f"{row[0]:35s} | {row[1]:10d} | {row[2]:15d} | {row[3]:15d}")

    # --- Percentage Summary ---
    print("\n📊 Percentage Breakdown by Metric:\n")
    metrics = {
        'Clarity': clarity_counts,
        'Completeness': completeness_counts,
        'Consistency': consistency_counts
    }

    percentage_table = []
    for metric, counts in metrics.items():
        total = sum(counts.values())
        if total == 0:
            continue
        percentage_table.append([
            metric,
            f"{counts.get('Exceeds Expectations', 0)} ({counts.get('Exceeds Expectations', 0) / total * 100:.1f}%)",
            f"{counts.get('Meets Expectations', 0)} ({counts.get('Meets Expectations', 0) / total * 100:.1f}%)",
            f"{counts.get('Partially Meets Expectations', 0)} ({counts.get('Partially Meets Expectations', 0) / total * 100:.1f}%)",
            f"{counts.get('Does Not Meet Expectations', 0)} ({counts.get('Does Not Meet Expectations', 0) / total * 100:.1f}%)"
        ])

    if tabulate:
        print(tabulate(percentage_table,
                       headers=["Metric", "Exceeds", "Meets", "Partially Meets", "Does Not Meet"],
                       tablefmt="fancy_grid"))
    else:
        print(f"{'Metric':15s} | {'Exceeds':15s} | {'Meets':15s} | {'Partial':20s} | {'Does Not Meet':15s}")
        print("-" * 90)
        for row in percentage_table:
            print(f"{row[0]:15s} | {row[1]:15s} | {row[2]:15s} | {row[3]:20s} | {row[4]:15s}")

    print("\n✅ Terminal analysis complete.\n")


def process_folder(folder_path, output_csv='ratings_output.csv', terminal_only=True):
    """Process all JSON files in a folder and show terminal summary."""
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f"Error: Folder '{folder_path}' does not exist.")
        return
    
    json_files = list(folder.glob('*.json'))
    if not json_files:
        print(f"No JSON files found in '{folder_path}'")
        return
    
    results = []
    for json_file in json_files:
        result = extract_ratings_from_json(json_file)
        if result:
            results.append(result)
    
    if results:
        # Print table summary in terminal
        print_terminal_analysis(results)

        # Also write to CSV for record-keeping
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['filename', 'clarity', 'completeness', 'consistency']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        
        print(f"📁 CSV saved to: {output_csv}\n")
    else:
        print("No valid data extracted from JSON files.")


if __name__ == "__main__":
    # Example usage
    folder_path = "LLM_as_a_Judge_openai_outputs_3cs"
    output_csv = "output_ratings.csv"
    process_folder(folder_path, output_csv, terminal_only=True)
