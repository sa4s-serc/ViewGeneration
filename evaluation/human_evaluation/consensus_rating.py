"""
Consensus Rating Calculator
============================
This script calculates consensus ratings between two authors
and provides statistics by experimental setting.
"""

import json
import pandas as pd
from collections import Counter
import os

def load_json_data(filepath):
    """Load JSON data from file."""
    with open(filepath, 'r') as f:
        return json.load(f)

def normalize_rating(rating):
    """Normalize rating text to standard format."""
    if not rating or pd.isna(rating):
        return None
    
    rating = str(rating).strip()
    
    # Map variations to standard format
    if rating in ['Meets Expectations', 'Meets', 'meets']:
        return 'Meets'
    elif rating in ['Partially Meets Expectations', 'Partial', 'partial', 'Partially Meets']:
        return 'Partial'
    elif rating in ['Does Not Meet Expectations', 'Not Meet', 'not meet', 'Does Not Meet', "Doesn't Meet"]:
        return 'Not Meet'
    else:
        return None

def calculate_consensus_rating(rating1, rating2, strategy='conservative'):
    """
    Calculate consensus rating between two authors.
    
    Args:
        rating1: Author 1's rating
        rating2: Author 2's rating
        strategy: 'conservative' (take lower), 'liberal' (take higher), or 'average'
    
    Returns:
        Consensus rating
    """
    # Normalize ratings
    r1 = normalize_rating(rating1)
    r2 = normalize_rating(rating2)
    
    # If either is None, return the other
    if r1 is None and r2 is None:
        return None
    if r1 is None:
        return r2
    if r2 is None:
        return r1
    
    # If same, return that rating
    if r1 == r2:
        return r1
    
    # Define ordering: Meets > Partial > Not Meet
    order = {'Meets': 3, 'Partial': 2, 'Not Meet': 1}
    
    if strategy == 'conservative':
        # Take the lower (more critical) rating
        return r1 if order[r1] < order[r2] else r2
    
    elif strategy == 'liberal':
        # Take the higher (more lenient) rating
        return r1 if order[r1] > order[r2] else r2
    
    elif strategy == 'average':
        # Average the two (round to nearest)
        avg = (order[r1] + order[r2]) / 2
        
        if avg >= 2.5:
            return 'Meets'
        elif avg >= 1.5:
            return 'Partial'
        else:
            return 'Not Meet'
    
    return None

def create_consensus_ratings(author1_file, author2_file, strategy='conservative'):
    """
    Create consensus ratings from two authors.
    
    Returns:
        DataFrame with consensus ratings
    """
    print(f"\nCreating consensus ratings using '{strategy}' strategy...")
    
    # Load data
    author1_data = load_json_data(author1_file)
    author2_data = load_json_data(author2_file)
    
    consensus_rows = []
    
    for sample_id in author1_data.keys():
        if sample_id not in author2_data:
            print(f"Warning: Sample {sample_id} not in author2 data")
            continue
        
        for setting_id in author1_data[sample_id].keys():
            if setting_id not in author2_data[sample_id]:
                print(f"Warning: Setting {setting_id} for sample {sample_id} not in author2 data")
                continue
            
            a1_eval = author1_data[sample_id][setting_id]
            a2_eval = author2_data[sample_id][setting_id]
            
            # Get ratings
            acc_a1 = a1_eval.get('accuracyRating')
            acc_a2 = a2_eval.get('accuracyRating')
            det_a1 = a1_eval.get('detailRating')
            det_a2 = a2_eval.get('detailRating')
            
            # Calculate consensus
            consensus_accuracy = calculate_consensus_rating(acc_a1, acc_a2, strategy)
            consensus_detail = calculate_consensus_rating(det_a1, det_a2, strategy)
            
            row = {
                'sample_id': sample_id,
                'setting_id': setting_id,
                'author1_accuracy': normalize_rating(acc_a1),
                'author2_accuracy': normalize_rating(acc_a2),
                'consensus_accuracy': consensus_accuracy,
                'accuracy_agreement': normalize_rating(acc_a1) == normalize_rating(acc_a2),
                'author1_detail': normalize_rating(det_a1),
                'author2_detail': normalize_rating(det_a2),
                'consensus_detail': consensus_detail,
                'detail_agreement': normalize_rating(det_a1) == normalize_rating(det_a2)
            }
            
            consensus_rows.append(row)
    
    return pd.DataFrame(consensus_rows)

def calculate_statistics_by_setting(consensus_df):
    """
    Calculate rating statistics grouped by experimental setting.
    
    Returns:
        DataFrame with statistics per setting
    """
    print("\nCalculating statistics by setting...")
    
    stats_rows = []
    
    # Group by setting
    for setting_id in sorted(consensus_df['setting_id'].unique()):
        setting_data = consensus_df[consensus_df['setting_id'] == setting_id]
        
        # Accuracy statistics
        acc_counter = Counter(setting_data['consensus_accuracy'].dropna())
        acc_total = len(setting_data['consensus_accuracy'].dropna())
        
        stats_rows.append({
            'setting_id': setting_id,
            'metric': 'Accuracy',
            'meets': acc_counter.get('Meets', 0),
            'partial': acc_counter.get('Partial', 0),
            'not_meet': acc_counter.get('Not Meet', 0),
            'total': acc_total,
            'meets_pct': acc_counter.get('Meets', 0) / acc_total * 100 if acc_total > 0 else 0,
            'partial_pct': acc_counter.get('Partial', 0) / acc_total * 100 if acc_total > 0 else 0,
            'not_meet_pct': acc_counter.get('Not Meet', 0) / acc_total * 100 if acc_total > 0 else 0
        })
        
        # Detail statistics
        det_counter = Counter(setting_data['consensus_detail'].dropna())
        det_total = len(setting_data['consensus_detail'].dropna())
        
        stats_rows.append({
            'setting_id': setting_id,
            'metric': 'Level of Detail',
            'meets': det_counter.get('Meets', 0),
            'partial': det_counter.get('Partial', 0),
            'not_meet': det_counter.get('Not Meet', 0),
            'total': det_total,
            'meets_pct': det_counter.get('Meets', 0) / det_total * 100 if det_total > 0 else 0,
            'partial_pct': det_counter.get('Partial', 0) / det_total * 100 if det_total > 0 else 0,
            'not_meet_pct': det_counter.get('Not Meet', 0) / det_total * 100 if det_total > 0 else 0
        })
    
    return pd.DataFrame(stats_rows)

def generate_latex_table(stats_df, output_file=None):
    """
    Generate LaTeX table from statistics.
    
    Returns:
        LaTeX table string
    """
    # Pivot the data for better table structure
    # We want: Setting | Metric | Meets | Partial | Not Meet | Total
    
    latex = """
\\begin{table}[ht]
\\centering
\\caption{Consensus ratings by experimental setting (human evaluation)}
\\label{tab:consensus_by_setting}
\\begin{tabular}{llcccc}
\\toprule
\\textbf{Setting} & \\textbf{Metric} & \\textbf{Meets} & \\textbf{Partial} & \\textbf{Not Meet} & \\textbf{Total} \\\\
\\midrule
"""
    
    current_setting = None
    for _, row in stats_df.iterrows():
        setting = row['setting_id']
        metric = row['metric']
        
        # Add horizontal line between settings
        if current_setting is not None and current_setting != setting:
            latex += "\\cmidrule{1-6}\n"
        
        current_setting = setting
        
        # Format the row
        latex += f"{setting} & {metric} & "
        latex += f"{row['meets']} ({row['meets_pct']:.1f}\\%) & "
        latex += f"{row['partial']} ({row['partial_pct']:.1f}\\%) & "
        latex += f"{row['not_meet']} ({row['not_meet_pct']:.1f}\\%) & "
        latex += f"{row['total']} \\\\\n"
    
    latex += """\\bottomrule
\\end{tabular}
\\end{table}
"""
    
    if output_file:
        with open(output_file, 'w') as f:
            f.write(latex)
        print(f"\nLaTeX table saved to {output_file}")
    
    return latex

def calculate_overall_statistics(consensus_df):
    """
    Calculate overall statistics across all settings.
    
    Returns:
        DataFrame with overall statistics
    """
    print("\nCalculating overall statistics...")
    
    overall_stats = []
    
    # Accuracy
    acc_counter = Counter(consensus_df['consensus_accuracy'].dropna())
    acc_total = len(consensus_df['consensus_accuracy'].dropna())
    
    overall_stats.append({
        'metric': 'Accuracy',
        'meets': acc_counter.get('Meets', 0),
        'partial': acc_counter.get('Partial', 0),
        'not_meet': acc_counter.get('Not Meet', 0),
        'total': acc_total,
        'meets_pct': acc_counter.get('Meets', 0) / acc_total * 100 if acc_total > 0 else 0,
        'partial_pct': acc_counter.get('Partial', 0) / acc_total * 100 if acc_total > 0 else 0,
        'not_meet_pct': acc_counter.get('Not Meet', 0) / acc_total * 100 if acc_total > 0 else 0
    })
    
    # Detail
    det_counter = Counter(consensus_df['consensus_detail'].dropna())
    det_total = len(consensus_df['consensus_detail'].dropna())
    
    overall_stats.append({
        'metric': 'Level of Detail',
        'meets': det_counter.get('Meets', 0),
        'partial': det_counter.get('Partial', 0),
        'not_meet': det_counter.get('Not Meet', 0),
        'total': det_total,
        'meets_pct': det_counter.get('Meets', 0) / det_total * 100 if det_total > 0 else 0,
        'partial_pct': det_counter.get('Partial', 0) / det_total * 100 if det_total > 0 else 0,
        'not_meet_pct': det_counter.get('Not Meet', 0) / det_total * 100 if det_total > 0 else 0
    })
    
    return pd.DataFrame(overall_stats)

def calculate_agreement_statistics(consensus_df):
    """
    Calculate agreement statistics between authors.
    
    Returns:
        Dictionary with agreement statistics
    """
    print("\nCalculating inter-author agreement...")
    
    acc_agreement = consensus_df['accuracy_agreement'].sum()
    acc_total = len(consensus_df['accuracy_agreement'])
    acc_agreement_pct = acc_agreement / acc_total * 100 if acc_total > 0 else 0
    
    det_agreement = consensus_df['detail_agreement'].sum()
    det_total = len(consensus_df['detail_agreement'])
    det_agreement_pct = det_agreement / det_total * 100 if det_total > 0 else 0
    
    stats = {
        'accuracy_agreement': acc_agreement,
        'accuracy_total': acc_total,
        'accuracy_agreement_pct': acc_agreement_pct,
        'detail_agreement': det_agreement,
        'detail_total': det_total,
        'detail_agreement_pct': det_agreement_pct
    }
    
    return stats

def print_formatted_report(consensus_df, by_setting_df, overall_df, agreement_stats):
    """
    Print a comprehensive formatted report.
    """
    print("\n" + "="*80)
    print("CONSENSUS RATING ANALYSIS REPORT")
    print("="*80)
    
    # Overall statistics
    print("\n--- OVERALL STATISTICS ---\n")
    for _, row in overall_df.iterrows():
        print(f"{row['metric']}:")
        print(f"  Meets:     {row['meets']:3d} ({row['meets_pct']:5.1f}%)")
        print(f"  Partial:   {row['partial']:3d} ({row['partial_pct']:5.1f}%)")
        print(f"  Not Meet:  {row['not_meet']:3d} ({row['not_meet_pct']:5.1f}%)")
        print(f"  Total:     {row['total']:3d}")
        print()
    
    # Agreement statistics
    print("--- INTER-AUTHOR AGREEMENT ---\n")
    print(f"Accuracy:        {agreement_stats['accuracy_agreement']}/{agreement_stats['accuracy_total']} ({agreement_stats['accuracy_agreement_pct']:.1f}%)")
    print(f"Level of Detail: {agreement_stats['detail_agreement']}/{agreement_stats['detail_total']} ({agreement_stats['detail_agreement_pct']:.1f}%)")
    
    # By-setting statistics
    print("\n--- STATISTICS BY SETTING ---\n")
    print(by_setting_df.to_string(index=False))
    
    print("\n" + "="*80)

def run_consensus_analysis(author1_file, author2_file, output_dir='consensus_results/', 
                          strategy='conservative'):
    """
    Run complete consensus rating analysis.
    
    Args:
        author1_file: Path to author 1's JSON file
        author2_file: Path to author 2's JSON file
        output_dir: Directory for output files
        strategy: Consensus strategy ('conservative', 'liberal', or 'average')
    
    Returns:
        Dictionary with all results
    """
    os.makedirs(output_dir, exist_ok=True)
    
    print("="*80)
    print("CONSENSUS RATING ANALYSIS")
    print("="*80)
    print(f"Strategy: {strategy}")
    
    # Step 1: Create consensus ratings
    consensus_df = create_consensus_ratings(author1_file, author2_file, strategy)
    consensus_file = os.path.join(output_dir, 'consensus_ratings.csv')
    consensus_df.to_csv(consensus_file, index=False)
    print(f"\nConsensus ratings saved to {consensus_file}")
    
    # Step 2: Calculate statistics by setting
    by_setting_df = calculate_statistics_by_setting(consensus_df)
    by_setting_file = os.path.join(output_dir, 'statistics_by_setting.csv')
    by_setting_df.to_csv(by_setting_file, index=False)
    print(f"By-setting statistics saved to {by_setting_file}")
    
    # Step 3: Calculate overall statistics
    overall_df = calculate_overall_statistics(consensus_df)
    overall_file = os.path.join(output_dir, 'overall_statistics.csv')
    overall_df.to_csv(overall_file, index=False)
    print(f"Overall statistics saved to {overall_file}")
    
    # Step 4: Calculate agreement statistics
    agreement_stats = calculate_agreement_statistics(consensus_df)
    
    # Step 5: Generate LaTeX table
    latex_file = os.path.join(output_dir, 'consensus_table.tex')
    latex_table = generate_latex_table(by_setting_df, latex_file)
    
    # Step 6: Print formatted report
    print_formatted_report(consensus_df, by_setting_df, overall_df, agreement_stats)
    
    # Step 7: Save text report
    report_file = os.path.join(output_dir, 'consensus_report.txt')
    with open(report_file, 'w') as f:
        f.write("CONSENSUS RATING ANALYSIS REPORT\n")
        f.write("="*80 + "\n\n")
        f.write(f"Strategy: {strategy}\n\n")
        f.write("OVERALL STATISTICS\n")
        f.write("-"*80 + "\n")
        f.write(overall_df.to_string(index=False))
        f.write("\n\n")
        f.write("INTER-AUTHOR AGREEMENT\n")
        f.write("-"*80 + "\n")
        f.write(f"Accuracy:        {agreement_stats['accuracy_agreement']}/{agreement_stats['accuracy_total']} ({agreement_stats['accuracy_agreement_pct']:.1f}%)\n")
        f.write(f"Level of Detail: {agreement_stats['detail_agreement']}/{agreement_stats['detail_total']} ({agreement_stats['detail_agreement_pct']:.1f}%)\n")
        f.write("\n\n")
        f.write("STATISTICS BY SETTING\n")
        f.write("-"*80 + "\n")
        f.write(by_setting_df.to_string(index=False))
    
    print(f"\nText report saved to {report_file}")
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE!")
    print("="*80)
    print(f"\nGenerated files in '{output_dir}':")
    print("  1. consensus_ratings.csv - Full consensus data")
    print("  2. statistics_by_setting.csv - Statistics per setting")
    print("  3. overall_statistics.csv - Overall statistics")
    print("  4. consensus_table.tex - LaTeX table")
    print("  5. consensus_report.txt - Text report")
    
    return {
        'consensus': consensus_df,
        'by_setting': by_setting_df,
        'overall': overall_df,
        'agreement': agreement_stats,
        'latex': latex_table
    }

# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    AUTHOR1_FILE = "evaluation_author_2.json"
    AUTHOR2_FILE = "evaluation_author_1.json"
    OUTPUT_DIR = "consensus_results/"
    
    # Run analysis with different strategies if desired
    strategies = ['average']  # Can also try: ['conservative', 'average', 'liberal']
    
    for strategy in strategies:
        print(f"\n\n{'='*80}")
        print(f"Running analysis with '{strategy}' strategy")
        print(f"{'='*80}\n")
        
        results = run_consensus_analysis(
            AUTHOR1_FILE, 
            AUTHOR2_FILE, 
            output_dir=f"{OUTPUT_DIR}{strategy}/",
            strategy=strategy
        )