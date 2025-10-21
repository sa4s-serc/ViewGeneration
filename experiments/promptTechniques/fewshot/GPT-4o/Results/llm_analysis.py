import json
import csv
import os
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

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

def plot_analysis(results, output_folder='plots'):
    """Create various plots for the analysis."""
    # Create output folder for plots
    os.makedirs(output_folder, exist_ok=True)
    
    # Set style
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (12, 8)
    
    # Extract data
    clarity_ratings = [r['clarity'] for r in results if r['clarity'] != 'N/A']
    completeness_ratings = [r['completeness'] for r in results if r['completeness'] != 'N/A']
    consistency_ratings = [r['consistency'] for r in results if r['consistency'] != 'N/A']
    
    # Define rating order for consistent plotting
    rating_order = [
        'Exceeds Expectations',
        'Meets Expectations',
        'Partially Meets Expectations',
        'Does Not Meet Expectations'
    ]
    
    # 1. Bar chart comparing all three metrics
    fig, ax = plt.subplots(figsize=(14, 8))
    
    clarity_counts = Counter(clarity_ratings)
    completeness_counts = Counter(completeness_ratings)
    consistency_counts = Counter(consistency_ratings)
    
    x = range(len(rating_order))
    width = 0.25
    
    clarity_values = [clarity_counts.get(rating, 0) for rating in rating_order]
    completeness_values = [completeness_counts.get(rating, 0) for rating in rating_order]
    consistency_values = [consistency_counts.get(rating, 0) for rating in rating_order]
    
    ax.bar([i - width for i in x], clarity_values, width, label='Clarity', color='#3498db')
    ax.bar(x, completeness_values, width, label='Completeness', color='#2ecc71')
    ax.bar([i + width for i in x], consistency_values, width, label='Consistency', color='#e74c3c')
    
    ax.set_xlabel('Rating', fontsize=12, fontweight='bold')
    ax.set_ylabel('Count', fontsize=12, fontweight='bold')
    ax.set_title('Distribution of Ratings Across All Metrics', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(rating_order, rotation=45, ha='right')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_folder}/ratings_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Individual pie charts for each metric
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    metrics = [
        ('Clarity', clarity_counts, '#3498db'),
        ('Completeness', completeness_counts, '#2ecc71'),
        ('Consistency', consistency_counts, '#e74c3c')
    ]
    
    for idx, (metric_name, counts, base_color) in enumerate(metrics):
        if counts:
            labels = list(counts.keys())
            sizes = list(counts.values())
            colors = plt.cm.Set3(range(len(labels)))
            
            axes[idx].pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
            axes[idx].set_title(f'{metric_name} Distribution', fontsize=12, fontweight='bold')
        else:
            axes[idx].text(0.5, 0.5, 'No Data', ha='center', va='center')
            axes[idx].set_title(f'{metric_name} Distribution', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{output_folder}/pie_charts.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Stacked bar chart showing percentage distribution
    fig, ax = plt.subplots(figsize=(12, 8))
    
    metrics_names = ['Clarity', 'Completeness', 'Consistency']
    data_for_stacked = []
    
    for rating in rating_order:
        data_for_stacked.append([
            clarity_counts.get(rating, 0),
            completeness_counts.get(rating, 0),
            consistency_counts.get(rating, 0)
        ])
    
    # Convert to percentages
    totals = [sum(clarity_values), sum(completeness_values), sum(consistency_values)]
    data_percentages = []
    for rating_data in data_for_stacked:
        percentages = [rating_data[i] / totals[i] * 100 if totals[i] > 0 else 0 
                      for i in range(3)]
        data_percentages.append(percentages)
    
    colors = ['#27ae60', '#f39c12', '#e67e22', '#c0392b']
    bottom = [0, 0, 0]
    
    for idx, rating in enumerate(rating_order):
        ax.bar(metrics_names, data_percentages[idx], bottom=bottom, 
               label=rating, color=colors[idx])
        bottom = [bottom[i] + data_percentages[idx][i] for i in range(3)]
    
    ax.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
    ax.set_title('Percentage Distribution of Ratings by Metric', fontsize=14, fontweight='bold')
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    ax.set_ylim(0, 100)
    
    plt.tight_layout()
    plt.savefig(f'{output_folder}/stacked_percentage.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 4. Heatmap showing rating distribution
    fig, ax = plt.subplots(figsize=(10, 6))
    
    heatmap_data = []
    for rating in rating_order:
        heatmap_data.append([
            clarity_counts.get(rating, 0),
            completeness_counts.get(rating, 0),
            consistency_counts.get(rating, 0)
        ])
    
    sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='YlOrRd', 
                xticklabels=metrics_names, yticklabels=rating_order,
                cbar_kws={'label': 'Count'}, ax=ax)
    
    ax.set_title('Heatmap of Rating Counts', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{output_folder}/heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 5. Summary statistics table plot
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.axis('tight')
    ax.axis('off')
    
    summary_data = []
    for metric_name, counts in [('Clarity', clarity_counts), 
                                 ('Completeness', completeness_counts), 
                                 ('Consistency', consistency_counts)]:
        total = sum(counts.values())
        exceeds = counts.get('Exceeds Expectations', 0)
        meets = counts.get('Meets Expectations', 0)
        partial = counts.get('Partially Meets Expectations', 0)
        does_not = counts.get('Does Not Meet Expectations', 0)
        
        summary_data.append([
            metric_name,
            total,
            f"{exceeds} ({exceeds/total*100:.1f}%)" if total > 0 else "0 (0.0%)",
            f"{meets} ({meets/total*100:.1f}%)" if total > 0 else "0 (0.0%)",
            f"{partial} ({partial/total*100:.1f}%)" if total > 0 else "0 (0.0%)",
            f"{does_not} ({does_not/total*100:.1f}%)" if total > 0 else "0 (0.0%)"
        ])
    
    table = ax.table(cellText=summary_data,
                     colLabels=['Metric', 'Total', 'Exceeds', 'Meets', 'Partially Meets', 'Does Not Meet'],
                     cellLoc='center',
                     loc='center',
                     colWidths=[0.15, 0.1, 0.15, 0.15, 0.2, 0.2])
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    
    # Color header
    for i in range(6):
        table[(0, i)].set_facecolor('#3498db')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    plt.title('Summary Statistics', fontsize=14, fontweight='bold', pad=20)
    plt.savefig(f'{output_folder}/summary_table.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"\nPlots saved to '{output_folder}/' folder:")
    print("  - ratings_comparison.png (Bar chart comparison)")
    print("  - pie_charts.png (Individual pie charts)")
    print("  - stacked_percentage.png (Stacked percentage bar chart)")
    print("  - heatmap.png (Heatmap of ratings)")
    print("  - summary_table.png (Summary statistics table)")

def process_folder(folder_path, output_csv='ratings_output.csv', create_plots=True):
    """Process all JSON files in a folder and create a CSV."""
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f"Error: Folder '{folder_path}' does not exist.")
        return
    
    # Find all JSON files
    json_files = list(folder.glob('*.json'))
    
    if not json_files:
        print(f"No JSON files found in '{folder_path}'")
        return
    
    # Extract ratings from all JSON files
    results = []
    for json_file in json_files:
        result = extract_ratings_from_json(json_file)
        if result:
            results.append(result)
    
    # Write to CSV
    if results:
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['filename', 'clarity', 'completeness', 'consistency']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(results)
        
        print(f"Successfully processed {len(results)} files.")
        print(f"CSV saved to: {output_csv}")
        
        # Create plots
        if create_plots:
            print("\nGenerating analysis plots...")
            plot_analysis(results)
    else:
        print("No valid data extracted from JSON files.")

if __name__ == "__main__":
    # Example usage
    folder_path = "LLM_as_a_Judge_openai_outputs_3cs"
    output_csv = "output_ratings.csv"
    
    if not output_csv:
        output_csv = 'ratings_output.csv'
    
    process_folder(folder_path, output_csv, create_plots=True)