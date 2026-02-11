"""
Focused Analysis: Few-Shot vs Agent vs Approach
================================================

Experimental Setup:
- Few-shot: Claude, DeepSeek, GPT (standard prompting with examples)
- Agent: Claude only (agentic approach - single model)
- Approach: Claude, DeepSeek, GPT (agentic approach - all models)

Both "agent" and "approach" are agentic methods. Key difference:
- "agent" = agentic with Claude only
- "approach" = agentic with all 3 LLMs

Key Questions:
1. Few-shot vs Agentic: Which paradigm works better?
2. Within agentic: Does "agent" (Claude-only) beat "approach" (multi-model)?
3. Model effects: How do Claude/DeepSeek/GPT compare within each strategy?
4. View-specific patterns: Which strategy excels at which view types?
5. Cost-benefit: Is the agentic overhead worth it?
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy.stats import kruskal, mannwhitneyu, wilcoxon, friedmanchisquare
from scipy.stats import spearmanr
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-whitegrid')
OUTPUT_DIR = Path("./analysis_fewshot_agent_approach")
OUTPUT_DIR.mkdir(exist_ok=True)

# Colors for the three strategies
STRATEGY_COLORS = {
    'few-shot': '#3498DB',   # Blue - standard prompting
    'agent': '#E74C3C',      # Red - agentic (Claude only)
    'approach': '#2ECC71'    # Green - agentic (all models)
}

MODEL_COLORS = {
    'Claude': '#9B59B6',     # Purple
    'DeepSeek': '#F39C12',   # Orange
    'GPT': '#1ABC9C'         # Teal
}

# Group strategies by paradigm
PARADIGM_GROUPS = {
    'standard': ['few-shot'],
    'agentic': ['agent', 'approach']
}


def load_and_filter_data(data_dir: Path) -> pd.DataFrame:
    """Load data and filter to only few-shot, agent, approach."""
    rows = []
    
    for f in data_dir.glob("simple_table_*.csv"):
        name = f.stem.replace("simple_table_", "")
        df = pd.read_csv(f)
        
        # Determine category
        if name.startswith("concern_"):
            category, view = 'concern', name.replace("concern_", "")
        elif name.startswith("scope_"):
            category, view = 'scope', name.replace("scope_", "")
        elif name.startswith("archnotation_"):
            category, view = 'notation', name.replace("archnotation_", "")
        elif name.startswith("qas_"):
            category, view = 'qas', name.replace("qas_", "")
        elif name in ['high', 'medium', 'low']:
            category, view = 'granularity', name
        else:
            continue
        
        for _, row in df.iterrows():
            model_name = row['Model'].lower()
            
            # Parse strategy
            if 'few' in model_name:
                strategy = 'few-shot'
            elif 'agent' in model_name:
                strategy = 'agent'
            elif 'approach' in model_name:
                strategy = 'approach'
            else:
                continue  # Skip zero-shot and one-shot
            
            # Parse base model
            if 'claude' in model_name:
                base_model = 'Claude'
            elif 'deepseek' in model_name:
                base_model = 'DeepSeek'
            elif 'gpt' in model_name:
                base_model = 'GPT'
            else:
                continue
            
            # Compute LLM scores
            llm_composite = np.nan
            scores = {}
            for aspect in ['Clarity', 'Completeness', 'Consistency']:
                m = f'LLM_{aspect}_Rating_Meets'
                p = f'LLM_{aspect}_Rating_PartiallyMeets'
                d = f'LLM_{aspect}_Rating_DoesNotMeet'
                if all(c in row.index for c in [m, p, d]):
                    total = row[m] + row[p] + row[d]
                    if total > 0:
                        scores[aspect] = (2*row[m] + row[p]) / (2 * total)
            
            if scores:
                llm_composite = np.mean(list(scores.values()))
            
            rows.append({
                'Setting': row['Model'].lower(),
                'Strategy': strategy,
                'Base_Model': base_model,
                'Category': category,
                'View': view,
                'Category_View': f"{category}:{view}",
                'SSIM': row.get('SSIM', np.nan),
                'PSNR': row.get('PSNR', np.nan),
                'RMSE': row.get('RMSE', np.nan),
                'LLM_Composite': llm_composite,
                'Clarity': scores.get('Clarity', np.nan),
                'Completeness': scores.get('Completeness', np.nan),
                'Consistency': scores.get('Consistency', np.nan),
            })
    
    return pd.DataFrame(rows)


# =============================================================================
# Analysis 1: Overall Strategy Comparison
# =============================================================================
def plot_overall_comparison(df: pd.DataFrame):
    """Direct comparison of the three strategies across all metrics."""
    
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    
    metrics = ['SSIM', 'PSNR', 'LLM_Composite', 'Clarity', 'Completeness', 'Consistency']
    
    for ax, metric in zip(axes.flat, metrics):
        if metric not in df.columns or df[metric].isna().all():
            ax.set_visible(False)
            continue
        
        # Box plot
        data_to_plot = [df[df['Strategy'] == s][metric].dropna() for s in ['few-shot', 'agent', 'approach']]
        bp = ax.boxplot(data_to_plot, labels=['Few-Shot', 'Agent', 'Approach'], patch_artist=True)
        
        colors = [STRATEGY_COLORS['few-shot'], STRATEGY_COLORS['agent'], STRATEGY_COLORS['approach']]
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        # Add mean markers
        means = [d.mean() for d in data_to_plot]
        ax.scatter([1, 2, 3], means, color='black', marker='D', s=50, zorder=5, label='Mean')
        
        # Add significance annotations
        strategies = ['few-shot', 'agent', 'approach']
        y_max = max([d.max() for d in data_to_plot if len(d) > 0])
        y_step = (y_max - min([d.min() for d in data_to_plot if len(d) > 0])) * 0.1
        
        for i, (s1, s2) in enumerate([(0, 1), (0, 2), (1, 2)]):
            if len(data_to_plot[s1]) > 0 and len(data_to_plot[s2]) > 0:
                stat, p = mannwhitneyu(data_to_plot[s1], data_to_plot[s2], alternative='two-sided')
                if p < 0.05:
                    y = y_max + y_step * (i + 1)
                    ax.plot([s1+1, s2+1], [y, y], 'k-', linewidth=1)
                    sig_text = '***' if p < 0.001 else '**' if p < 0.01 else '*'
                    ax.text((s1 + s2 + 2) / 2, y, sig_text, ha='center', va='bottom', fontsize=10)
        
        ax.set_title(f'{metric}', fontweight='bold', fontsize=12)
        ax.set_ylabel(metric)
    
    plt.suptitle('Overall Strategy Comparison: Few-Shot vs Agent vs Approach\n'
                 '(* p<0.05, ** p<0.01, *** p<0.001)', 
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'overall_comparison_boxplots.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: overall_comparison_boxplots.png")


# =============================================================================
# Analysis 2: Strategy Comparison by Model
# =============================================================================
def plot_strategy_by_model(df: pd.DataFrame, metric: str = 'SSIM'):
    """Does the best strategy depend on which model you use?"""
    
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    
    strategies = ['few-shot', 'agent', 'approach']
    models = ['Claude', 'DeepSeek', 'GPT']
    
    # Panel 1: Grouped bar chart
    ax = axes[0]
    x = np.arange(len(models))
    width = 0.25
    
    for i, strategy in enumerate(strategies):
        means = []
        stds = []
        for model in models:
            data = df[(df['Strategy'] == strategy) & (df['Base_Model'] == model)][metric]
            means.append(data.mean() if len(data) > 0 else 0)
            stds.append(data.std() if len(data) > 0 else 0)
        
        bars = ax.bar(x + i*width, means, width, label=strategy, 
                     color=STRATEGY_COLORS[strategy], yerr=stds, capsize=3)
    
    ax.set_xlabel('Model')
    ax.set_ylabel(f'Mean {metric}')
    ax.set_title(f'{metric} by Model and Strategy', fontweight='bold')
    ax.set_xticks(x + width)
    ax.set_xticklabels(models)
    ax.legend(title='Strategy')
    
    # Panel 2: Heatmap of differences
    ax = axes[1]
    pivot = df.groupby(['Base_Model', 'Strategy'])[metric].mean().unstack()
    pivot = pivot[strategies]  # Ensure order
    
    sns.heatmap(pivot, annot=True, fmt='.4f', cmap='RdYlGn', ax=ax, 
                cbar_kws={'label': metric})
    ax.set_title(f'Mean {metric}: Model × Strategy', fontweight='bold')
    
    # Panel 3: Winner per model
    ax = axes[2]
    winner_data = []
    for model in models:
        model_df = df[df['Base_Model'] == model]
        strategy_means = model_df.groupby('Strategy')[metric].mean()
        
        if len(strategy_means) > 0:
            best = strategy_means.idxmax()
            best_score = strategy_means.max()
            second_best = strategy_means.drop(best).idxmax() if len(strategy_means) > 1 else None
            gap = best_score - strategy_means.drop(best).max() if len(strategy_means) > 1 else 0
            
            winner_data.append({
                'Model': model,
                'Best Strategy': best,
                f'Best {metric}': f'{best_score:.4f}',
                'Runner-up': second_best,
                'Gap': f'{gap:.4f}'
            })
    
    winner_df = pd.DataFrame(winner_data)
    ax.axis('off')
    table = ax.table(cellText=winner_df.values, colLabels=winner_df.columns,
                     loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 2)
    ax.set_title('Best Strategy per Model', fontweight='bold', y=0.8)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f'strategy_by_model_{metric}.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: strategy_by_model_{metric}.png")


# =============================================================================
# Analysis 3: Strategy Comparison by View Category
# =============================================================================
def plot_strategy_by_category(df: pd.DataFrame, metric: str = 'SSIM'):
    """Which strategy works best for each view category?"""
    
    categories = df['Category'].unique()
    strategies = ['few-shot', 'agent', 'approach']
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    # Panel 1: Heatmap
    ax = axes[0, 0]
    pivot = df.groupby(['Category', 'Strategy'])[metric].mean().unstack()
    pivot = pivot[strategies]
    
    sns.heatmap(pivot, annot=True, fmt='.4f', cmap='RdYlGn', ax=ax)
    ax.set_title(f'Mean {metric} by Category and Strategy', fontweight='bold')
    
    # Panel 2: Best strategy per category
    ax = axes[0, 1]
    best_per_cat = pivot.idxmax(axis=1)
    best_counts = best_per_cat.value_counts()
    
    colors = [STRATEGY_COLORS[s] for s in best_counts.index]
    bars = ax.bar(best_counts.index, best_counts.values, color=colors)
    ax.set_ylabel('Number of Categories Won')
    ax.set_title('Which Strategy Wins Most Categories?', fontweight='bold')
    
    for bar, count in zip(bars, best_counts.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
               str(count), ha='center', va='bottom', fontweight='bold')
    
    # Panel 3: Detailed category breakdown
    ax = axes[1, 0]
    x = np.arange(len(categories))
    width = 0.25
    
    for i, strategy in enumerate(strategies):
        means = [pivot.loc[cat, strategy] if cat in pivot.index else 0 for cat in categories]
        ax.bar(x + i*width, means, width, label=strategy, color=STRATEGY_COLORS[strategy])
    
    ax.set_xticks(x + width)
    ax.set_xticklabels(categories, rotation=45, ha='right')
    ax.set_ylabel(f'Mean {metric}')
    ax.set_title(f'{metric} by Category', fontweight='bold')
    ax.legend()
    
    # Panel 4: Strategy advantage (difference from mean)
    ax = axes[1, 1]
    overall_mean = df[metric].mean()
    
    advantage_data = []
    for strategy in strategies:
        for cat in categories:
            val = pivot.loc[cat, strategy] if cat in pivot.index else np.nan
            if not np.isnan(val):
                advantage_data.append({
                    'Category': cat,
                    'Strategy': strategy,
                    'Advantage': val - overall_mean
                })
    
    adv_df = pd.DataFrame(advantage_data)
    adv_pivot = adv_df.pivot(index='Category', columns='Strategy', values='Advantage')
    
    sns.heatmap(adv_pivot, annot=True, fmt='.4f', cmap='RdBu_r', center=0, ax=ax)
    ax.set_title(f'Strategy Advantage vs Overall Mean\n(Positive = Better than average)', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f'strategy_by_category_{metric}.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: strategy_by_category_{metric}.png")


# =============================================================================
# Analysis 4: Strategy Comparison by Specific View
# =============================================================================
def plot_strategy_by_view(df: pd.DataFrame, metric: str = 'SSIM'):
    """Detailed view-level analysis: where does each strategy shine?"""
    
    strategies = ['few-shot', 'agent', 'approach']
    
    # Compute mean per view per strategy
    view_strategy = df.groupby(['Category_View', 'Strategy'])[metric].mean().unstack()
    view_strategy = view_strategy[strategies]
    
    # Determine winner per view
    view_strategy['Winner'] = view_strategy.idxmax(axis=1)
    view_strategy['Best_Score'] = view_strategy[strategies].max(axis=1)
    view_strategy['Margin'] = view_strategy[strategies].max(axis=1) - view_strategy[strategies].median(axis=1)
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 14))
    
    # Panel 1: Large heatmap of all views
    ax = axes[0, 0]
    plot_data = view_strategy[strategies].sort_values(strategies[0], ascending=False)
    
    if len(plot_data) > 20:
        # Show top 20 most variable views
        variance = plot_data.var(axis=1)
        top_views = variance.nlargest(20).index
        plot_data = plot_data.loc[top_views]
    
    sns.heatmap(plot_data, annot=True, fmt='.3f', cmap='RdYlGn', ax=ax, 
                annot_kws={'size': 8})
    ax.set_title(f'{metric} by View and Strategy\n(Top 20 most variable views)', fontweight='bold')
    ax.set_xlabel('Strategy')
    ax.set_ylabel('View')
    
    # Panel 2: Winner distribution
    ax = axes[0, 1]
    winner_counts = view_strategy['Winner'].value_counts()
    colors = [STRATEGY_COLORS[s] for s in winner_counts.index]
    
    wedges, texts, autotexts = ax.pie(winner_counts.values, labels=winner_counts.index, 
                                       autopct='%1.1f%%', colors=colors, startangle=90)
    ax.set_title('Which Strategy Wins Most Views?', fontweight='bold')
    
    # Panel 3: Views where each strategy dominates
    ax = axes[1, 0]
    
    # Find views where one strategy clearly wins (margin > threshold)
    margin_threshold = 0.01
    clear_winners = view_strategy[view_strategy['Margin'] > margin_threshold]
    
    strategy_domains = {}
    for strategy in strategies:
        domains = clear_winners[clear_winners['Winner'] == strategy].index.tolist()
        strategy_domains[strategy] = domains[:5]  # Top 5
    
    y_pos = 0
    y_labels = []
    y_colors = []
    x_values = []
    
    for strategy in strategies:
        for view in strategy_domains.get(strategy, []):
            y_labels.append(view)
            y_colors.append(STRATEGY_COLORS[strategy])
            x_values.append(view_strategy.loc[view, strategy])
            y_pos += 1
    
    if y_labels:
        bars = ax.barh(range(len(y_labels)), x_values, color=y_colors)
        ax.set_yticks(range(len(y_labels)))
        ax.set_yticklabels(y_labels, fontsize=8)
        ax.set_xlabel(metric)
        ax.set_title('Views Where Each Strategy Dominates', fontweight='bold')
    
    # Panel 4: Strategy consistency (std across views)
    ax = axes[1, 1]
    
    consistency = df.groupby('Strategy')[metric].agg(['mean', 'std', 'min', 'max'])
    consistency['cv'] = consistency['std'] / consistency['mean']
    
    x = range(len(strategies))
    ax.bar(x, consistency.loc[strategies, 'mean'], 
           yerr=consistency.loc[strategies, 'std'],
           color=[STRATEGY_COLORS[s] for s in strategies],
           capsize=5, alpha=0.7)
    
    ax.set_xticks(x)
    ax.set_xticklabels(strategies)
    ax.set_ylabel(f'Mean {metric} (± std)')
    ax.set_title('Strategy Consistency Across Views', fontweight='bold')
    
    # Add CV annotations
    for i, s in enumerate(strategies):
        cv = consistency.loc[s, 'cv']
        ax.text(i, consistency.loc[s, 'mean'] + consistency.loc[s, 'std'] + 0.01,
               f'CV={cv:.3f}', ha='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f'strategy_by_view_{metric}.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: strategy_by_view_{metric}.png")


# =============================================================================
# Analysis 5: Pairwise Strategy Comparisons
# =============================================================================
def plot_pairwise_comparisons(df: pd.DataFrame, metric: str = 'SSIM'):
    """Direct head-to-head comparisons between strategies."""
    
    strategies = ['few-shot', 'agent', 'approach']
    pairs = [('few-shot', 'agent'), ('few-shot', 'approach'), ('agent', 'approach')]
    
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    
    # Row 1: Scatter plots
    for ax, (s1, s2) in zip(axes[0], pairs):
        # Get paired data - need to match on BOTH Category_View AND Base_Model
        # Because agent only has Claude, we need to compare within same model
        s1_df = df[df['Strategy'] == s1][['Category_View', 'Base_Model', metric]].dropna()
        s2_df = df[df['Strategy'] == s2][['Category_View', 'Base_Model', metric]].dropna()
        
        # Merge on both view and model to get proper pairs
        merged = pd.merge(s1_df, s2_df, on=['Category_View', 'Base_Model'], suffixes=('_1', '_2'))
        
        if len(merged) == 0:
            # Fallback: just compare by view (averaging across models)
            s1_means = df[df['Strategy'] == s1].groupby('Category_View')[metric].mean()
            s2_means = df[df['Strategy'] == s2].groupby('Category_View')[metric].mean()
            common = s1_means.index.intersection(s2_means.index)
            
            if len(common) == 0:
                ax.text(0.5, 0.5, f'No overlapping data\nfor {s1} vs {s2}', 
                       transform=ax.transAxes, ha='center', va='center', fontsize=11)
                ax.set_title(f'{s1} vs {s2}\n(No comparable data)', fontweight='bold')
                ax.set_xlabel(f'{s1} {metric}')
                ax.set_ylabel(f'{s2} {metric}')
                continue
            
            x = s1_means[common].values
            y = s2_means[common].values
        else:
            x = merged[f'{metric}_1'].values
            y = merged[f'{metric}_2'].values
        
        # Check for valid data
        valid_mask = ~(np.isnan(x) | np.isnan(y))
        x = x[valid_mask]
        y = y[valid_mask]
        
        if len(x) == 0:
            ax.text(0.5, 0.5, f'No valid data\nfor {s1} vs {s2}', 
                   transform=ax.transAxes, ha='center', va='center', fontsize=11)
            ax.set_title(f'{s1} vs {s2}\n(No valid data)', fontweight='bold')
            ax.set_xlabel(f'{s1} {metric}')
            ax.set_ylabel(f'{s2} {metric}')
            continue
        
        ax.scatter(x, y, alpha=0.6, c='steelblue', edgecolor='white', s=50)
        
        # Diagonal line (equal performance)
        all_vals = np.concatenate([x, y])
        min_val, max_val = all_vals.min(), all_vals.max()
        margin = (max_val - min_val) * 0.05 if max_val > min_val else 0.01
        lim = [min_val - margin, max_val + margin]
        ax.plot(lim, lim, 'k--', alpha=0.5, label='Equal')
        
        # Regression line
        if len(x) > 2:
            z = np.polyfit(x, y, 1)
            p_line = np.poly1d(z)
            x_sorted = np.sort(x)
            ax.plot(x_sorted, p_line(x_sorted), 'r-', alpha=0.7, label='Trend')
            
            r, pval = spearmanr(x, y)
            ax.text(0.05, 0.95, f'ρ = {r:.3f}\np = {pval:.4f}\nn = {len(x)}', 
                   transform=ax.transAxes, va='top', fontsize=9,
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        # Count wins
        s1_wins = (x > y).sum()
        s2_wins = (y > x).sum()
        
        ax.set_xlabel(f'{s1} {metric}')
        ax.set_ylabel(f'{s2} {metric}')
        ax.set_title(f'{s1} vs {s2}\n({s1}: {s1_wins} wins, {s2}: {s2_wins} wins)', fontweight='bold')
        ax.legend(loc='lower right')
        ax.set_xlim(lim)
        ax.set_ylim(lim)
    
    # Row 2: Difference distributions
    for ax, (s1, s2) in zip(axes[1], pairs):
        # Same matching logic
        s1_df = df[df['Strategy'] == s1][['Category_View', 'Base_Model', metric]].dropna()
        s2_df = df[df['Strategy'] == s2][['Category_View', 'Base_Model', metric]].dropna()
        
        merged = pd.merge(s1_df, s2_df, on=['Category_View', 'Base_Model'], suffixes=('_1', '_2'))
        
        if len(merged) == 0:
            # Fallback to view-level means
            s1_means = df[df['Strategy'] == s1].groupby('Category_View')[metric].mean()
            s2_means = df[df['Strategy'] == s2].groupby('Category_View')[metric].mean()
            common = s1_means.index.intersection(s2_means.index)
            
            if len(common) == 0:
                ax.text(0.5, 0.5, f'No overlapping data', 
                       transform=ax.transAxes, ha='center', va='center', fontsize=11)
                ax.set_xlabel('View')
                ax.set_ylabel(f'{metric} Difference')
                ax.set_title(f'{s1} vs {s2}\n(No comparable data)', fontweight='bold')
                continue
            
            diff = s2_means[common] - s1_means[common]
            labels = common.tolist()
        else:
            diff = merged[f'{metric}_2'] - merged[f'{metric}_1']
            labels = merged['Category_View'].tolist()
        
        # Remove NaN values
        diff = diff.dropna()
        
        if len(diff) == 0:
            ax.text(0.5, 0.5, 'No valid data', transform=ax.transAxes, ha='center', va='center')
            ax.set_xlabel('View')
            ax.set_ylabel(f'{metric} Difference')
            ax.set_title(f'{s1} vs {s2}', fontweight='bold')
            continue
        
        colors = ['green' if d > 0 else 'red' for d in diff]
        ax.bar(range(len(diff)), diff.values, color=colors, alpha=0.7)
        ax.axhline(0, color='black', linewidth=1)
        ax.axhline(diff.mean(), color='blue', linestyle='--', label=f'Mean diff: {diff.mean():.4f}')
        
        ax.set_xlabel('View')
        ax.set_ylabel(f'{metric} Difference ({s2} - {s1})')
        ax.set_title(f'Per-View Difference\n(Green = {s2} better, Red = {s1} better)', fontweight='bold')
        ax.legend()
        
        # Significance test
        if len(diff) >= 5:
            try:
                # Check if all differences are zero (would cause wilcoxon to fail)
                if (diff != 0).sum() > 0:
                    stat, p = wilcoxon(diff)
                    sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'ns'
                    ax.text(0.95, 0.95, f'Wilcoxon: {sig}\n(p={p:.4f})', transform=ax.transAxes, 
                           ha='right', va='top', fontsize=10,
                           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
            except Exception as e:
                pass  # Skip if test fails
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f'pairwise_comparisons_{metric}.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: pairwise_comparisons_{metric}.png")


# =============================================================================
# Analysis 6: LLM Quality Breakdown
# =============================================================================
def plot_llm_quality_breakdown(df: pd.DataFrame):
    """Detailed analysis of LLM quality scores (Clarity, Completeness, Consistency)."""
    
    strategies = ['few-shot', 'agent', 'approach']
    aspects = ['Clarity', 'Completeness', 'Consistency']
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    # Panel 1: Radar chart per strategy
    ax = axes[0, 0]
    
    angles = np.linspace(0, 2*np.pi, len(aspects), endpoint=False).tolist()
    angles += angles[:1]
    
    ax = plt.subplot(2, 2, 1, polar=True)
    
    for strategy in strategies:
        values = []
        for aspect in aspects:
            val = df[df['Strategy'] == strategy][aspect].mean()
            values.append(val if not np.isnan(val) else 0)
        values += values[:1]
        
        ax.plot(angles, values, 'o-', linewidth=2, label=strategy, color=STRATEGY_COLORS[strategy])
        ax.fill(angles, values, alpha=0.25, color=STRATEGY_COLORS[strategy])
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(aspects)
    ax.set_title('LLM Quality Profile by Strategy', fontweight='bold', y=1.08)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
    
    # Panel 2: Grouped bars
    ax = plt.subplot(2, 2, 2)
    x = np.arange(len(aspects))
    width = 0.25
    
    for i, strategy in enumerate(strategies):
        means = [df[df['Strategy'] == strategy][a].mean() for a in aspects]
        stds = [df[df['Strategy'] == strategy][a].std() for a in aspects]
        ax.bar(x + i*width, means, width, label=strategy, 
               color=STRATEGY_COLORS[strategy], yerr=stds, capsize=3)
    
    ax.set_xticks(x + width)
    ax.set_xticklabels(aspects)
    ax.set_ylabel('Score (0-1)')
    ax.set_title('LLM Quality Scores by Strategy', fontweight='bold')
    ax.legend()
    
    # Panel 3: Per-model breakdown
    ax = plt.subplot(2, 2, 3)
    
    data_for_heatmap = []
    for model in ['Claude', 'DeepSeek', 'GPT']:
        for strategy in strategies:
            subset = df[(df['Base_Model'] == model) & (df['Strategy'] == strategy)]
            composite = subset['LLM_Composite'].mean()
            data_for_heatmap.append({
                'Model': model,
                'Strategy': strategy,
                'LLM_Composite': composite
            })
    
    heat_df = pd.DataFrame(data_for_heatmap)
    pivot = heat_df.pivot(index='Model', columns='Strategy', values='LLM_Composite')
    
    sns.heatmap(pivot[strategies], annot=True, fmt='.3f', cmap='RdYlGn', ax=ax)
    ax.set_title('LLM Composite by Model × Strategy', fontweight='bold')
    
    # Panel 4: Quality vs SSIM correlation
    ax = plt.subplot(2, 2, 4)
    
    for strategy in strategies:
        subset = df[df['Strategy'] == strategy].dropna(subset=['SSIM', 'LLM_Composite'])
        ax.scatter(subset['SSIM'], subset['LLM_Composite'], 
                  label=strategy, color=STRATEGY_COLORS[strategy], alpha=0.6)
    
    ax.set_xlabel('SSIM')
    ax.set_ylabel('LLM Composite')
    ax.set_title('Image Quality vs LLM Quality', fontweight='bold')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'llm_quality_breakdown.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: llm_quality_breakdown.png")


# =============================================================================
# Analysis 7: Paradigm Comparison (Few-shot vs Agentic)
# =============================================================================
def plot_paradigm_comparison(df: pd.DataFrame, metric: str = 'SSIM'):
    """
    Compare standard prompting (few-shot) vs agentic approaches (agent + approach).
    This groups agent and approach together as "agentic" paradigm.
    """
    
    # Create paradigm column
    df_copy = df.copy()
    df_copy['Paradigm'] = df_copy['Strategy'].apply(
        lambda x: 'Standard (Few-shot)' if x == 'few-shot' else 'Agentic (Agent/Approach)'
    )
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    
    # Panel 1: Overall paradigm comparison
    ax = axes[0, 0]
    paradigm_data = [
        df_copy[df_copy['Paradigm'] == 'Standard (Few-shot)'][metric].dropna(),
        df_copy[df_copy['Paradigm'] == 'Agentic (Agent/Approach)'][metric].dropna()
    ]
    
    bp = ax.boxplot(paradigm_data, labels=['Standard\n(Few-shot)', 'Agentic\n(Agent/Approach)'], 
                    patch_artist=True)
    bp['boxes'][0].set_facecolor('#3498DB')
    bp['boxes'][1].set_facecolor('#E74C3C')
    
    # Significance test
    if len(paradigm_data[0]) > 0 and len(paradigm_data[1]) > 0:
        stat, p = mannwhitneyu(paradigm_data[0], paradigm_data[1], alternative='two-sided')
        sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'ns'
        ax.text(1.5, ax.get_ylim()[1], f'p={p:.4f} ({sig})', ha='center', fontsize=10)
    
    ax.set_ylabel(metric)
    ax.set_title(f'Paradigm Comparison: {metric}', fontweight='bold')
    
    # Panel 2: Paradigm by model
    ax = axes[0, 1]
    paradigm_model = df_copy.groupby(['Base_Model', 'Paradigm'])[metric].mean().unstack()
    paradigm_model.plot(kind='bar', ax=ax, color=['#3498DB', '#E74C3C'], width=0.7)
    ax.set_xlabel('Model')
    ax.set_ylabel(f'Mean {metric}')
    ax.set_title('Paradigm Performance by Model', fontweight='bold')
    ax.legend(title='Paradigm')
    ax.tick_params(axis='x', rotation=0)
    
    # Panel 3: Paradigm by category
    ax = axes[0, 2]
    paradigm_cat = df_copy.groupby(['Category', 'Paradigm'])[metric].mean().unstack()
    paradigm_cat.plot(kind='barh', ax=ax, color=['#3498DB', '#E74C3C'], width=0.7)
    ax.set_xlabel(f'Mean {metric}')
    ax.set_title('Paradigm Performance by Category', fontweight='bold')
    ax.legend(title='Paradigm')
    
    # Panel 4: Within agentic - Agent vs Approach (Claude only for fair comparison)
    ax = axes[1, 0]
    claude_agent = df[(df['Strategy'] == 'agent') & (df['Base_Model'] == 'Claude')][metric].dropna()
    claude_approach = df[(df['Strategy'] == 'approach') & (df['Base_Model'] == 'Claude')][metric].dropna()
    
    if len(claude_agent) > 0 and len(claude_approach) > 0:
        bp = ax.boxplot([claude_agent, claude_approach], 
                       labels=['Agent\n(Claude)', 'Approach\n(Claude)'], 
                       patch_artist=True)
        bp['boxes'][0].set_facecolor('#E74C3C')
        bp['boxes'][1].set_facecolor('#2ECC71')
        
        stat, p = mannwhitneyu(claude_agent, claude_approach, alternative='two-sided')
        sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'ns'
        ax.text(1.5, ax.get_ylim()[1], f'p={p:.4f} ({sig})', ha='center', fontsize=10)
    
    ax.set_ylabel(metric)
    ax.set_title('Agentic Comparison (Claude only)\nAgent vs Approach', fontweight='bold')
    
    # Panel 5: Few-shot vs Approach across all models
    ax = axes[1, 1]
    models = ['Claude', 'DeepSeek', 'GPT']
    x = np.arange(len(models))
    width = 0.35
    
    fewshot_means = [df[(df['Strategy'] == 'few-shot') & (df['Base_Model'] == m)][metric].mean() for m in models]
    approach_means = [df[(df['Strategy'] == 'approach') & (df['Base_Model'] == m)][metric].mean() for m in models]
    
    ax.bar(x - width/2, fewshot_means, width, label='Few-shot', color='#3498DB')
    ax.bar(x + width/2, approach_means, width, label='Approach', color='#2ECC71')
    
    ax.set_xticks(x)
    ax.set_xticklabels(models)
    ax.set_ylabel(f'Mean {metric}')
    ax.set_title('Few-shot vs Approach (by Model)', fontweight='bold')
    ax.legend()
    
    # Add delta annotations
    for i, (f, a) in enumerate(zip(fewshot_means, approach_means)):
        if not np.isnan(f) and not np.isnan(a):
            delta = a - f
            color = 'green' if delta > 0 else 'red'
            ax.annotate(f'{delta:+.3f}', (i, max(f, a) + 0.01), ha='center', fontsize=9, color=color)
    
    # Panel 6: Summary table
    ax = axes[1, 2]
    ax.axis('off')
    
    summary_data = []
    
    # Overall means
    for strategy in ['few-shot', 'agent', 'approach']:
        s_data = df[df['Strategy'] == strategy][metric]
        summary_data.append({
            'Strategy': strategy,
            'N': len(s_data),
            'Mean': f'{s_data.mean():.4f}',
            'Std': f'{s_data.std():.4f}',
            'Models': ', '.join(df[df['Strategy'] == strategy]['Base_Model'].unique())
        })
    
    summary_df = pd.DataFrame(summary_data)
    table = ax.table(cellText=summary_df.values, colLabels=summary_df.columns,
                     loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 2)
    ax.set_title('Strategy Summary', fontweight='bold', y=0.85)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f'paradigm_comparison_{metric}.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: paradigm_comparison_{metric}.png")


# =============================================================================
# Analysis 8: Claude-Specific Deep Dive (All 3 strategies available)
# =============================================================================
def plot_claude_comparison(df: pd.DataFrame, metric: str = 'SSIM'):
    """
    Deep dive into Claude specifically, since it's the only model with all 3 strategies.
    This is the fairest comparison.
    """
    
    claude_df = df[df['Base_Model'] == 'Claude'].copy()
    strategies = ['few-shot', 'agent', 'approach']
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    
    # Panel 1: Overall comparison for Claude
    ax = axes[0, 0]
    data_to_plot = [claude_df[claude_df['Strategy'] == s][metric].dropna() for s in strategies]
    
    bp = ax.boxplot(data_to_plot, labels=['Few-shot', 'Agent', 'Approach'], patch_artist=True)
    colors = [STRATEGY_COLORS[s] for s in strategies]
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    # Add means
    means = [d.mean() for d in data_to_plot]
    ax.scatter([1, 2, 3], means, color='black', marker='D', s=50, zorder=5)
    
    ax.set_ylabel(metric)
    ax.set_title(f'Claude: {metric} by Strategy\n(Fair comparison - same model)', fontweight='bold')
    
    # Panel 2: By category for Claude
    ax = axes[0, 1]
    claude_pivot = claude_df.groupby(['Category', 'Strategy'])[metric].mean().unstack()
    claude_pivot = claude_pivot[[s for s in strategies if s in claude_pivot.columns]]
    
    sns.heatmap(claude_pivot, annot=True, fmt='.3f', cmap='RdYlGn', ax=ax)
    ax.set_title('Claude: Performance by Category', fontweight='bold')
    
    # Panel 3: Winner per category for Claude
    ax = axes[0, 2]
    if not claude_pivot.empty:
        winners = claude_pivot.idxmax(axis=1)
        winner_counts = winners.value_counts()
        colors = [STRATEGY_COLORS.get(s, 'gray') for s in winner_counts.index]
        ax.pie(winner_counts.values, labels=winner_counts.index, autopct='%1.1f%%', 
               colors=colors, startangle=90)
        ax.set_title('Claude: Which Strategy Wins\nMost Categories?', fontweight='bold')
    
    # Panel 4: View-level scatter (Agent vs Approach for Claude)
    ax = axes[1, 0]
    agent_views = claude_df[claude_df['Strategy'] == 'agent'].groupby('Category_View')[metric].mean()
    approach_views = claude_df[claude_df['Strategy'] == 'approach'].groupby('Category_View')[metric].mean()
    common = agent_views.index.intersection(approach_views.index)
    
    if len(common) > 0:
        ax.scatter(agent_views[common], approach_views[common], alpha=0.7, s=60, c='steelblue')
        lim = [min(agent_views[common].min(), approach_views[common].min()) * 0.95,
               max(agent_views[common].max(), approach_views[common].max()) * 1.05]
        ax.plot(lim, lim, 'k--', alpha=0.5, label='Equal')
        
        agent_wins = (agent_views[common] > approach_views[common]).sum()
        approach_wins = (approach_views[common] > agent_views[common]).sum()
        
        ax.set_xlabel(f'Agent {metric}')
        ax.set_ylabel(f'Approach {metric}')
        ax.set_title(f'Claude: Agent vs Approach\n(Agent wins: {agent_wins}, Approach wins: {approach_wins})', 
                    fontweight='bold')
        ax.legend()
    
    # Panel 5: View-level scatter (Few-shot vs Approach for Claude)
    ax = axes[1, 1]
    fewshot_views = claude_df[claude_df['Strategy'] == 'few-shot'].groupby('Category_View')[metric].mean()
    approach_views = claude_df[claude_df['Strategy'] == 'approach'].groupby('Category_View')[metric].mean()
    common = fewshot_views.index.intersection(approach_views.index)
    
    if len(common) > 0:
        ax.scatter(fewshot_views[common], approach_views[common], alpha=0.7, s=60, c='steelblue')
        lim = [min(fewshot_views[common].min(), approach_views[common].min()) * 0.95,
               max(fewshot_views[common].max(), approach_views[common].max()) * 1.05]
        ax.plot(lim, lim, 'k--', alpha=0.5, label='Equal')
        
        fewshot_wins = (fewshot_views[common] > approach_views[common]).sum()
        approach_wins = (approach_views[common] > fewshot_views[common]).sum()
        
        ax.set_xlabel(f'Few-shot {metric}')
        ax.set_ylabel(f'Approach {metric}')
        ax.set_title(f'Claude: Few-shot vs Approach\n(Few-shot wins: {fewshot_wins}, Approach wins: {approach_wins})', 
                    fontweight='bold')
        ax.legend()
    
    # Panel 6: Statistical tests for Claude
    ax = axes[1, 2]
    ax.axis('off')
    
    results = []
    # Kruskal-Wallis
    groups = [claude_df[claude_df['Strategy'] == s][metric].dropna() for s in strategies]
    groups = [g for g in groups if len(g) > 0]
    if len(groups) >= 2:
        stat, p = kruskal(*groups)
        results.append({'Test': 'Kruskal-Wallis (3-way)', 'p-value': f'{p:.4f}', 
                       'Sig': 'Yes' if p < 0.05 else 'No'})
    
    # Pairwise
    for s1, s2 in [('few-shot', 'agent'), ('few-shot', 'approach'), ('agent', 'approach')]:
        g1 = claude_df[claude_df['Strategy'] == s1][metric].dropna()
        g2 = claude_df[claude_df['Strategy'] == s2][metric].dropna()
        if len(g1) > 0 and len(g2) > 0:
            stat, p = mannwhitneyu(g1, g2, alternative='two-sided')
            results.append({'Test': f'{s1} vs {s2}', 'p-value': f'{p:.4f}',
                           'Sig': 'Yes' if p < 0.05 else 'No'})
    
    if results:
        results_df = pd.DataFrame(results)
        table = ax.table(cellText=results_df.values, colLabels=results_df.columns,
                         loc='center', cellLoc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.3, 2)
        
        # Color significant rows
        for i, row in results_df.iterrows():
            if row['Sig'] == 'Yes':
                for j in range(len(results_df.columns)):
                    table[(i+1, j)].set_facecolor('#90EE90')
    
    ax.set_title('Claude: Statistical Tests', fontweight='bold', y=0.9)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f'claude_comparison_{metric}.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: claude_comparison_{metric}.png")


# =============================================================================
# Analysis 7: Statistical Summary
# =============================================================================
def generate_statistical_summary(df: pd.DataFrame):
    """Comprehensive statistical tests."""
    
    strategies = ['few-shot', 'agent', 'approach']
    results = []
    
    for metric in ['SSIM', 'PSNR', 'LLM_Composite']:
        if metric not in df.columns or df[metric].isna().all():
            continue
        
        # Kruskal-Wallis (overall difference)
        groups = [df[df['Strategy'] == s][metric].dropna() for s in strategies]
        groups = [g for g in groups if len(g) > 0]
        
        if len(groups) >= 2:
            stat, p = kruskal(*groups)
            results.append({
                'Metric': metric,
                'Test': 'Kruskal-Wallis (3-way)',
                'Statistic': f'{stat:.2f}',
                'p-value': f'{p:.4f}',
                'Significant': 'Yes' if p < 0.05 else 'No'
            })
        
        # Pairwise Mann-Whitney
        for s1, s2 in [('few-shot', 'agent'), ('few-shot', 'approach'), ('agent', 'approach')]:
            g1 = df[df['Strategy'] == s1][metric].dropna()
            g2 = df[df['Strategy'] == s2][metric].dropna()
            
            if len(g1) > 0 and len(g2) > 0:
                stat, p = mannwhitneyu(g1, g2, alternative='two-sided')
                results.append({
                    'Metric': metric,
                    'Test': f'Mann-Whitney: {s1} vs {s2}',
                    'Statistic': f'{stat:.0f}',
                    'p-value': f'{p:.4f}',
                    'Significant': 'Yes' if p < 0.05 else 'No'
                })
    
    results_df = pd.DataFrame(results)
    
    # Save as image
    fig, ax = plt.subplots(figsize=(12, len(results_df)*0.4 + 2))
    ax.axis('off')
    
    table = ax.table(cellText=results_df.values, colLabels=results_df.columns,
                     loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.6)
    
    # Color significant rows
    for i, row in results_df.iterrows():
        if row['Significant'] == 'Yes':
            for j in range(len(results_df.columns)):
                table[(i+1, j)].set_facecolor('#90EE90')
    
    ax.set_title('Statistical Significance Tests:\nFew-Shot vs Agent vs Approach', 
                fontweight='bold', fontsize=14, y=0.98)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'statistical_significance.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    results_df.to_csv(OUTPUT_DIR / 'statistical_significance.csv', index=False)
    print("Saved: statistical_significance.png, statistical_significance.csv")
    
    return results_df


# =============================================================================
# Analysis 10: Key Findings Summary
# =============================================================================
def generate_key_findings(df: pd.DataFrame):
    """Auto-generate key findings."""
    
    strategies = ['few-shot', 'agent', 'approach']
    findings = []
    
    print("\n" + "="*70)
    print("KEY FINDINGS: Few-Shot vs Agent vs Approach")
    print("="*70)
    
    # 1. Overall winner
    overall = df.groupby('Strategy')['SSIM'].mean()
    winner = overall.idxmax()
    findings.append(f"1. OVERALL BEST (SSIM): {winner} ({overall[winner]:.4f})")
    findings.append(f"   Rankings: {', '.join([f'{s}: {overall[s]:.4f}' for s in overall.sort_values(ascending=False).index])}")
    
    # 2. LLM winner
    if 'LLM_Composite' in df.columns:
        llm_overall = df.groupby('Strategy')['LLM_Composite'].mean()
        llm_winner = llm_overall.idxmax()
        findings.append(f"\n2. BEST LLM QUALITY: {llm_winner} ({llm_overall[llm_winner]:.4f})")
    
    # 3. Paradigm comparison
    findings.append("\n3. PARADIGM COMPARISON (Standard vs Agentic):")
    fewshot_mean = df[df['Strategy'] == 'few-shot']['SSIM'].mean()
    agentic_mean = df[df['Strategy'].isin(['agent', 'approach'])]['SSIM'].mean()
    findings.append(f"   Standard (Few-shot): {fewshot_mean:.4f}")
    findings.append(f"   Agentic (Agent+Approach): {agentic_mean:.4f}")
    findings.append(f"   Difference: {agentic_mean - fewshot_mean:+.4f} ({'Agentic better' if agentic_mean > fewshot_mean else 'Standard better'})")
    
    # 4. Claude-specific (fair comparison - all 3 strategies)
    findings.append("\n4. CLAUDE-SPECIFIC (Fair comparison - all 3 strategies):")
    for s in strategies:
        s_data = df[(df['Strategy'] == s) & (df['Base_Model'] == 'Claude')]['SSIM']
        if len(s_data) > 0:
            findings.append(f"   {s}: {s_data.mean():.4f}")
    
    # 5. Per-model winners (for strategies with multiple models)
    findings.append("\n5. BEST STRATEGY PER MODEL:")
    for model in ['Claude', 'DeepSeek', 'GPT']:
        model_data = df[df['Base_Model'] == model]
        if not model_data.empty and model_data['Strategy'].nunique() > 1:
            model_winner = model_data.groupby('Strategy')['SSIM'].mean().idxmax()
            findings.append(f"   {model}: {model_winner}")
        elif not model_data.empty:
            findings.append(f"   {model}: only {model_data['Strategy'].unique()[0]} available")
    
    # 6. Per-category winners
    findings.append("\n6. BEST STRATEGY PER CATEGORY:")
    for cat in sorted(df['Category'].unique()):
        cat_data = df[df['Category'] == cat]
        if not cat_data.empty:
            cat_winner = cat_data.groupby('Strategy')['SSIM'].mean().idxmax()
            cat_score = cat_data.groupby('Strategy')['SSIM'].mean().max()
            findings.append(f"   {cat}: {cat_winner} ({cat_score:.4f})")
    
    # 7. Consistency (variance)
    findings.append("\n7. CONSISTENCY (lower CV = more reliable):")
    for s in strategies:
        s_data = df[df['Strategy'] == s]['SSIM']
        if len(s_data) > 0:
            cv = s_data.std() / s_data.mean() if s_data.mean() > 0 else 0
            findings.append(f"   {s}: CV = {cv:.4f} (n={len(s_data)})")
    
    # 8. Head-to-head summary
    findings.append("\n8. HEAD-TO-HEAD (view-level wins):")
    for s1, s2 in [('few-shot', 'agent'), ('few-shot', 'approach'), ('agent', 'approach')]:
        s1_data = df[df['Strategy'] == s1].groupby('Category_View')['SSIM'].mean()
        s2_data = df[df['Strategy'] == s2].groupby('Category_View')['SSIM'].mean()
        common = s1_data.index.intersection(s2_data.index)
        if len(common) > 0:
            s1_wins = (s1_data[common] > s2_data[common]).sum()
            s2_wins = (s2_data[common] > s1_data[common]).sum()
            findings.append(f"   {s1} vs {s2}: {s1_wins} - {s2_wins} (n={len(common)} views)")
        else:
            findings.append(f"   {s1} vs {s2}: No overlapping views to compare")
    
    # 9. Key insight
    findings.append("\n9. KEY INSIGHT:")
    claude_data = df[df['Base_Model'] == 'Claude']
    if not claude_data.empty:
        claude_best = claude_data.groupby('Strategy')['SSIM'].mean().idxmax()
        findings.append(f"   For Claude (only model with all 3 strategies): {claude_best} performs best")
    
    # Print and save
    for f in findings:
        print(f)
    
    with open(OUTPUT_DIR / 'key_findings.txt', 'w') as file:
        file.write("KEY FINDINGS: Few-Shot vs Agent vs Approach\n")
        file.write("="*70 + "\n")
        file.write("\nExperimental Setup:\n")
        file.write("  - Few-shot: Claude, DeepSeek, GPT (standard prompting)\n")
        file.write("  - Agent: Claude only (agentic approach)\n")
        file.write("  - Approach: Claude, DeepSeek, GPT (agentic approach)\n")
        file.write("\n" + "="*70 + "\n\n")
        for f in findings:
            file.write(f + "\n")
    
    print(f"\nSaved: key_findings.txt")
    
    return findings


# =============================================================================
# Main
# =============================================================================
def main(data_dir: str):
    """Run all analyses."""
    data_path = Path(data_dir)
    
    print("="*70)
    print("FOCUSED ANALYSIS: Few-Shot vs Agent vs Approach")
    print("="*70)
    print("\nExperimental Setup:")
    print("  - Few-shot: Claude, DeepSeek, GPT (standard prompting)")
    print("  - Agent: Claude only (agentic approach)")
    print("  - Approach: Claude, DeepSeek, GPT (agentic approach)")
    
    print(f"\nLoading data from: {data_path}")
    df = load_and_filter_data(data_path)
    
    print(f"\nFiltered data summary:")
    print(f"  Total rows: {len(df)}")
    print(f"  Strategies: {df['Strategy'].unique().tolist()}")
    print(f"  Models: {df['Base_Model'].unique().tolist()}")
    print(f"  Categories: {df['Category'].unique().tolist()}")
    print(f"  Unique views: {df['Category_View'].nunique()}")
    
    print(f"\nSamples per strategy:")
    print(df['Strategy'].value_counts())
    
    print(f"\nStrategy × Model breakdown:")
    print(df.groupby(['Strategy', 'Base_Model']).size().unstack(fill_value=0))
    
    print("\n" + "="*70)
    print("GENERATING ANALYSES...")
    print("="*70)
    
    # Run all analyses
    plot_overall_comparison(df)
    
    for metric in ['SSIM', 'LLM_Composite']:
        if metric in df.columns and df[metric].notna().sum() > 0:
            print(f"\n--- {metric} analyses ---")
            plot_strategy_by_model(df, metric)
            plot_strategy_by_category(df, metric)
            plot_strategy_by_view(df, metric)
            plot_pairwise_comparisons(df, metric)
            plot_paradigm_comparison(df, metric)
            plot_claude_comparison(df, metric)
    
    plot_llm_quality_breakdown(df)
    generate_statistical_summary(df)
    generate_key_findings(df)
    
    print(f"\n" + "="*70)
    print(f"ALL OUTPUTS SAVED TO: {OUTPUT_DIR.absolute()}")
    print("="*70)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Usage: python focused_analysis.py <data_directory>")
        print("\nExample: python focused_analysis.py .")