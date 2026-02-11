"""
Inter-View Relationship Analysis for Architectural View Generation
===================================================================

Key Research Questions:
1. Setting × View Interactions: Which experimental settings work best for which view types?
2. View Difficulty Patterns: Are certain views universally harder across all settings?
3. Model-Strategy Interactions: Does optimal strategy depend on the model?
4. Cross-Category Patterns: How do concerns, scopes, notations, QAs relate to each other?
5. Metric Consistency: Do automated metrics agree with LLM judgments?
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy.stats import spearmanr, kruskal, mannwhitneyu
from scipy.cluster.hierarchy import dendrogram, linkage
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-whitegrid')
OUTPUT_DIR = Path("./analysis_outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


# =============================================================================
# Data Loading
# =============================================================================
def load_all_csvs(data_dir: Path) -> dict:
    """Load all simple_table CSVs organized by category."""
    data = {
        'concern': {},
        'scope': {},
        'notation': {},
        'qas': {},
        'granularity': {}
    }
    
    for f in data_dir.glob("simple_table_*.csv"):
        name = f.stem.replace("simple_table_", "")
        df = pd.read_csv(f)
        
        # Parse experimental settings
        df['Model'] = df['Model'].str.lower()
        df['Base_Model'] = df['Model'].apply(lambda x: 
            'Claude' if 'claude' in x else 
            'DeepSeek' if 'deepseek' in x else 
            'GPT' if 'gpt' in x else 'Unknown')
        df['Strategy'] = df['Model'].apply(lambda x:
            'zero-shot' if 'zero' in x else
            'one-shot' if '1shot' in x else
            'few-shot' if 'few' in x else
            'agent' if 'agent' in x else
            'approach' if 'approach' in x else 'unknown')
        
        # Compute LLM composite scores
        for aspect in ['Clarity', 'Completeness', 'Consistency']:
            m, p, d = f'LLM_{aspect}_Rating_Meets', f'LLM_{aspect}_Rating_PartiallyMeets', f'LLM_{aspect}_Rating_DoesNotMeet'
            if all(c in df.columns for c in [m, p, d]):
                total = df[m] + df[p] + df[d]
                df[f'{aspect}_Score'] = (2*df[m] + df[p]) / (2 * total.replace(0, 1))
        
        score_cols = [c for c in df.columns if c.endswith('_Score')]
        if score_cols:
            df['LLM_Composite'] = df[score_cols].mean(axis=1)
        
        # Categorize
        if name.startswith("concern_"):
            data['concern'][name.replace("concern_", "")] = df
        elif name.startswith("scope_"):
            data['scope'][name.replace("scope_", "")] = df
        elif name.startswith("archnotation_"):
            data['notation'][name.replace("archnotation_", "")] = df
        elif name.startswith("qas_"):
            data['qas'][name.replace("qas_", "")] = df
        elif name in ['high', 'medium', 'low']:
            data['granularity'][name] = df
    
    return data


def build_master_matrix(data: dict, metric: str = 'SSIM') -> pd.DataFrame:
    """
    Build a matrix: rows = experimental settings, columns = view categories.
    This is the core data structure for inter-view analysis.
    """
    rows = []
    
    for category, views in data.items():
        for view_name, df in views.items():
            for _, row in df.iterrows():
                rows.append({
                    'Setting': row['Model'],
                    'Base_Model': row['Base_Model'],
                    'Strategy': row['Strategy'],
                    'Category': category,
                    'View': view_name,
                    'Category_View': f"{category}:{view_name}",
                    'SSIM': row.get('SSIM', np.nan),
                    'PSNR': row.get('PSNR', np.nan),
                    'RMSE': row.get('RMSE', np.nan),
                    'LLM_Composite': row.get('LLM_Composite', np.nan),
                    'Clarity_Score': row.get('Clarity_Score', np.nan),
                    'Completeness_Score': row.get('Completeness_Score', np.nan),
                    'Consistency_Score': row.get('Consistency_Score', np.nan),
                })
    
    return pd.DataFrame(rows)


# =============================================================================
# Analysis 1: Setting × View Interaction Heatmap
# =============================================================================
def plot_setting_view_heatmap(master: pd.DataFrame, metric: str = 'SSIM'):
    """
    Large heatmap: rows = 13 experimental settings, columns = all view types.
    Shows which settings excel at which views.
    """
    pivot = master.pivot_table(index='Setting', columns='Category_View', values=metric)
    
    # Sort settings logically
    setting_order = [
        'zeroshot_claude', 'zeroshot_gpt', 'zero_shot_deepseek',
        '1shot_claude', '1shot_gpt', '1shot_deepseek',
        'fewshot_claude', 'fewshot_gpt', 'fewshot_deepseek',
        'approach_claude', 'approach_gpt', 'approach_deepseek',
        'agent_claude'
    ]
    setting_order = [s for s in setting_order if s in pivot.index]
    pivot = pivot.reindex(setting_order)
    
    # Group columns by category
    col_order = sorted(pivot.columns, key=lambda x: (x.split(':')[0], x.split(':')[1]))
    pivot = pivot[col_order]
    
    fig, ax = plt.subplots(figsize=(20, 10))
    sns.heatmap(pivot, annot=True, fmt='.3f', cmap='RdYlGn', center=pivot.values.mean(),
                ax=ax, cbar_kws={'label': metric}, annot_kws={'size': 7})
    
    ax.set_title(f'Experimental Setting × View Type Performance ({metric})\n'
                 f'Rows: 13 Settings | Columns: View Types (grouped by category)', 
                 fontsize=14, fontweight='bold')
    ax.set_xlabel('View Type (Category:Name)', fontsize=11)
    ax.set_ylabel('Experimental Setting', fontsize=11)
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.yticks(fontsize=9)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f'heatmap_setting_x_view_{metric}.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: heatmap_setting_x_view_{metric}.png")


# =============================================================================
# Analysis 2: View Difficulty Ranking (Consistent Across Settings?)
# =============================================================================
def plot_view_difficulty_analysis(master: pd.DataFrame, metric: str = 'SSIM'):
    """
    Are some views universally harder? Or does difficulty depend on setting?
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 14))
    
    # Panel 1: Mean difficulty per view (averaged across all settings)
    view_means = master.groupby('Category_View')[metric].agg(['mean', 'std']).sort_values('mean')
    colors = plt.cm.RdYlGn(np.linspace(0.2, 0.8, len(view_means)))
    
    ax = axes[0, 0]
    bars = ax.barh(range(len(view_means)), view_means['mean'], color=colors, xerr=view_means['std'], capsize=3)
    ax.set_yticks(range(len(view_means)))
    ax.set_yticklabels(view_means.index, fontsize=8)
    ax.set_xlabel(f'Mean {metric} (± std across settings)')
    ax.set_title('View Difficulty Ranking\n(Averaged across all 13 settings)', fontweight='bold')
    ax.axvline(view_means['mean'].mean(), color='red', linestyle='--', label='Overall mean')
    ax.legend()
    
    # Panel 2: Difficulty variance - which views have inconsistent performance?
    ax = axes[0, 1]
    view_cv = (view_means['std'] / view_means['mean']).sort_values(ascending=False)
    ax.barh(range(len(view_cv)), view_cv.values, color='steelblue')
    ax.set_yticks(range(len(view_cv)))
    ax.set_yticklabels(view_cv.index, fontsize=8)
    ax.set_xlabel('Coefficient of Variation')
    ax.set_title('View Performance Variability\n(High = inconsistent across settings)', fontweight='bold')
    
    # Panel 3: Per-category breakdown
    ax = axes[1, 0]
    category_means = master.groupby(['Category', 'View'])[metric].mean().unstack(level=0)
    if not category_means.empty:
        category_means.plot(kind='bar', ax=ax, width=0.8)
        ax.set_xlabel('View')
        ax.set_ylabel(f'Mean {metric}')
        ax.set_title('Performance by Category', fontweight='bold')
        ax.legend(title='Category', bbox_to_anchor=(1.02, 1))
        ax.tick_params(axis='x', rotation=45)
    
    # Panel 4: Hardest/Easiest views per model
    ax = axes[1, 1]
    model_view_perf = master.groupby(['Base_Model', 'Category_View'])[metric].mean().unstack()
    
    summary_data = []
    for model in ['Claude', 'DeepSeek', 'GPT']:
        if model in model_view_perf.index:
            row = model_view_perf.loc[model]
            summary_data.append({
                'Model': model,
                'Best View': row.idxmax(),
                'Best Score': row.max(),
                'Worst View': row.idxmin(),
                'Worst Score': row.min(),
                'Range': row.max() - row.min()
            })
    
    summary_df = pd.DataFrame(summary_data)
    ax.axis('off')
    table = ax.table(cellText=summary_df.round(3).values, colLabels=summary_df.columns,
                     loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.8)
    ax.set_title('Best/Worst Views per Model', fontweight='bold', y=0.95)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f'view_difficulty_analysis_{metric}.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: view_difficulty_analysis_{metric}.png")


# =============================================================================
# Analysis 3: Model × Strategy Interaction
# =============================================================================
def plot_model_strategy_interaction(master: pd.DataFrame, metric: str = 'SSIM'):
    """
    Does the best strategy depend on which model you use?
    """
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # Panel 1: Overall interaction heatmap
    ax = axes[0]
    interaction = master.groupby(['Base_Model', 'Strategy'])[metric].mean().unstack()
    sns.heatmap(interaction, annot=True, fmt='.3f', cmap='YlGnBu', ax=ax)
    ax.set_title(f'Model × Strategy Interaction\n(Mean {metric} across all views)', fontweight='bold')
    
    # Panel 2: Best strategy per model per category
    ax = axes[1]
    best_strategies = []
    for category in master['Category'].unique():
        cat_data = master[master['Category'] == category]
        for model in ['Claude', 'DeepSeek', 'GPT']:
            model_data = cat_data[cat_data['Base_Model'] == model]
            if not model_data.empty:
                best = model_data.groupby('Strategy')[metric].mean().idxmax()
                best_strategies.append({
                    'Category': category,
                    'Model': model,
                    'Best_Strategy': best
                })
    
    best_df = pd.DataFrame(best_strategies)
    if not best_df.empty:
        pivot = best_df.pivot(index='Category', columns='Model', values='Best_Strategy')
        # Convert to numeric for heatmap
        strategy_map = {'zero-shot': 0, 'one-shot': 1, 'few-shot': 2, 'approach': 3, 'agent': 4}
        pivot_num = pivot.applymap(lambda x: strategy_map.get(x, -1) if pd.notna(x) else -1)
        
        sns.heatmap(pivot_num, annot=pivot.values, fmt='', cmap='tab10', ax=ax, 
                    cbar=False, vmin=-0.5, vmax=4.5)
        ax.set_title('Best Strategy per Model per Category', fontweight='bold')
    
    # Panel 3: Strategy ranking consistency
    ax = axes[2]
    strategy_ranks = master.groupby(['Category', 'Strategy'])[metric].mean().unstack()
    strategy_ranks = strategy_ranks.rank(axis=1, ascending=False)
    
    mean_ranks = strategy_ranks.mean()
    std_ranks = strategy_ranks.std()
    
    x = range(len(mean_ranks))
    ax.bar(x, mean_ranks.values, yerr=std_ranks.values, capsize=5, color='coral')
    ax.set_xticks(x)
    ax.set_xticklabels(mean_ranks.index, rotation=45, ha='right')
    ax.set_ylabel('Mean Rank (lower = better)')
    ax.set_title('Strategy Ranking Consistency\n(Error bars = variance across categories)', fontweight='bold')
    ax.invert_yaxis()
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f'model_strategy_interaction_{metric}.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: model_strategy_interaction_{metric}.png")


# =============================================================================
# Analysis 4: Cross-Category Correlation
# =============================================================================
def plot_cross_category_correlation(master: pd.DataFrame, metric: str = 'SSIM'):
    """
    Do settings that perform well on concerns also perform well on scopes/notations/QAs?
    """
    # Build setting-level averages per category
    category_perf = master.groupby(['Setting', 'Category'])[metric].mean().unstack()
    
    if category_perf.shape[1] < 2:
        print("Not enough categories for correlation analysis")
        return
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Panel 1: Category correlation
    ax = axes[0]
    corr = category_perf.corr(method='spearman')
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdBu_r', center=0, vmin=-1, vmax=1, ax=ax)
    ax.set_title(f'Cross-Category Performance Correlation\n(Spearman ρ, based on {metric})', fontweight='bold')
    
    # Panel 2: Scatter matrix for top categories
    ax = axes[1]
    top_cats = category_perf.columns[:4]  # First 4 categories
    if len(top_cats) >= 2:
        scatter_data = category_perf[top_cats]
        pd.plotting.scatter_matrix(scatter_data, ax=None, figsize=(8, 8), diagonal='hist')
        plt.suptitle('Category Performance Scatter Matrix', fontweight='bold')
        plt.savefig(OUTPUT_DIR / f'scatter_matrix_categories_{metric}.png', dpi=150, bbox_inches='tight')
        plt.close()
        print(f"Saved: scatter_matrix_categories_{metric}.png")
    
    # Just save the correlation plot
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdBu_r', center=0, vmin=-1, vmax=1, ax=ax)
    ax.set_title(f'Cross-Category Performance Correlation\n(Spearman ρ, based on {metric})', fontweight='bold')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f'cross_category_correlation_{metric}.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: cross_category_correlation_{metric}.png")


# =============================================================================
# Analysis 5: Metric Agreement Analysis
# =============================================================================
def plot_metric_agreement(master: pd.DataFrame):
    """
    Do SSIM, PSNR agree with LLM judgments? Does this vary by view type?
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    # Panel 1: Overall metric correlation
    ax = axes[0, 0]
    metrics = ['SSIM', 'PSNR', 'RMSE', 'LLM_Composite', 'Clarity_Score', 'Completeness_Score', 'Consistency_Score']
    available = [m for m in metrics if m in master.columns and master[m].notna().sum() > 10]
    
    if len(available) >= 2:
        corr = master[available].corr(method='spearman')
        sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdBu_r', center=0, ax=ax)
        ax.set_title('Metric Correlation (All Data)', fontweight='bold')
    
    # Panel 2: SSIM vs LLM by category
    ax = axes[0, 1]
    if 'LLM_Composite' in master.columns:
        for cat in master['Category'].unique():
            cat_data = master[master['Category'] == cat]
            ax.scatter(cat_data['SSIM'], cat_data['LLM_Composite'], label=cat, alpha=0.6, s=50)
        ax.set_xlabel('SSIM')
        ax.set_ylabel('LLM Composite Score')
        ax.set_title('SSIM vs LLM Score by Category', fontweight='bold')
        ax.legend(title='Category', bbox_to_anchor=(1.02, 1))
    
    # Panel 3: Correlation by category
    ax = axes[1, 0]
    if 'LLM_Composite' in master.columns:
        cat_corrs = []
        for cat in master['Category'].unique():
            cat_data = master[master['Category'] == cat].dropna(subset=['SSIM', 'LLM_Composite'])
            if len(cat_data) >= 5:
                r, p = spearmanr(cat_data['SSIM'], cat_data['LLM_Composite'])
                cat_corrs.append({'Category': cat, 'Correlation': r, 'p-value': p, 'N': len(cat_data)})
        
        if cat_corrs:
            corr_df = pd.DataFrame(cat_corrs).sort_values('Correlation')
            colors = ['green' if p < 0.05 else 'gray' for p in corr_df['p-value']]
            ax.barh(corr_df['Category'], corr_df['Correlation'], color=colors)
            ax.axvline(0, color='black', linestyle='-', linewidth=0.5)
            ax.set_xlabel('Spearman Correlation (SSIM vs LLM)')
            ax.set_title('Metric Agreement by Category\n(Green = significant p<0.05)', fontweight='bold')
    
    # Panel 4: LLM sub-scores breakdown
    ax = axes[1, 1]
    llm_scores = ['Clarity_Score', 'Completeness_Score', 'Consistency_Score']
    available_llm = [s for s in llm_scores if s in master.columns]
    
    if available_llm:
        llm_by_cat = master.groupby('Category')[available_llm].mean()
        llm_by_cat.plot(kind='bar', ax=ax, width=0.8)
        ax.set_xlabel('Category')
        ax.set_ylabel('Score (0-1)')
        ax.set_title('LLM Sub-Scores by Category', fontweight='bold')
        ax.legend(title='Metric')
        ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'metric_agreement_analysis.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: metric_agreement_analysis.png")


# =============================================================================
# Analysis 6: View Clustering Based on Performance Patterns
# =============================================================================
def plot_view_clustering(master: pd.DataFrame, metric: str = 'SSIM'):
    """
    Cluster views based on which settings perform well on them.
    Views that cluster together have similar "difficulty profiles".
    """
    # Build view × setting matrix
    pivot = master.pivot_table(index='Category_View', columns='Setting', values=metric)
    pivot = pivot.dropna(thresh=pivot.shape[1]*0.5)  # Keep views with enough data
    
    if pivot.shape[0] < 3:
        print("Not enough views for clustering")
        return
    
    # Fill remaining NaN with column means
    pivot = pivot.fillna(pivot.mean())
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    
    # Panel 1: Hierarchical clustering dendrogram
    ax = axes[0]
    Z = linkage(pivot.values, method='ward')
    dendrogram(Z, labels=pivot.index.tolist(), ax=ax, leaf_rotation=90, leaf_font_size=8)
    ax.set_title('View Clustering by Performance Profile\n(Views that cluster together behave similarly)', 
                 fontweight='bold')
    ax.set_ylabel('Distance')
    
    # Panel 2: Clustermap
    g = sns.clustermap(pivot, method='ward', cmap='RdYlGn', figsize=(14, 10),
                       row_cluster=True, col_cluster=True,
                       cbar_kws={'label': metric})
    g.fig.suptitle(f'Clustered Heatmap: Views × Settings ({metric})', fontweight='bold', y=1.02)
    g.savefig(OUTPUT_DIR / f'clustermap_views_settings_{metric}.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: clustermap_views_settings_{metric}.png")
    
    # Save dendrogram separately
    fig, ax = plt.subplots(figsize=(14, 8))
    dendrogram(Z, labels=pivot.index.tolist(), ax=ax, leaf_rotation=45, leaf_font_size=9)
    ax.set_title('View Clustering Dendrogram', fontweight='bold')
    ax.set_ylabel('Distance')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f'dendrogram_views_{metric}.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: dendrogram_views_{metric}.png")


# =============================================================================
# Analysis 7: Statistical Summary Table
# =============================================================================
def generate_statistical_summary(master: pd.DataFrame, metric: str = 'SSIM'):
    """
    Generate key statistics and significance tests.
    """
    results = []
    
    # Test 1: Do models differ significantly?
    model_groups = [master[master['Base_Model'] == m][metric].dropna() for m in ['Claude', 'DeepSeek', 'GPT']]
    model_groups = [g for g in model_groups if len(g) > 0]
    if len(model_groups) >= 2:
        stat, p = kruskal(*model_groups)
        results.append({'Test': 'Kruskal-Wallis: Models', 'Statistic': f'{stat:.2f}', 'p-value': f'{p:.4f}', 
                       'Significant': 'Yes' if p < 0.05 else 'No'})
    
    # Test 2: Do strategies differ significantly?
    strategies = ['zero-shot', 'one-shot', 'few-shot', 'approach', 'agent']
    strat_groups = [master[master['Strategy'] == s][metric].dropna() for s in strategies]
    strat_groups = [g for g in strat_groups if len(g) > 0]
    if len(strat_groups) >= 2:
        stat, p = kruskal(*strat_groups)
        results.append({'Test': 'Kruskal-Wallis: Strategies', 'Statistic': f'{stat:.2f}', 'p-value': f'{p:.4f}',
                       'Significant': 'Yes' if p < 0.05 else 'No'})
    
    # Test 3: Do categories differ?
    cat_groups = [master[master['Category'] == c][metric].dropna() for c in master['Category'].unique()]
    cat_groups = [g for g in cat_groups if len(g) > 0]
    if len(cat_groups) >= 2:
        stat, p = kruskal(*cat_groups)
        results.append({'Test': 'Kruskal-Wallis: Categories', 'Statistic': f'{stat:.2f}', 'p-value': f'{p:.4f}',
                       'Significant': 'Yes' if p < 0.05 else 'No'})
    
    # Pairwise model comparisons
    for m1, m2 in [('Claude', 'GPT'), ('Claude', 'DeepSeek'), ('GPT', 'DeepSeek')]:
        g1 = master[master['Base_Model'] == m1][metric].dropna()
        g2 = master[master['Base_Model'] == m2][metric].dropna()
        if len(g1) > 0 and len(g2) > 0:
            stat, p = mannwhitneyu(g1, g2, alternative='two-sided')
            results.append({'Test': f'Mann-Whitney: {m1} vs {m2}', 'Statistic': f'{stat:.0f}', 
                           'p-value': f'{p:.4f}', 'Significant': 'Yes' if p < 0.05 else 'No'})
    
    results_df = pd.DataFrame(results)
    
    # Save as image
    fig, ax = plt.subplots(figsize=(10, len(results_df)*0.6 + 1.5))
    ax.axis('off')
    
    table = ax.table(cellText=results_df.values, colLabels=results_df.columns,
                     loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.3, 1.8)
    
    # Color significant rows
    for i, row in results_df.iterrows():
        if row['Significant'] == 'Yes':
            for j in range(len(results_df.columns)):
                table[(i+1, j)].set_facecolor('#90EE90')
    
    ax.set_title(f'Statistical Significance Tests ({metric})', fontweight='bold', fontsize=14, y=0.95)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f'statistical_summary_{metric}.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: statistical_summary_{metric}.png")
    
    # Also save as CSV
    results_df.to_csv(OUTPUT_DIR / f'statistical_summary_{metric}.csv', index=False)
    print(f"Saved: statistical_summary_{metric}.csv")
    
    return results_df


# =============================================================================
# Analysis 8: Key Findings Summary
# =============================================================================
def generate_key_findings(master: pd.DataFrame, metric: str = 'SSIM'):
    """
    Auto-generate key findings for the paper.
    """
    findings = []
    
    # Best overall setting
    best_setting = master.groupby('Setting')[metric].mean().idxmax()
    best_score = master.groupby('Setting')[metric].mean().max()
    findings.append(f"1. BEST OVERALL SETTING: {best_setting} (mean {metric}={best_score:.4f})")
    
    # Best model
    best_model = master.groupby('Base_Model')[metric].mean().idxmax()
    findings.append(f"2. BEST MODEL: {best_model}")
    
    # Best strategy
    best_strategy = master.groupby('Strategy')[metric].mean().idxmax()
    findings.append(f"3. BEST STRATEGY: {best_strategy}")
    
    # Hardest view category
    hardest_cat = master.groupby('Category')[metric].mean().idxmin()
    easiest_cat = master.groupby('Category')[metric].mean().idxmax()
    findings.append(f"4. HARDEST CATEGORY: {hardest_cat}")
    findings.append(f"5. EASIEST CATEGORY: {easiest_cat}")
    
    # Hardest specific view
    hardest_view = master.groupby('Category_View')[metric].mean().idxmin()
    easiest_view = master.groupby('Category_View')[metric].mean().idxmax()
    findings.append(f"6. HARDEST VIEW: {hardest_view}")
    findings.append(f"7. EASIEST VIEW: {easiest_view}")
    
    # Most consistent model
    model_stds = master.groupby('Base_Model')[metric].std()
    most_consistent = model_stds.idxmin()
    findings.append(f"8. MOST CONSISTENT MODEL: {most_consistent} (lowest variance across views)")
    
    # LLM vs Image metric correlation
    if 'LLM_Composite' in master.columns:
        valid = master.dropna(subset=[metric, 'LLM_Composite'])
        if len(valid) > 10:
            r, p = spearmanr(valid[metric], valid['LLM_Composite'])
            findings.append(f"9. METRIC AGREEMENT: {metric} vs LLM: ρ={r:.3f} (p={p:.4f})")
    
    # Print and save
    print("\n" + "="*60)
    print("KEY FINDINGS")
    print("="*60)
    for f in findings:
        print(f)
    
    with open(OUTPUT_DIR / 'key_findings.txt', 'w') as f:
        f.write("KEY FINDINGS\n")
        f.write("="*60 + "\n\n")
        for finding in findings:
            f.write(finding + "\n")
    
    print(f"\nSaved: key_findings.txt")
    
    return findings


# =============================================================================
# Main
# =============================================================================
def main(data_dir: str):
    """Run all analyses."""
    data_path = Path(data_dir)
    
    print(f"Loading data from: {data_path}")
    data = load_all_csvs(data_path)
    
    # Print summary
    total_views = sum(len(v) for v in data.values())
    print(f"\nLoaded data:")
    for category, views in data.items():
        if views:
            print(f"  {category}: {len(views)} view types")
            for name in views.keys():
                print(f"    - {name}")
    
    print(f"\nBuilding master matrix...")
    master = build_master_matrix(data)
    print(f"Master matrix: {len(master)} rows (settings × views)")
    print(f"Unique settings: {master['Setting'].nunique()}")
    print(f"Unique views: {master['Category_View'].nunique()}")
    
    print("\n" + "="*60)
    print("GENERATING ANALYSES")
    print("="*60)
    
    # Run all analyses for both SSIM and LLM_Composite
    for metric in ['SSIM', 'LLM_Composite']:
        if metric in master.columns and master[metric].notna().sum() > 0:
            print(f"\n--- Analyses for {metric} ---")
            plot_setting_view_heatmap(master, metric)
            plot_view_difficulty_analysis(master, metric)
            plot_model_strategy_interaction(master, metric)
            plot_cross_category_correlation(master, metric)
            plot_view_clustering(master, metric)
            generate_statistical_summary(master, metric)
    
    # Metric agreement (only once)
    plot_metric_agreement(master)
    
    # Key findings
    generate_key_findings(master, 'SSIM')
    
    print(f"\n" + "="*60)
    print(f"ALL OUTPUTS SAVED TO: {OUTPUT_DIR.absolute()}")
    print("="*60)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Usage: python proper_analysis.py <data_directory>")
        print("\nExample: python proper_analysis.py .")