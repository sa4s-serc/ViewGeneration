"""
Human Evaluation Analysis Script
=================================
This script processes human evaluation data for architectural view generation,
calculates inter-rater reliability, validates LLM-as-a-Judge ratings,
and generates statistical summaries.

Author: [Your Name]
Date: [Current Date]
"""

import json
import pandas as pd
import numpy as np
from collections import defaultdict, Counter
from sklearn.metrics import cohen_kappa_score, confusion_matrix
from scipy.stats import spearmanr
import matplotlib.pyplot as plt
import seaborn as sns

# =============================================================================
# CONFIGURATION
# =============================================================================

# File paths
AUTHOR1_FILE = "author1_evaluations.json"
AUTHOR2_FILE = "author2_evaluations.json"
LLM_JUDGE_FILE = "llm_judge_ratings.json"
OUTPUT_DIR = "analysis_results/"

# Rating mappings for numerical conversion
RATING_MAP = {
    'Meets Expectations': 3,
    'Meets': 3,
    'meets': 3,
    'Partially Meets Expectations': 2,
    'Partial': 2,
    'partial': 2,
    'Partially Meets': 2,
    'Does Not Meet Expectations': 1,
    'Not Meet': 1,
    'not meet': 1,
    'Does Not Meet': 1,
    'Doesn\'t Meet': 1,
}

# Experimental settings
SETTINGS = ['zero-shot', 'one-shot', 'few-shot', 'agent', 'archview']
MODELS = ['DeepSeek-V2.5', 'ChatGPT-4o', 'Claude-3.5 Sonnet']

# =============================================================================
# DATA LOADING FUNCTIONS
# =============================================================================

def load_json_data(filepath):
    """Load JSON data from file."""
    with open(filepath, 'r') as f:
        return json.load(f)

def parse_evaluation_data(data):
    """
    Parse nested JSON structure into flat DataFrame.
    
    Structure: {sample_id: {setting_id: {evaluation_fields}}}
    Returns: DataFrame with columns [sample_id, setting_id, metric, value, justification]
    """
    rows = []
    for sample_id, settings in data.items():
        for setting_id, evaluation in settings.items():
            row = {
                'sample_id': sample_id,
                'setting_id': setting_id,
                'clarityAgree': evaluation.get('clarityAgree'),
                'clarityJustification': evaluation.get('clarityJustification', ''),
                'completenessAgree': evaluation.get('completenessAgree'),
                'completenessJustification': evaluation.get('completenessJustification', ''),
                'consistencyAgree': evaluation.get('consistencyAgree'),
                'consistencyJustification': evaluation.get('consistencyJustification', ''),
                'accuracyRating': evaluation.get('accuracyRating'),
                'accuracyJustification': evaluation.get('accuracyJustification', ''),
                'detailRating': evaluation.get('detailRating'),
                'detailJustification': evaluation.get('detailJustification', ''),
                'timestamp': evaluation.get('timestamp')
            }
            rows.append(row)
    return pd.DataFrame(rows)

# =============================================================================
# INTER-RATER RELIABILITY ANALYSIS
# =============================================================================

def calculate_inter_rater_reliability(author1_df, author2_df):
    """
    Calculate Cohen's Kappa for inter-rater reliability.
    
    Returns: Dictionary with kappa scores for each metric
    """
    # Merge dataframes on sample_id and setting_id
    merged = pd.merge(
        author1_df, 
        author2_df, 
        on=['sample_id', 'setting_id'], 
        suffixes=('_a1', '_a2')
    )
    
    results = {}
    
    # Boolean agreement metrics (3Cs)
    for metric in ['clarityAgree', 'completenessAgree', 'consistencyAgree']:
        col_a1 = f'{metric}_a1'
        col_a2 = f'{metric}_a2'
        
        # Filter out rows where either value is None/NaN
        valid_mask = merged[col_a1].notna() & merged[col_a2].notna()
        valid_data = merged[valid_mask]
        
        if len(valid_data) == 0:
            print(f"Warning: No valid data for {metric}")
            results[metric] = {
                'kappa': None,
                'agreement_pct': None,
                'interpretation': 'No valid data',
                'n_valid': 0
            }
            continue
        
        # Convert boolean to numeric
        a1_numeric = valid_data[col_a1].astype(int)
        a2_numeric = valid_data[col_a2].astype(int)
        
        kappa = cohen_kappa_score(a1_numeric, a2_numeric)
        agreement_pct = (a1_numeric == a2_numeric).mean() * 100
        
        results[metric] = {
            'kappa': kappa,
            'agreement_pct': agreement_pct,
            'interpretation': interpret_kappa(kappa),
            'n_valid': len(valid_data)
        }
    
    # Rating metrics (Accuracy and Detail)
    for metric in ['accuracyRating', 'detailRating']:
        col_a1 = f'{metric}_a1'
        col_a2 = f'{metric}_a2'
        
        # Filter out rows where either value is None/NaN
        valid_mask = merged[col_a1].notna() & merged[col_a2].notna()
        valid_data = merged[valid_mask]
        
        if len(valid_data) == 0:
            print(f"Warning: No valid data for {metric}")
            results[metric] = {
                'kappa': None,
                'agreement_pct': None,
                'interpretation': 'No valid data',
                'n_valid': 0
            }
            continue
        
        # Convert ratings to numeric
        a1_numeric = valid_data[col_a1].map(RATING_MAP)
        a2_numeric = valid_data[col_a2].map(RATING_MAP)
        
        # Check for unmapped values
        unmapped_a1 = a1_numeric.isna().sum()
        unmapped_a2 = a2_numeric.isna().sum()
        
        if unmapped_a1 > 0 or unmapped_a2 > 0:
            print(f"Warning: {metric} has unmapped values (A1: {unmapped_a1}, A2: {unmapped_a2})")
            # Print unique values to help debug
            print(f"  Unique values in A1: {valid_data[col_a1].unique()}")
            print(f"  Unique values in A2: {valid_data[col_a2].unique()}")
        
        # Remove rows with unmapped values
        final_valid_mask = a1_numeric.notna() & a2_numeric.notna()
        a1_numeric = a1_numeric[final_valid_mask]
        a2_numeric = a2_numeric[final_valid_mask]
        
        if len(a1_numeric) == 0:
            print(f"Warning: No valid mappable data for {metric}")
            results[metric] = {
                'kappa': None,
                'agreement_pct': None,
                'interpretation': 'No valid mappable data',
                'n_valid': 0
            }
            continue
        
        kappa = cohen_kappa_score(a1_numeric, a2_numeric)
        agreement_pct = (a1_numeric == a2_numeric).mean() * 100
        
        results[metric] = {
            'kappa': kappa,
            'agreement_pct': agreement_pct,
            'interpretation': interpret_kappa(kappa),
            'n_valid': len(a1_numeric)
        }
    
    return results, merged

def interpret_kappa(kappa):
    """Interpret Cohen's Kappa score."""
    if kappa > 0.8:
        return "Strong agreement"
    elif kappa > 0.6:
        return "Substantial agreement"
    elif kappa > 0.4:
        return "Moderate agreement"
    else:
        return "Poor agreement"

def identify_disagreements(merged_df):
    """
    Identify cases where authors disagreed.
    
    Returns: DataFrame with disagreement cases
    """
    disagreements = []
    
    for metric in ['clarityAgree', 'completenessAgree', 'consistencyAgree',
                   'accuracyRating', 'detailRating']:
        col_a1 = f'{metric}_a1'
        col_a2 = f'{metric}_a2'
        
        # Only compare where both have values
        valid_mask = merged_df[col_a1].notna() & merged_df[col_a2].notna()
        valid_df = merged_df[valid_mask]
        
        # Find disagreements
        disagree_mask = valid_df[col_a1] != valid_df[col_a2]
        disagree_cases = valid_df[disagree_mask][['sample_id', 'setting_id', col_a1, col_a2]].copy()
        
        if len(disagree_cases) > 0:
            disagree_cases['metric'] = metric
            disagree_cases = disagree_cases.rename(columns={
                col_a1: 'author1_rating',
                col_a2: 'author2_rating'
            })
            disagreements.append(disagree_cases)
    
    if disagreements:
        return pd.concat(disagreements, ignore_index=True)
    return pd.DataFrame()
# =============================================================================
# CONSENSUS GENERATION
# =============================================================================

def create_consensus_ratings(author1_df, author2_df, resolution_strategy='conservative'):
    """
    Create consensus ratings from two authors.
    
    Args:
        resolution_strategy: 'conservative' (take lower rating) or 'average'
    
    Returns: DataFrame with consensus ratings
    """
    merged = pd.merge(
        author1_df, 
        author2_df, 
        on=['sample_id', 'setting_id'], 
        suffixes=('_a1', '_a2')
    )
    
    consensus_df = merged[['sample_id', 'setting_id']].copy()
    
    # For boolean metrics, use majority (if same, keep; if different, flag)
    for metric in ['clarityAgree', 'completenessAgree', 'consistencyAgree']:
        col_a1 = f'{metric}_a1'
        col_a2 = f'{metric}_a2'
        
        # Handle None values
        def consensus_bool(row):
            val1 = row[col_a1]
            val2 = row[col_a2]
            
            # If both are None, return None
            if pd.isna(val1) and pd.isna(val2):
                return None
            # If one is None, use the other
            if pd.isna(val1):
                return val2
            if pd.isna(val2):
                return val1
            # If both agree, return the value
            if val1 == val2:
                return val1
            # If they disagree, flag it (you can change this logic)
            return None  # or return the more conservative one
        
        consensus_df[metric] = merged.apply(consensus_bool, axis=1)
        consensus_df[f'{metric}_flagged'] = (merged[col_a1] != merged[col_a2]) & merged[col_a1].notna() & merged[col_a2].notna()
    
    # For ratings, apply resolution strategy
    for metric in ['accuracyRating', 'detailRating']:
        col_a1 = f'{metric}_a1'
        col_a2 = f'{metric}_a2'
        
        def consensus_rating(row):
            val1 = row[col_a1]
            val2 = row[col_a2]
            
            # If both are None, return None
            if pd.isna(val1) and pd.isna(val2):
                return None
            # If one is None, use the other
            if pd.isna(val1):
                return val2
            if pd.isna(val2):
                return val1
            
            # If both have values
            if resolution_strategy == 'conservative':
                # Take the lower (more critical) rating
                num1 = RATING_MAP.get(val1)
                num2 = RATING_MAP.get(val2)
                
                if num1 is None or num2 is None:
                    return None
                
                min_num = min(num1, num2)
                # Map back to text
                reverse_map = {v: k for k, v in RATING_MAP.items() if k in ['Meets', 'Partial', 'Not Meet']}
                return reverse_map.get(min_num)
                
            elif resolution_strategy == 'average':
                # Average and round
                num1 = RATING_MAP.get(val1)
                num2 = RATING_MAP.get(val2)
                
                if num1 is None or num2 is None:
                    return None
                
                avg_num = int(round((num1 + num2) / 2))
                reverse_map = {v: k for k, v in RATING_MAP.items() if k in ['Meets', 'Partial', 'Not Meet']}
                return reverse_map.get(avg_num)
            
            # Default: if they agree, return the value
            if val1 == val2:
                return val1
            return None
        
        consensus_df[metric] = merged.apply(consensus_rating, axis=1)
    
    # Combine justifications
    for metric in ['clarity', 'completeness', 'consistency', 'accuracy', 'detail']:
        just_col = f'{metric}Justification'
        col_a1 = f'{just_col}_a1'
        col_a2 = f'{just_col}_a2'
        
        if col_a1 in merged.columns and col_a2 in merged.columns:
            def combine_justifications(row):
                j1 = str(row[col_a1]) if pd.notna(row[col_a1]) else ""
                j2 = str(row[col_a2]) if pd.notna(row[col_a2]) else ""
                
                if j1 and j2:
                    return f"{j1} | {j2}"
                elif j1:
                    return j1
                elif j2:
                    return j2
                return ""
            
            consensus_df[just_col] = merged.apply(combine_justifications, axis=1)
    
    return consensus_df

# =============================================================================
# LLM-AS-A-JUDGE VALIDATION
# =============================================================================

def validate_llm_judge(consensus_df, llm_judge_df):
    """
    Validate LLM-as-a-Judge ratings against human consensus.
    
    Returns: Dictionary with validation metrics
    """
    # Merge consensus with LLM ratings
    merged = pd.merge(
        consensus_df,
        llm_judge_df,
        on=['sample_id', 'setting_id'],
        suffixes=('_human', '_llm')
    )
    
    validation_results = {}
    
    # For 3Cs (boolean agreement)
    for metric in ['clarityAgree', 'completenessAgree', 'consistencyAgree']:
        human_col = f'{metric}_human'
        llm_col = f'{metric}_llm'
        
        if llm_col in merged.columns:
            agreement = (merged[human_col] == merged[llm_col]).mean() * 100
            
            # Calculate kappa
            kappa = cohen_kappa_score(
                merged[human_col].astype(int),
                merged[llm_col].astype(int)
            )
            
            # Determine tendency
            llm_harsher = (merged[llm_col].astype(int) < merged[human_col].astype(int)).sum()
            llm_lenient = (merged[llm_col].astype(int) > merged[human_col].astype(int)).sum()
            
            if llm_harsher > llm_lenient:
                tendency = "Harsher"
            elif llm_lenient > llm_harsher:
                tendency = "Lenient"
            else:
                tendency = "Neutral"
            
            validation_results[metric] = {
                'agreement_pct': agreement,
                'kappa': kappa,
                'tendency': tendency
            }
    
    return validation_results, merged

def create_confusion_matrices(merged_validation_df):
    """
    Create confusion matrices for LLM vs Human ratings.
    
    Returns: Dictionary of confusion matrices
    """
    matrices = {}
    
    for metric in ['accuracyRating', 'detailRating']:
        human_col = f'{metric}_human'
        llm_col = f'{metric}_llm'
        
        if llm_col in merged_validation_df.columns:
            human_numeric = merged_validation_df[human_col].map(RATING_MAP)
            llm_numeric = merged_validation_df[llm_col].map(RATING_MAP)
            
            cm = confusion_matrix(
                human_numeric, 
                llm_numeric,
                labels=[1, 2, 3]
            )
            
            matrices[metric] = {
                'matrix': cm,
                'labels': ['Not Meet', 'Partial', 'Meets']
            }
    
    return matrices

# =============================================================================
# QUALITATIVE ANALYSIS
# =============================================================================

def analyze_justifications(consensus_df):
    """
    Analyze justification text for common themes.
    
    Returns: Dictionary with theme counts
    """
    themes = {
        'missing_components': 0,
        'extra_components': 0,
        'too_many_components': 0,
        'granularity_mismatch': 0,
        'too_detailed': 0,
        'wrong_level': 0,
        'complex_connectors': 0,
        'matching_structure': 0
    }
    
    # Keywords for each theme
    keywords = {
        'missing_components': ['missing', 'omitted', 'absent', 'not included'],
        'extra_components': ['extra', 'additional', 'unnecessary'],
        'too_many_components': ['too many', 'excessive'],
        'granularity_mismatch': ['granularity', 'level mismatch', 'abstraction'],
        'too_detailed': ['too detailed', 'too detail', 'overly detailed'],
        'wrong_level': ['wrong level', 'incorrect level', 'different level'],
        'complex_connectors': ['complex connector', 'complicated relationship'],
        'matching_structure': ['matching', 'matches', 'similar structure']
    }
    
    # Analyze all justification fields
    justification_cols = [col for col in consensus_df.columns if 'Justification' in col]
    
    for col in justification_cols:
        for _, row in consensus_df.iterrows():
            text = str(row[col]).lower()
            
            for theme, keyword_list in keywords.items():
                if any(keyword in text for keyword in keyword_list):
                    themes[theme] += 1
    
    return themes

def extract_specific_issues(consensus_df):
    """
    Extract specific issues mentioned in justifications.
    
    Returns: DataFrame with categorized issues
    """
    issues = []
    
    for _, row in consensus_df.iterrows():
        sample_id = row['sample_id']
        setting_id = row['setting_id']
        
        # Analyze accuracy justification
        acc_just = str(row.get('accuracyJustification', '')).lower()
        detail_just = str(row.get('detailJustification', '')).lower()
        
        issue_entry = {
            'sample_id': sample_id,
            'setting_id': setting_id,
            'has_missing_components': 'missing' in acc_just,
            'has_extra_components': 'extra' in acc_just or 'too many' in acc_just,
            'granularity_issue': 'level' in detail_just or 'detailed' in detail_just,
            'complexity_issue': 'complex' in acc_just or 'complex' in detail_just
        }
        
        issues.append(issue_entry)
    
    return pd.DataFrame(issues)

# =============================================================================
# STATISTICAL ANALYSIS
# =============================================================================

def calculate_rating_distributions(consensus_df):
    """
    Calculate distribution of ratings across all samples.
    
    Returns: Dictionary with distributions
    """
    distributions = {}
    
    for metric in ['accuracyRating', 'detailRating']:
        dist = consensus_df[metric].value_counts(normalize=True) * 100
        distributions[metric] = dist.to_dict()
    
    return distributions

def analyze_by_setting(consensus_df):
    """
    Analyze ratings grouped by experimental setting.
    
    Returns: DataFrame with statistics per setting
    """
    # Map setting_id to setting name (you'll need to provide this mapping)
    # For now, using setting_id directly
    
    setting_stats = []
    
    for setting_id in consensus_df['setting_id'].unique():
        subset = consensus_df[consensus_df['setting_id'] == setting_id]
        
        # Calculate distributions for this setting
        acc_dist = subset['accuracyRating'].value_counts()
        detail_dist = subset['detailRating'].value_counts()
        
        stats = {
            'setting_id': setting_id,
            'n_samples': len(subset),
            'accuracy_meets': acc_dist.get('Meets', 0),
            'accuracy_partial': acc_dist.get('Partial', 0),
            'accuracy_not_meet': acc_dist.get('Not Meet', 0),
            'detail_meets': detail_dist.get('Meets', 0),
            'detail_partial': detail_dist.get('Partial', 0),
            'detail_not_meet': detail_dist.get('Not Meet', 0)
        }
        
        setting_stats.append(stats)
    
    return pd.DataFrame(setting_stats)

def correlation_analysis(consensus_df):
    """
    Analyze correlation between accuracy and detail ratings.
    
    Returns: Correlation coefficient and p-value
    """
    accuracy_numeric = consensus_df['accuracyRating'].map(RATING_MAP)
    detail_numeric = consensus_df['detailRating'].map(RATING_MAP)
    
    correlation, p_value = spearmanr(accuracy_numeric, detail_numeric)
    
    return {
        'correlation': correlation,
        'p_value': p_value,
        'interpretation': 'Significant' if p_value < 0.05 else 'Not significant'
    }

# =============================================================================
# VISUALIZATION FUNCTIONS
# =============================================================================

def plot_inter_rater_reliability(reliability_results, output_path):
    """Create bar plot of inter-rater reliability scores."""
    metrics = list(reliability_results.keys())
    kappas = [reliability_results[m]['kappa'] for m in metrics]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(metrics, kappas)
    
    # Color bars based on interpretation
    colors = []
    for kappa in kappas:
        if kappa > 0.8:
            colors.append('green')
        elif kappa > 0.6:
            colors.append('yellow')
        elif kappa > 0.4:
            colors.append('orange')
        else:
            colors.append('red')
    
    for bar, color in zip(bars, colors):
        bar.set_color(color)
    
    plt.ylabel("Cohen's Kappa")
    plt.title("Inter-Rater Reliability")
    plt.xticks(rotation=45, ha='right')
    plt.axhline(y=0.8, color='g', linestyle='--', label='Strong')
    plt.axhline(y=0.6, color='y', linestyle='--', label='Substantial')
    plt.axhline(y=0.4, color='orange', linestyle='--', label='Moderate')
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_rating_distributions(consensus_df, output_path):
    """Create stacked bar chart of rating distributions."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    for idx, metric in enumerate(['accuracyRating', 'detailRating']):
        dist = consensus_df[metric].value_counts()
        
        axes[idx].bar(['Meets', 'Partial', 'Not Meet'], 
                     [dist.get('Meets', 0), dist.get('Partial', 0), dist.get('Not Meet', 0)],
                     color=['green', 'yellow', 'red'])
        axes[idx].set_title(f'{metric} Distribution')
        axes[idx].set_ylabel('Count')
    
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_confusion_matrix(cm, labels, title, output_path):
    """Plot confusion matrix heatmap."""
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=labels, yticklabels=labels)
    plt.title(title)
    plt.ylabel('Human Rating')
    plt.xlabel('LLM Rating')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

# =============================================================================
# REPORT GENERATION
# =============================================================================

def generate_latex_tables(reliability_results, validation_results, 
                         rating_distributions, setting_analysis):
    """
    Generate LaTeX tables for paper.
    
    Returns: Dictionary of LaTeX table strings
    """
    tables = {}
    
    # Table 1: Inter-Rater Reliability
    irr_table = """
\\begin{table}[ht]
\\centering
\\caption{Inter-rater reliability between human evaluators}
\\begin{tabular}{lccc}
\\toprule
Metric & Cohen's Kappa & Interpretation & N Valid \\\\
\\midrule
"""
    for metric, results in reliability_results.items():
        metric_name = metric.replace('Agree', ' Agreement').replace('Rating', ' Rating')
        kappa_str = f"{results['kappa']:.3f}" if results['kappa'] is not None else "N/A"
        irr_table += f"{metric_name} & {kappa_str} & {results['interpretation']} & {results['n_valid']} \\\\\n"
    
    irr_table += """\\bottomrule
\\end{tabular}
\\label{tab:inter_rater_reliability}
\\end{table}
"""
    tables['inter_rater'] = irr_table
    
    # Table 2: LLM Validation
    llm_val_table = """
\\begin{table}[ht]
\\centering
\\caption{LLM-as-a-Judge validation against human consensus}
\\begin{tabular}{lccc}
\\toprule
Dimension & Agreement (\\%) & Cohen's Kappa & Tendency \\\\
\\midrule
"""
    for metric, results in validation_results.items():
        metric_name = metric.replace('Agree', '')
        llm_val_table += f"{metric_name} & {results['agreement_pct']:.1f}\\% & {results['kappa']:.3f} & {results['tendency']} \\\\\n"
    
    llm_val_table += """\\bottomrule
\\end{tabular}
\\label{tab:llm_validation}
\\end{table}
"""
    tables['llm_validation'] = llm_val_table
    
    # Table 3: Rating Distributions
    dist_table = """
\\begin{table}[ht]
\\centering
\\caption{Human evaluation rating distributions}
\\begin{tabular}{lccc}
\\toprule
\\multirow{2}{*}{Metric} & \\multicolumn{3}{c}{Rating Distribution} \\\\
\\cmidrule{2-4}
& Meets & Partial & Not Meet \\\\
\\midrule
"""
    for metric, dist in rating_distributions.items():
        total = sum(dist.values())
        meets = dist.get('Meets', 0) / total * 100
        partial = dist.get('Partial', 0) / total * 100
        not_meet = dist.get('Not Meet', 0) / total * 100
        
        metric_name = metric.replace('Rating', '')
        dist_table += f"{metric_name} & {meets:.1f}\\% & {partial:.1f}\\% & {not_meet:.1f}\\% \\\\\n"
    
    dist_table += """\\bottomrule
\\end{tabular}
\\label{tab:rating_distributions}
\\end{table}
"""
    tables['distributions'] = dist_table
    
    return tables

def generate_text_report(reliability_results, validation_results, 
                        theme_analysis, correlation_results):
    """
    Generate comprehensive text report.
    
    Returns: Formatted string report
    """
    report = """
HUMAN EVALUATION ANALYSIS REPORT
=================================

1. INTER-RATER RELIABILITY
---------------------------
"""
    for metric, results in reliability_results.items():
        report += f"\n{metric}:\n"
        report += f"  Cohen's Kappa: {results['kappa']:.3f}\n"
        report += f"  Agreement: {results['agreement_pct']:.1f}%\n"
        report += f"  Interpretation: {results['interpretation']}\n"
    
    report += """
2. LLM-AS-A-JUDGE VALIDATION
-----------------------------
"""
    for metric, results in validation_results.items():
        report += f"\n{metric}:\n"
        report += f"  Agreement with humans: {results['agreement_pct']:.1f}%\n"
        report += f"  Cohen's Kappa: {results['kappa']:.3f}\n"
        report += f"  Tendency: {results['tendency']}\n"
    
    report += """
3. QUALITATIVE THEME ANALYSIS
------------------------------
"""
    for theme, count in theme_analysis.items():
        report += f"{theme}: {count} occurrences\n"
    
    report += f"""
4. CORRELATION ANALYSIS
-----------------------
Accuracy vs Detail Correlation: {correlation_results['correlation']:.3f}
P-value: {correlation_results['p_value']:.4f}
Interpretation: {correlation_results['interpretation']}
"""
    
    return report

# =============================================================================
# MAIN ANALYSIS PIPELINE
# =============================================================================

def run_complete_analysis(author1_file, author2_file, llm_judge_file=None, 
                         output_dir='analysis_results/'):
    """
    Run complete analysis pipeline.
    
    Args:
        author1_file: Path to author 1's evaluation JSON
        author2_file: Path to author 2's evaluation JSON
        llm_judge_file: Path to LLM judge ratings JSON (optional)
        output_dir: Directory for output files
    
    Returns: Dictionary with all analysis results
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    print("Loading data...")
    author1_data = load_json_data(author1_file)
    author2_data = load_json_data(author2_file)
    
    author1_df = parse_evaluation_data(author1_data)
    author2_df = parse_evaluation_data(author2_data)
    
    print(f"Author 1: {len(author1_df)} evaluations")
    print(f"Author 2: {len(author2_df)} evaluations")
    
    # Step 1: Inter-rater reliability
    print("\n1. Calculating inter-rater reliability...")
    reliability_results, merged_df = calculate_inter_rater_reliability(author1_df, author2_df)
    
    # Save reliability results
    plot_inter_rater_reliability(reliability_results, 
                                 os.path.join(output_dir, 'inter_rater_reliability.png'))
    
    # Step 2: Identify disagreements
    print("\n2. Identifying disagreements...")
    disagreements = identify_disagreements(merged_df)
    if len(disagreements) > 0:
        disagreements.to_csv(os.path.join(output_dir, 'disagreements.csv'), index=False)
        print(f"   Found {len(disagreements)} disagreement cases")
    else:
        print("   No disagreements found")
    
    # Step 3: Create consensus
    print("\n3. Creating consensus ratings...")
    consensus_df = create_consensus_ratings(author1_df, author2_df, 
                                           resolution_strategy='conservative')
    consensus_df.to_csv(os.path.join(output_dir, 'consensus_ratings.csv'), index=False)
    
    # Step 4: Rating distributions
    print("\n4. Analyzing rating distributions...")
    rating_distributions = calculate_rating_distributions(consensus_df)
    plot_rating_distributions(consensus_df, 
                             os.path.join(output_dir, 'rating_distributions.png'))
    
    # Step 5: By-setting analysis
    print("\n5. Analyzing by experimental setting...")
    setting_analysis = analyze_by_setting(consensus_df)
    setting_analysis.to_csv(os.path.join(output_dir, 'setting_analysis.csv'), index=False)
    
    # Step 6: Qualitative analysis
    print("\n6. Analyzing justifications...")
    theme_analysis = analyze_justifications(consensus_df)
    issue_analysis = extract_specific_issues(consensus_df)
    issue_analysis.to_csv(os.path.join(output_dir, 'issue_analysis.csv'), index=False)
    
    # Step 7: Correlation analysis
    print("\n7. Correlation analysis...")
    correlation_results = correlation_analysis(consensus_df)
    
    # Step 8: LLM validation (if data available)
    validation_results = None
    # if llm_judge_file:
    #     print("\n8. Validating LLM-as-a-Judge...")
    #     llm_judge_data = load_json_data(llm_judge_file)
    #     llm_judge_df = parse_evaluation_data(llm_judge_data)
        
    #     validation_results, validation_merged = validate_llm_judge(consensus_df, llm_judge_df)
        
    #     # Create confusion matrices
    #     matrices = create_confusion_matrices(validation_merged)
    #     for metric, mat_data in matrices.items():
    #         plot_confusion_matrix(mat_data['matrix'], mat_data['labels'],
    #                             f'LLM vs Human: {metric}',
    #                             os.path.join(output_dir, f'confusion_matrix_{metric}.png'))
    
    # Step 9: Generate reports
    print("\n9. Generating reports...")
    
    # LaTeX tables
    latex_tables = generate_latex_tables(reliability_results, validation_results or {}, 
                                        rating_distributions, setting_analysis)
    with open(os.path.join(output_dir, 'latex_tables.tex'), 'w') as f:
        for table_name, table_content in latex_tables.items():
            f.write(f"% {table_name}\n")
            f.write(table_content)
            f.write("\n\n")
    
    # Text report
    text_report = generate_text_report(reliability_results, validation_results or {},
                                      theme_analysis, correlation_results)
    with open(os.path.join(output_dir, 'analysis_report.txt'), 'w') as f:
        f.write(text_report)
    
    print(f"\nAnalysis complete! Results saved to {output_dir}")
    
    # Return all results
    return {
        'reliability': reliability_results,
        'validation': validation_results,
        'consensus': consensus_df,
        'distributions': rating_distributions,
        'setting_analysis': setting_analysis,
        'themes': theme_analysis,
        'correlation': correlation_results,
        'disagreements': disagreements
    }

# =============================================================================
# USAGE EXAMPLE
# =============================================================================

if __name__ == "__main__":
    # Run the complete analysis
    results = run_complete_analysis(
        author1_file="evaluation_author_2.json",
        author2_file="evaluation_author_1.json",
        llm_judge_file="llm_judge_ratings.json",  
        output_dir="analysis_results/"
    )
    
    # Print summary
    print("\n" + "="*60)
    print("SUMMARY OF KEY FINDINGS")
    print("="*60)
    
    print("\nInter-Rater Reliability:")
    for metric, res in results['reliability'].items():
        print(f"  {metric}: κ = {res['kappa']:.3f} ({res['interpretation']})")
    
    if results['validation']:
        print("\nLLM-as-a-Judge Validation:")
        for metric, res in results['validation'].items():
            print(f"  {metric}: {res['agreement_pct']:.1f}% agreement ({res['tendency']})")
    
    print("\nMost Common Issues:")
    sorted_themes = sorted(results['themes'].items(), key=lambda x: x[1], reverse=True)
    for theme, count in sorted_themes[:5]:
        print(f"  {theme}: {count} occurrences")
    
    print("\nCorrelation:")
    print(f"  Accuracy vs Detail: r = {results['correlation']['correlation']:.3f}")
    print(f"  Significance: {results['correlation']['interpretation']}")