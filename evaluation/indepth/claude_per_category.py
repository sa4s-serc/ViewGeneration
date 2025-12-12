"""
Clean Heatmap Generator for Publication
========================================

- NO titles
- Clean readable labels
- ArchView instead of Approach
- Red (Agent), Blue (Few-shot), Green (ArchView)
- Professional publication-ready style
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Output directory
OUTPUT_DIR = Path("./clean_plots")
OUTPUT_DIR.mkdir(exist_ok=True)

# =============================================================================
# SETTINGS
# =============================================================================

STRATEGIES = ['fewshot_claude', 'agent_claude', 'approach_claude']

# Column labels (what appears in the heatmap)
STRATEGY_LABELS = ['Few-shot', 'Agent', 'ArchView']

# Colors for other plots (not used in heatmap directly)
COLORS = {
    'fewshot_claude': '#3498DB',      # Blue
    'agent_claude': '#E74C3C',         # Red  
    'approach_claude': '#27AE60'       # Green
}

# =============================================================================
# NOTATION LABEL MAPPING - CLEAN READABLE NAMES
# =============================================================================
NOTATION_LABELS = {
    'UML': 'UML',
    'boxes': 'Boxes',
    'boxes_and_arrows': 'Boxes & Arrows',
    'boxes_and_arrows_icons_and_arrows': 'Boxes & Arrows,\nIcons & Arrows',
    'boxes_boxes_and_arrows': 'Boxes,\nBoxes & Arrows',
    'boxes_icons_and_arrows': 'Boxes,\nIcons & Arrows',
    'icons_and_arrows': 'Icons & Arrows',
    'icons_and_arrows_boxes': 'Icons & Arrows,\nBoxes'
}

CONCERN_LABELS = {
    'connectivity': 'Connectivity',
    'control_flow': 'Control Flow',
    'data_flow': 'Data Flow',
    'deployment': 'Deployment',
    'general': 'General',
    'performance': 'Performance',
    'scheduling': 'Scheduling',
    'security': 'Security'
}

QAS_LABELS = {
    'compatibility': 'Compatibility',
    'flexibility': 'Flexibility',
    'functional_suitability': 'Functional Suitability',
    'interaction_capability': 'Interaction Capability',
    'maintainability': 'Maintainability',
    'performance_efficiency': 'Performance Efficiency',
    'reliability': 'Reliability',
    'security': 'Security'
}

SCOPE_LABELS = {
    'part': 'Part',
    'entire': 'Entire',
    'entire+': 'Entire+'
}

GRANULARITY_LABELS = {
    'low': 'Low',
    'medium': 'Medium',
    'high': 'High'
}


def get_label_map(category: str) -> dict:
    """Get the appropriate label map for a category."""
    maps = {
        'notation': NOTATION_LABELS,
        'concern': CONCERN_LABELS,
        'qas': QAS_LABELS,
        'scope': SCOPE_LABELS,
        'granularity': GRANULARITY_LABELS
    }
    return maps.get(category, {})


# =============================================================================
# DATA LOADING
# =============================================================================
def load_data(data_dir: Path) -> pd.DataFrame:
    """Load all simple_table CSVs and extract Claude data."""
    rows = []
    
    for f in data_dir.glob("simple_table_*.csv"):
        name = f.stem.replace("simple_table_", "")
        df = pd.read_csv(f)
        
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
            model_name = row['Model'].lower().replace(' ', '_')
            
            if 'claude' not in model_name:
                continue
            
            if 'fewshot' in model_name or 'few_shot' in model_name:
                strategy = 'fewshot_claude'
            elif 'agent' in model_name:
                strategy = 'agent_claude'
            elif 'approach' in model_name:
                strategy = 'approach_claude'
            else:
                continue
            
            row_data = {
                'Strategy': strategy,
                'Category': category,
                'View': view,
                'SSIM': row.get('SSIM', np.nan),
                'PSNR': row.get('PSNR', np.nan),
                'RMSE': row.get('RMSE', np.nan),
            }
            
            for aspect in ['Clarity', 'Completeness', 'Consistency']:
                meets = row.get(f'LLM_{aspect}_Rating_Meets', 0)
                partial = row.get(f'LLM_{aspect}_Rating_PartiallyMeets', 0)
                total = meets + partial + row.get(f'LLM_{aspect}_Rating_DoesNotMeet', 0)
                if total > 0:
                    row_data[aspect] = (2*meets + partial) / (2*total)
                else:
                    row_data[aspect] = np.nan
            
            scores = [row_data.get(a, np.nan) for a in ['Clarity', 'Completeness', 'Consistency']]
            valid_scores = [s for s in scores if not np.isnan(s)]
            row_data['LLM_Composite'] = np.mean(valid_scores) if valid_scores else np.nan
            
            rows.append(row_data)
    
    return pd.DataFrame(rows)


# =============================================================================
# SINGLE HEATMAP - CLEAN VERSION
# =============================================================================
def create_single_heatmap(df: pd.DataFrame, category: str, metric: str, output_file: Path):
    """
    Create a single clean heatmap.
    NO title, clean labels, publication ready.
    """
    cat_df = df[df['Category'] == category]
    
    # Create pivot table
    pivot = cat_df.pivot_table(index='View', columns='Strategy', values=metric, aggfunc='mean')
    pivot = pivot[STRATEGIES]  # Ensure correct order
    
    # Get label map and apply clean labels to rows
    label_map = get_label_map(category)
    pivot.index = [label_map.get(v, v) for v in pivot.index]
    
    # Apply clean column labels
    pivot.columns = STRATEGY_LABELS
    
    # Figure size based on number of rows
    n_rows = len(pivot)
    fig_height = max(4, n_rows * 0.6)
    fig_width = 6
    
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    
    # Create heatmap - NO title
    sns.heatmap(
        pivot,
        annot=True,
        fmt='.3f',
        cmap='RdYlGn',
        center=pivot.values.mean(),
        annot_kws={'size': 12, 'fontweight': 'bold'},
        linewidths=2,
        linecolor='white',
        cbar_kws={'label': metric, 'shrink': 0.8},
        square=False,
        ax=ax
    )
    
    # Clean up axes - NO xlabel, NO ylabel, NO title
    ax.set_xlabel('')
    ax.set_ylabel('')
    
    # Style the tick labels
    ax.set_xticklabels(STRATEGY_LABELS, fontsize=12, fontweight='bold', rotation=0)
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=11, rotation=0)
    
    # Adjust colorbar label
    cbar = ax.collections[0].colorbar
    cbar.ax.set_ylabel(metric, fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print(f"Saved: {output_file}")


# =============================================================================
# SIDE-BY-SIDE HEATMAPS (SSIM + LLM)
# =============================================================================
def create_dual_heatmap(df: pd.DataFrame, category: str, output_file: Path):
    """
    Create side-by-side heatmaps for SSIM and LLM Quality.
    NO title, clean labels.
    """
    cat_df = df[df['Category'] == category]
    label_map = get_label_map(category)
    
    fig, axes = plt.subplots(1, 2, figsize=(13, max(4, len(cat_df['View'].unique()) * 0.6)))
    
    for ax, metric, cbar_label in zip(axes, ['SSIM', 'LLM_Composite'], ['SSIM', 'LLM Quality']):
        # Create pivot
        pivot = cat_df.pivot_table(index='View', columns='Strategy', values=metric, aggfunc='mean')
        pivot = pivot[STRATEGIES]
        
        # Clean labels
        pivot.index = [label_map.get(v, v) for v in pivot.index]
        pivot.columns = STRATEGY_LABELS
        
        # Heatmap
        sns.heatmap(
            pivot,
            annot=True,
            fmt='.3f',
            cmap='RdYlGn',
            annot_kws={'size': 11, 'fontweight': 'bold'},
            linewidths=2,
            linecolor='white',
            cbar_kws={'label': cbar_label, 'shrink': 0.8},
            ax=ax
        )
        
        # NO title, NO axis labels
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.set_xticklabels(STRATEGY_LABELS, fontsize=11, fontweight='bold', rotation=0)
        ax.set_yticklabels(ax.get_yticklabels(), fontsize=10, rotation=0)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print(f"Saved: {output_file}")


# =============================================================================
# BAR CHART - CLEAN VERSION
# =============================================================================
def create_bar_chart(df: pd.DataFrame, category: str, metric: str, output_file: Path):
    """
    Create clean grouped bar chart.
    NO title.
    """
    cat_df = df[df['Category'] == category]
    label_map = get_label_map(category)
    views = sorted(cat_df['View'].unique())
    
    fig, ax = plt.subplots(figsize=(max(8, len(views) * 1.2), 5))
    
    x = np.arange(len(views))
    width = 0.25
    
    for i, (strategy, label, color) in enumerate(zip(STRATEGIES, STRATEGY_LABELS, 
                                                      [COLORS[s] for s in STRATEGIES])):
        means = [cat_df[(cat_df['Strategy'] == strategy) & (cat_df['View'] == v)][metric].mean() 
                for v in views]
        ax.bar(x + i*width, means, width, label=label, color=color, alpha=0.85,
              edgecolor='white', linewidth=0.5)
    
    # Clean labels
    clean_labels = [label_map.get(v, v) for v in views]
    
    ax.set_ylabel(metric, fontsize=12, fontweight='bold')
    ax.set_xticks(x + width)
    ax.set_xticklabels(clean_labels, fontsize=10, rotation=45, ha='right')
    ax.legend(fontsize=11, framealpha=0.9)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_axisbelow(True)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print(f"Saved: {output_file}")


# =============================================================================
# RADAR CHART - CLEAN VERSION
# =============================================================================
def create_radar_chart(df: pd.DataFrame, category: str, metric: str, output_file: Path):
    """
    Create clean radar chart.
    NO title.
    """
    cat_df = df[df['Category'] == category]
    label_map = get_label_map(category)
    views = sorted(cat_df['View'].unique())
    
    if len(views) < 3:
        print(f"  Skipping radar for {category} (< 3 views)")
        return
    
    angles = np.linspace(0, 2*np.pi, len(views), endpoint=False).tolist()
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    
    for strategy, label, color in zip(STRATEGIES, STRATEGY_LABELS, [COLORS[s] for s in STRATEGIES]):
        values = [cat_df[(cat_df['Strategy'] == strategy) & (cat_df['View'] == v)][metric].mean() 
                 for v in views]
        values += values[:1]
        ax.plot(angles, values, 'o-', linewidth=2.5, label=label, color=color, markersize=6)
        ax.fill(angles, values, alpha=0.15, color=color)
    
    # Clean labels (shortened if needed)
    clean_labels = [label_map.get(v, v)[:15] for v in views]
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(clean_labels, fontsize=10)
    ax.legend(loc='upper right', bbox_to_anchor=(1.25, 1.0), fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print(f"Saved: {output_file}")


# =============================================================================
# WINNER PIE CHART - CLEAN VERSION
# =============================================================================
def create_winner_pie(df: pd.DataFrame, category: str, metric: str, output_file: Path):
    """
    Create clean pie chart showing which strategy wins most.
    NO title.
    """
    cat_df = df[df['Category'] == category]
    
    pivot = cat_df.pivot_table(index='View', columns='Strategy', values=metric, aggfunc='mean')
    pivot = pivot[STRATEGIES].dropna()
    
    if len(pivot) == 0:
        return
    
    winners = pivot.idxmax(axis=1)
    winner_counts = winners.value_counts()
    
    fig, ax = plt.subplots(figsize=(6, 6))
    
    colors = [COLORS[s] for s in winner_counts.index]
    labels = [STRATEGY_LABELS[STRATEGIES.index(s)] for s in winner_counts.index]
    
    wedges, texts, autotexts = ax.pie(
        winner_counts.values,
        labels=labels,
        autopct='%1.1f%%',
        colors=colors,
        startangle=90,
        textprops={'fontsize': 12, 'fontweight': 'bold'},
        wedgeprops={'edgecolor': 'white', 'linewidth': 2}
    )
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(11)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print(f"Saved: {output_file}")


# =============================================================================
# TREND LINE CHART - CLEAN VERSION
# =============================================================================
def create_trend_chart(df: pd.DataFrame, category: str, metric: str, output_file: Path, 
                       view_order: list = None, x_labels: list = None):
    """
    Create clean trend line chart.
    NO title.
    """
    cat_df = df[df['Category'] == category]
    
    if view_order:
        views = [v for v in view_order if v in cat_df['View'].unique()]
    else:
        views = sorted(cat_df['View'].unique())
    
    if len(views) < 2:
        return
    
    fig, ax = plt.subplots(figsize=(8, 5))
    
    for strategy, label, color in zip(STRATEGIES, STRATEGY_LABELS, [COLORS[s] for s in STRATEGIES]):
        values = [cat_df[(cat_df['Strategy'] == strategy) & (cat_df['View'] == v)][metric].mean() 
                 for v in views]
        ax.plot(range(len(views)), values, 'o-', linewidth=2.5, markersize=10,
               label=label, color=color)
    
    ax.set_ylabel(metric, fontsize=12, fontweight='bold')
    ax.set_xticks(range(len(views)))
    ax.set_xticklabels(x_labels if x_labels else views, fontsize=11)
    ax.legend(fontsize=11)
    ax.grid(alpha=0.3, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print(f"Saved: {output_file}")


# =============================================================================
# GENERATE ALL PLOTS FOR A CATEGORY
# =============================================================================
def generate_category_plots(df: pd.DataFrame, category: str):
    """Generate all plots for a category."""
    
    output_dir = OUTPUT_DIR / category
    output_dir.mkdir(exist_ok=True)
    
    print(f"\n{'='*50}")
    print(f"{category.upper()}")
    print(f"{'='*50}")
    
    # Dual heatmap (SSIM + LLM side by side)
    create_dual_heatmap(df, category, output_dir / f'{category}_heatmaps.png')
    
    # Individual heatmaps
    create_single_heatmap(df, category, 'SSIM', output_dir / f'{category}_ssim_heatmap.png')
    create_single_heatmap(df, category, 'LLM_Composite', output_dir / f'{category}_llm_heatmap.png')
    
    # Bar charts
    create_bar_chart(df, category, 'SSIM', output_dir / f'{category}_ssim_bar.png')
    create_bar_chart(df, category, 'LLM_Composite', output_dir / f'{category}_llm_bar.png')
    
    # Radar charts
    create_radar_chart(df, category, 'SSIM', output_dir / f'{category}_ssim_radar.png')
    create_radar_chart(df, category, 'LLM_Composite', output_dir / f'{category}_llm_radar.png')
    
    # Winner pies
    create_winner_pie(df, category, 'SSIM', output_dir / f'{category}_ssim_winners.png')
    create_winner_pie(df, category, 'LLM_Composite', output_dir / f'{category}_llm_winners.png')
    
    # Special: Trend charts for ordered categories
    if category == 'scope':
        create_trend_chart(df, category, 'SSIM', output_dir / f'{category}_ssim_trend.png',
                          view_order=['part', 'entire', 'entire+'],
                          x_labels=['Part', 'Entire', 'Entire+'])
        create_trend_chart(df, category, 'LLM_Composite', output_dir / f'{category}_llm_trend.png',
                          view_order=['part', 'entire', 'entire+'],
                          x_labels=['Part', 'Entire', 'Entire+'])
    
    if category == 'granularity':
        create_trend_chart(df, category, 'SSIM', output_dir / f'{category}_ssim_trend.png',
                          view_order=['low', 'medium', 'high'],
                          x_labels=['Low', 'Medium', 'High'])
        create_trend_chart(df, category, 'LLM_Composite', output_dir / f'{category}_llm_trend.png',
                          view_order=['low', 'medium', 'high'],
                          x_labels=['Low', 'Medium', 'High'])


# =============================================================================
# MAIN
# =============================================================================
def main(data_dir: str):
    """Generate all clean plots."""
    
    data_path = Path(data_dir)
    
    print("="*60)
    print("CLEAN PLOT GENERATOR")
    print("Few-shot (Blue) | Agent (Red) | ArchView (Green)")
    print("="*60)
    
    df = load_data(data_path)
    
    print(f"\nLoaded {len(df)} rows")
    print(f"Categories: {df['Category'].unique().tolist()}")
    
    # Generate plots for each category
    for category in ['notation', 'concern', 'qas', 'scope', 'granularity']:
        if category in df['Category'].unique():
            generate_category_plots(df, category)
    
    print(f"\n{'='*60}")
    print(f"ALL PLOTS SAVED TO: {OUTPUT_DIR.absolute()}")
    print("="*60)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Usage: python clean_heatmap_generator.py <data_directory>")
        print("\nExample: python clean_heatmap_generator.py .")