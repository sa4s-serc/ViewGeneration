"""
Inter-View Relationship Analysis
================================

This script focuses specifically on understanding relationships BETWEEN
different types of architectural views. Key questions:

1. Do models that do well on deployment views also do well on control flow?
2. Are certain notations universally easier/harder across all models?
3. How does granularity (scope) affect consistency across view types?
4. Are there "clusters" of similar view types based on model performance patterns?
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from scipy.stats import spearmanr, kendalltau
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-whitegrid')
OUTPUT_DIR = Path("./analysis_outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


def load_all_data(data_dir: Path) -> dict:
    """Load and organize all CSV files."""
    data = {
        'by_concern': {},
        'by_scope': {},
        'by_notation': {},
        'by_qas': {}
    }
    
    for f in data_dir.glob("simple_table_*.csv"):
        name = f.stem.replace("simple_table_", "")
        df = pd.read_csv(f)
        
        # Parse model names
        df['Strategy'] = df['Model'].apply(lambda x: 
            'zero-shot' if 'zero' in x.lower() else
            'one-shot' if '1shot' in x.lower() else
            'few-shot' if 'few' in x.lower() else
            'agent' if 'agent' in x.lower() else
            'approach' if 'approach' in x.lower() else 'unknown')
        
        df['Base_Model'] = df['Model'].apply(lambda x:
            'Claude' if 'claude' in x.lower() else
            'DeepSeek' if 'deepseek' in x.lower() else
            'GPT' if 'gpt' in x.lower() else 'Unknown')
        
        if name.startswith("concern_"):
            data['by_concern'][name.replace("concern_", "")] = df
        elif name.startswith("scope_"):
            data['by_scope'][name.replace("scope_", "")] = df
        elif name.startswith("archnotation_"):
            data['by_notation'][name.replace("archnotation_", "")] = df
        elif name.startswith("qas_"):
            data['by_qas'][name.replace("qas_", "")] = df
    
    return data


# ============================================================================
# Analysis 1: Cross-View Performance Correlation Matrix
# ============================================================================
def analyze_cross_view_correlation(data: dict, metric: str = 'SSIM'):
    """
    For each model configuration, compute performance across all view types.
    Then correlate: does good performance on view A predict good performance on view B?
    """
    
    # Build matrix: rows = model configs, columns = view types (concerns)
    view_types = list(data['by_concern'].keys())
    model_configs = set()
    
    for df in data['by_concern'].values():
        model_configs.update(df['Model'].unique())
    
    model_configs = sorted(model_configs)
    
    # Create performance matrix
    perf_matrix = pd.DataFrame(index=model_configs, columns=view_types, dtype=float)
    
    for view, df in data['by_concern'].items():
        for _, row in df.iterrows():
            if metric in row and pd.notna(row[metric]):
                perf_matrix.loc[row['Model'], view] = row[metric]
    
    # Drop views/models with too much missing data
    perf_matrix = perf_matrix.dropna(axis=1, thresh=len(model_configs)*0.5)
    perf_matrix = perf_matrix.dropna(axis=0, thresh=len(perf_matrix.columns)*0.5)
    
    if perf_matrix.shape[1] < 2:
        print("Not enough view types for correlation analysis")
        return None
    
    # Compute correlation between view types
    view_corr = perf_matrix.corr(method='spearman')
    
    # Plot
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    
    # Correlation heatmap
    mask = np.triu(np.ones_like(view_corr, dtype=bool))
    sns.heatmap(view_corr, annot=True, fmt='.2f', cmap='RdBu_r', center=0,
                ax=axes[0], vmin=-1, vmax=1, mask=mask)
    axes[0].set_title(f'Cross-View Performance Correlation\n(Based on {metric})', 
                     fontweight='bold', fontsize=12)
    
    # Hierarchical clustering of views
    if perf_matrix.shape[1] >= 3:
        linkage_matrix = linkage(perf_matrix.T.fillna(perf_matrix.mean()), method='ward')
        dendrogram(linkage_matrix, labels=perf_matrix.columns, ax=axes[1], 
                  leaf_rotation=45)
        axes[1].set_title('View Type Clustering\n(Similar views cluster together)', 
                         fontweight='bold', fontsize=12)
        axes[1].set_ylabel('Distance')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'cross_view_correlation.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: cross_view_correlation.png")
    
    return view_corr


# ============================================================================
# Analysis 2: Model Consistency Across Views
# ============================================================================
def analyze_model_consistency(data: dict, metric: str = 'SSIM'):
    """
    Which models are most consistent across different view types?
    High variance = specialized (good at some, bad at others)
    Low variance = generalist (similar performance across all)
    """
    
    results = []
    
    for model_type in ['Claude', 'DeepSeek', 'GPT']:
        for strategy in ['zero-shot', 'one-shot', 'few-shot', 'approach', 'agent']:
            scores = []
            for view, df in data['by_concern'].items():
                subset = df[(df['Base_Model'] == model_type) & (df['Strategy'] == strategy)]
                if not subset.empty and metric in subset.columns:
                    scores.append(subset[metric].mean())
            
            if len(scores) >= 2:
                results.append({
                    'Model': model_type,
                    'Strategy': strategy,
                    'Mean': np.mean(scores),
                    'Std': np.std(scores),
                    'CV': np.std(scores) / np.mean(scores) if np.mean(scores) > 0 else 0,
                    'Range': max(scores) - min(scores),
                    'N_Views': len(scores)
                })
    
    results_df = pd.DataFrame(results)
    
    if results_df.empty:
        print("No data for consistency analysis")
        return None
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot 1: Mean vs Std (consistency vs quality tradeoff)
    for model in ['Claude', 'DeepSeek', 'GPT']:
        subset = results_df[results_df['Model'] == model]
        if not subset.empty:
            axes[0].scatter(subset['Mean'], subset['Std'], s=100, label=model, alpha=0.7)
            for _, row in subset.iterrows():
                axes[0].annotate(row['Strategy'][:3], (row['Mean'], row['Std']), 
                               fontsize=8, alpha=0.7)
    
    axes[0].set_xlabel(f'Mean {metric} (Higher = Better Quality)', fontsize=11)
    axes[0].set_ylabel(f'Std Dev of {metric} (Lower = More Consistent)', fontsize=11)
    axes[0].set_title('Quality vs Consistency Tradeoff', fontweight='bold')
    axes[0].legend()
    
    # Ideal corner annotation
    axes[0].annotate('IDEAL\n(high quality,\nlow variance)', 
                    xy=(axes[0].get_xlim()[1]*0.95, axes[0].get_ylim()[0]*1.1),
                    fontsize=9, ha='right', style='italic', color='green')
    
    # Plot 2: Coefficient of Variation by Model
    cv_pivot = results_df.pivot_table(index='Strategy', columns='Model', values='CV')
    cv_pivot.plot(kind='bar', ax=axes[1], width=0.8)
    axes[1].set_title('Performance Variability Across Views\n(Lower = More Consistent)', fontweight='bold')
    axes[1].set_xlabel('Prompting Strategy')
    axes[1].set_ylabel('Coefficient of Variation')
    axes[1].legend(title='Model')
    axes[1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'model_consistency.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: model_consistency.png")
    
    return results_df


# ============================================================================
# Analysis 3: Notation Difficulty by Concern
# ============================================================================
def analyze_notation_by_concern(data: dict, combined_csv_path: Path = None):
    """
    Are certain notations harder for specific concerns?
    E.g., Is UML harder for deployment views but easier for control flow?
    """
    
    # This requires the full combined data with both notation and concern info
    # For now, show relative difficulty of notations
    
    if not data['by_notation']:
        print("No notation data available")
        return
    
    notation_stats = []
    for notation, df in data['by_notation'].items():
        for metric in ['SSIM', 'PSNR', 'RMSE']:
            if metric in df.columns:
                notation_stats.append({
                    'Notation': notation.replace('_', '+'),
                    'Metric': metric,
                    'Mean': df[metric].mean(),
                    'Std': df[metric].std(),
                    'N': len(df)
                })
    
    stats_df = pd.DataFrame(notation_stats)
    
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    
    for i, metric in enumerate(['SSIM', 'PSNR', 'RMSE']):
        subset = stats_df[stats_df['Metric'] == metric].sort_values('Mean', ascending=(metric=='RMSE'))
        if not subset.empty:
            colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(subset)))
            bars = axes[i].barh(subset['Notation'], subset['Mean'], color=colors)
            axes[i].errorbar(subset['Mean'], subset['Notation'], xerr=subset['Std'], 
                           fmt='none', color='black', capsize=3)
            axes[i].set_title(f'{metric} by Notation Type', fontweight='bold')
            axes[i].set_xlabel(f'Mean {metric}')
            
            # Add sample size annotations
            for j, (_, row) in enumerate(subset.iterrows()):
                axes[i].annotate(f'n={row["N"]}', xy=(row['Mean'], j), 
                               xytext=(5, 0), textcoords='offset points',
                               fontsize=8, va='center')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'notation_difficulty.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: notation_difficulty.png")


# ============================================================================
# Analysis 4: Scope (Granularity) Effect on Performance
# ============================================================================
def analyze_scope_effect(data: dict, metric: str = 'SSIM'):
    """
    How does architectural scope (part vs entire vs entire+) affect performance?
    """
    
    if not data['by_scope']:
        print("No scope data available")
        return
    
    scope_order = ['part', 'entire', 'entire+']
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Collect data
    scope_data = []
    for scope, df in data['by_scope'].items():
        for _, row in df.iterrows():
            scope_data.append({
                'Scope': scope,
                'Model': row['Base_Model'],
                'Strategy': row['Strategy'],
                metric: row.get(metric, np.nan)
            })
    
    scope_df = pd.DataFrame(scope_data)
    
    # Plot 1: Box plot by scope
    available_scopes = [s for s in scope_order if s in scope_df['Scope'].unique()]
    sns.boxplot(data=scope_df, x='Scope', y=metric, hue='Model', ax=axes[0],
               order=available_scopes)
    axes[0].set_title(f'{metric} Distribution by Architecture Scope', fontweight='bold')
    axes[0].legend(title='Model')
    
    # Plot 2: Trend lines showing scope effect per model
    for model in ['Claude', 'DeepSeek', 'GPT']:
        model_data = scope_df[scope_df['Model'] == model]
        if not model_data.empty:
            means = model_data.groupby('Scope')[metric].mean()
            means = means.reindex(available_scopes)
            axes[1].plot(range(len(available_scopes)), means.values, 'o-', 
                        label=model, linewidth=2, markersize=8)
    
    axes[1].set_xticks(range(len(available_scopes)))
    axes[1].set_xticklabels(available_scopes)
    axes[1].set_xlabel('Architecture Scope')
    axes[1].set_ylabel(f'Mean {metric}')
    axes[1].set_title(f'{metric} Trend by Scope', fontweight='bold')
    axes[1].legend(title='Model')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'scope_effect.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: scope_effect.png")


# ============================================================================
# Analysis 5: Quality Attribute Difficulty Patterns
# ============================================================================
def analyze_qa_patterns(data: dict, metric: str = 'SSIM'):
    """
    Which quality attributes are hardest to capture in architectural views?
    """
    
    if not data['by_qas']:
        print("No QA data available")
        return
    
    qa_performance = []
    for qa, df in data['by_qas'].items():
        qa_clean = qa.replace('_', ' ').title()
        for model in ['Claude', 'DeepSeek', 'GPT']:
            subset = df[df['Base_Model'] == model]
            if not subset.empty and metric in subset.columns:
                qa_performance.append({
                    'QA': qa_clean,
                    'Model': model,
                    'Mean': subset[metric].mean(),
                    'Std': subset[metric].std()
                })
    
    qa_df = pd.DataFrame(qa_performance)
    
    if qa_df.empty:
        print("No QA performance data")
        return
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot 1: Heatmap of QA x Model
    pivot = qa_df.pivot_table(index='QA', columns='Model', values='Mean')
    sns.heatmap(pivot, annot=True, fmt='.3f', cmap='YlGnBu', ax=axes[0])
    axes[0].set_title(f'{metric} by Quality Attribute', fontweight='bold')
    
    # Plot 2: Difficulty ranking (average across models)
    qa_avg = qa_df.groupby('QA')['Mean'].mean().sort_values()
    colors = plt.cm.RdYlGn(np.linspace(0.2, 0.8, len(qa_avg)))
    qa_avg.plot(kind='barh', ax=axes[1], color=colors)
    axes[1].set_title('Quality Attribute Difficulty\n(Lower SSIM = Harder)', fontweight='bold')
    axes[1].set_xlabel(f'Mean {metric}')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'qa_patterns.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: qa_patterns.png")


# ============================================================================
# Analysis 6: Statistical Significance Testing
# ============================================================================
def statistical_tests(data: dict, metric: str = 'SSIM'):
    """
    Perform statistical tests to validate observed differences.
    """
    from scipy.stats import mannwhitneyu, kruskal
    
    results = []
    
    # Test 1: Model differences
    model_scores = {model: [] for model in ['Claude', 'DeepSeek', 'GPT']}
    for view, df in data['by_concern'].items():
        for model in model_scores:
            subset = df[df['Base_Model'] == model]
            if not subset.empty and metric in subset.columns:
                model_scores[model].extend(subset[metric].dropna().tolist())
    
    # Kruskal-Wallis test (non-parametric ANOVA)
    valid_scores = [scores for scores in model_scores.values() if len(scores) > 0]
    if len(valid_scores) >= 2:
        stat, p_val = kruskal(*valid_scores)
        results.append({
            'Test': 'Kruskal-Wallis (Models)',
            'Statistic': stat,
            'p-value': p_val,
            'Significant': p_val < 0.05
        })
    
    # Test 2: Strategy differences
    strategy_scores = {s: [] for s in ['zero-shot', 'one-shot', 'few-shot', 'approach', 'agent']}
    for view, df in data['by_concern'].items():
        for strategy in strategy_scores:
            subset = df[df['Strategy'] == strategy]
            if not subset.empty and metric in subset.columns:
                strategy_scores[strategy].extend(subset[metric].dropna().tolist())
    
    valid_scores = [scores for scores in strategy_scores.values() if len(scores) > 0]
    if len(valid_scores) >= 2:
        stat, p_val = kruskal(*valid_scores)
        results.append({
            'Test': 'Kruskal-Wallis (Strategies)',
            'Statistic': stat,
            'p-value': p_val,
            'Significant': p_val < 0.05
        })
    
    # Pairwise comparisons
    models = list(model_scores.keys())
    for i, m1 in enumerate(models):
        for m2 in models[i+1:]:
            if model_scores[m1] and model_scores[m2]:
                stat, p_val = mannwhitneyu(model_scores[m1], model_scores[m2], 
                                          alternative='two-sided')
                results.append({
                    'Test': f'Mann-Whitney ({m1} vs {m2})',
                    'Statistic': stat,
                    'p-value': p_val,
                    'Significant': p_val < 0.05
                })
    
    results_df = pd.DataFrame(results)
    
    # Save as table image
    fig, ax = plt.subplots(figsize=(10, len(results_df)*0.5 + 1))
    ax.axis('off')
    
    table = ax.table(
        cellText=results_df.round(4).values,
        colLabels=results_df.columns,
        loc='center',
        cellLoc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.5)
    
    # Color significant results
    for i, row in results_df.iterrows():
        if row['Significant']:
            table[(i+1, 3)].set_facecolor('#90EE90')  # Light green
    
    ax.set_title('Statistical Significance Tests', fontweight='bold', fontsize=14, y=0.98)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'statistical_tests.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: statistical_tests.png")
    
    return results_df


# ============================================================================
# Main
# ============================================================================
def main(data_dir: str):
    """Run inter-view relationship analyses."""
    data_path = Path(data_dir)
    sns.color_palette("pastel")
    print(f"Loading data from: {data_path}")
    data = load_all_data(data_path)
    
    # Print summary
    for category, items in data.items():
        print(f"  {category}: {len(items)} files")
    
    print("\nRunning inter-view analyses...")
    
    # Run analyses
    if data['by_concern']:
        analyze_cross_view_correlation(data, 'SSIM')
        analyze_model_consistency(data, 'SSIM')
        statistical_tests(data, 'SSIM')
    
    if data['by_notation']:
        analyze_notation_by_concern(data)
    
    if data['by_scope']:
        analyze_scope_effect(data, 'SSIM')
    
    if data['by_qas']:
        analyze_qa_patterns(data, 'SSIM')
    
    print(f"\nOutputs saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Usage: python inter_view_analysis.py <data_directory>")