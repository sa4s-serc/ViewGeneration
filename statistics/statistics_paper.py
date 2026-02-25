import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import friedmanchisquare, wilcoxon
import itertools

# Mapping for ordinal ratings
RATING_MAP = {
    'Meets Expectations': 2,
    'Partially Meets Expectations': 1,
    'Does Not Meet Expectations': 0
}

def calculate_matched_rank_biserial(x, y):
    """Effect size for Wilcoxon: Matched-Pairs Rank-Biserial Correlation"""
    diff = x - y
    diff = diff[diff != 0]
    if len(diff) == 0: return 0
    ranks = pd.Series(diff).abs().rank()
    pos_ranks = ranks[diff > 0].sum()
    neg_ranks = ranks[diff < 0].sum()
    return (pos_ranks - neg_ranks) / (pos_ranks + neg_ranks)

def interpret_effect(r):
    abs_r = abs(r)
    if abs_r < 0.1: return "negligible"
    if abs_r < 0.3: return "small"
    if abs_r < 0.5: return "medium"
    return "large"

def run_rq1_pipeline(df, metric_col_suffix):
    """Complete pipeline for a single 3Cs metric"""
    print(f"\n{'='*30} ANALYZING: {metric_col_suffix} {'='*30}")
    
    # Identify model columns
    models = {
        'ArchView (AV)': f'approach_claude_LLM_{metric_col_suffix}_Rating',
        'GPA (Claude Code)': f'agent_claude_LLM_{metric_col_suffix}_Rating',
        'Few-Shot (FS)': f'fewshot_claude_LLM_{metric_col_suffix}_Rating',
        'One-Shot (OS)': f'1shot_claude_LLM_{metric_col_suffix}_Rating',
        'Zero-Shot (ZS)': f'zeroshot_claude_LLM_{metric_col_suffix}_Rating'
    }

    # Prepare numeric data (Paired)
    analysis_df = pd.DataFrame()
    for label, col in models.items():
        analysis_df[label] = df[col].map(RATING_MAP).fillna(0)

    # 1. Friedman Test (Omnibus)
    stat, p_omnibus = friedmanchisquare(*[analysis_df[m] for m in models.keys()])
    print(f"Friedman Test: Q={stat:.4f}, p={p_omnibus:.4e}")

    # 2. Post-hoc Wilcoxon with Bonferroni
    target = 'ArchView (AV)'
    others = [m for m in models.keys() if m != target]
    adj_alpha = 0.05 / len(others)
    
    results = []
    for other in others:
        w_stat, p_val = wilcoxon(analysis_df[target], analysis_df[other], zero_method='pratt')
        r = calculate_matched_rank_biserial(analysis_df[target], analysis_df[other])
        results.append({
            'Metric': metric_col_suffix,
            'Comparison': f"AV vs {other}",
            'p-value': p_val,
            'r (Effect)': r,
            'Interpretation': interpret_effect(r),
            'Sig': 'Yes' if p_val < adj_alpha else 'No'
        })
    
    return pd.DataFrame(results), analysis_df

# --- Execution ---
df = pd.read_csv('final_combined_all_models.csv')  # Load your data here
# Below assumes 'df' is loaded from your provided CSV structure.

metrics = ['Clarity', 'Completeness', 'Consistency']
all_stats = []
plot_data = []

for m in metrics:
    stats_df, numeric_df = run_rq1_pipeline(df, m)
    all_stats.append(stats_df)
    
    # Melt for plotting
    melted = numeric_df.melt(var_name='Approach', value_name='Score')
    melted['Metric'] = m
    plot_data.append(melted)

# --- Plotting ---
plt.figure(figsize=(15, 5))
full_plot_df = pd.concat(plot_data)
sns.barplot(data=full_plot_df, x='Metric', y='Score', hue='Approach', palette='viridis', capsize=.1)
plt.title("Mean Performance Ratings Across Approaches (Paired Comparison)")
plt.ylabel("Rating (0=Fail, 1=Partial, 2=Meets)")
plt.savefig('rq1_performance.png')
plt.show()

# --- LaTeX Export ---
final_results = pd.concat(all_stats)
print("\nLaTeX Table Code:")
print(final_results.to_latex(index=False))