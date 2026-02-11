"""
Publication-Quality Heatmap Generator
======================================

- Large, readable fonts (publication-ready)
- Professional color scheme
- Clean, crisp 300 DPI outputs
- ArchView instead of Approach
- Red (Agent), Blue (Few-shot), Green (ArchView)
- NO unnecessary titles
- Combined plots for comprehensive analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# PUBLICATION-QUALITY SETTINGS
# =============================================================================

# Set matplotlib defaults for publication quality
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 14
plt.rcParams['axes.linewidth'] = 2
plt.rcParams['xtick.major.width'] = 1.5
plt.rcParams['ytick.major.width'] = 1.5
plt.rcParams['xtick.major.size'] = 6
plt.rcParams['ytick.major.size'] = 6

# Output directory
OUTPUT_DIR = Path("./publication_plots")
OUTPUT_DIR.mkdir(exist_ok=True)

# =============================================================================
# PROFESSIONAL COLOR SCHEME
# =============================================================================

STRATEGIES = ['fewshot_claude', 'agent_claude', 'approach_claude']

# Column labels (what appears in the heatmap)
STRATEGY_LABELS = ['Few-Shot(FS)', 'Agent (GPA)', 'ArchView (AV)']

# Professional, distinguishable colors
COLORS = {
    'fewshot_claude': '#5DA5DA',   # Blue
    'agent_claude': '#F15854',      # Red  
    'approach_claude': '#60BD68'    # Green
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
# COMBINED METRIC PLOTS - PUBLICATION QUALITY
# =============================================================================
def create_combined_metric_plot(df: pd.DataFrame, category: str, output_file: Path):
    """
    Create combined plot showing both SSIM and LLM Quality.
    Publication-ready with large fonts and clear styling.
    """
    cat_df = df[df['Category'] == category]
    label_map = get_label_map(category)
    views = sorted(cat_df['View'].unique())
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Left: SSIM comparison
    ax1 = axes[0]
    x = np.arange(len(views))
    width = 0.25
    
    for i, (strategy, label, color) in enumerate(zip(STRATEGIES, STRATEGY_LABELS, 
                                                      [COLORS[s] for s in STRATEGIES])):
        ssim_means = [cat_df[(cat_df['Strategy'] == strategy) & (cat_df['View'] == v)]['SSIM'].mean() 
                     for v in views]
        ax1.bar(x + i*width, ssim_means, width, label=label, color=color, alpha=0.8,
               edgecolor='white', linewidth=1.5)
    
    clean_labels = [label_map.get(v, v) for v in views]
    ax1.set_ylabel('SSIM', fontsize=18, fontweight='bold')
    ax1.set_xticks(x + width)
    ax1.set_xticklabels(clean_labels, fontsize=14, rotation=45, ha='right')
    ax1.legend(fontsize=14, framealpha=0.95, loc='upper left', edgecolor='black', fancybox=False)
    ax1.grid(axis='y', alpha=0.25, linestyle='--', linewidth=1.5)
    ax1.set_axisbelow(True)
    ax1.tick_params(axis='both', labelsize=14, width=1.5, length=6)
    
    for spine in ax1.spines.values():
        spine.set_linewidth(2)
        spine.set_color('black')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    
    # Right: LLM Quality comparison
    ax2 = axes[1]
    for i, (strategy, label, color) in enumerate(zip(STRATEGIES, STRATEGY_LABELS, 
                                                      [COLORS[s] for s in STRATEGIES])):
        llm_means = [cat_df[(cat_df['Strategy'] == strategy) & (cat_df['View'] == v)]['LLM_Composite'].mean() 
                    for v in views]
        ax2.bar(x + i*width, llm_means, width, label=label, color=color, alpha=0.8,
               edgecolor='white', linewidth=1.5)
    
    ax2.set_ylabel('LLM Quality', fontsize=18, fontweight='bold')
    ax2.set_xticks(x + width)
    ax2.set_xticklabels(clean_labels, fontsize=14, rotation=45, ha='right')
    ax2.legend(fontsize=14, framealpha=0.95, loc='upper left', edgecolor='black', fancybox=False)
    ax2.grid(axis='y', alpha=0.25, linestyle='--', linewidth=1.5)
    ax2.set_axisbelow(True)
    ax2.tick_params(axis='both', labelsize=14, width=1.5, length=6)
    
    for spine in ax2.spines.values():
        spine.set_linewidth(2)
        spine.set_color('black')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.savefig(output_file.with_suffix('.pdf'), format='pdf', bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    print(f"✓ {output_file.name}")


def create_combined_scatter_plot(df: pd.DataFrame, category: str, output_file: Path):
    """
    Create scatter plot showing SSIM vs LLM Quality relationship.
    Publication-ready styling.
    """
    cat_df = df[df['Category'] == category]
    label_map = get_label_map(category)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    for strategy, label, color in zip(STRATEGIES, STRATEGY_LABELS, [COLORS[s] for s in STRATEGIES]):
        strat_df = cat_df[cat_df['Strategy'] == strategy]
        
        # Group by view and get means
        view_means = strat_df.groupby('View')[['SSIM', 'LLM_Composite']].mean()
        
        ax.scatter(view_means['SSIM'], view_means['LLM_Composite'], 
                  s=250, alpha=0.75, color=color, label=label, 
                  edgecolors='white', linewidth=2.5)
        
        # Add view labels
        for view, row in view_means.iterrows():
            clean_view = label_map.get(view, view)
            ax.annotate(clean_view[:12], (row['SSIM'], row['LLM_Composite']),
                       fontsize=9, ha='center', va='bottom', fontweight='bold')
    
    ax.set_xlabel('SSIM', fontsize=18, fontweight='bold')
    ax.set_ylabel('LLM Quality', fontsize=18, fontweight='bold')
    ax.legend(fontsize=15, framealpha=0.95, edgecolor='black', fancybox=False)
    ax.grid(alpha=0.25, linestyle='--', linewidth=1.5)
    ax.tick_params(axis='both', labelsize=14, width=1.5, length=6)
    
    for spine in ax.spines.values():
        spine.set_linewidth(2)
        spine.set_color('black')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.savefig(output_file.with_suffix('.pdf'), format='pdf', bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    print(f"✓ {output_file.name}")


def create_combined_dual_radar(df: pd.DataFrame, category: str, output_file: Path):
    """
    Create dual radar chart: SSIM on left, LLM Quality on right.
    Publication-quality with large fonts.
    """
    cat_df = df[df['Category'] == category]
    label_map = get_label_map(category)
    views = sorted(cat_df['View'].unique())
    
    if len(views) < 3:
        print(f"  ⊘ Skipping dual radar for {category} (< 3 views)")
        return
    
    angles = np.linspace(0, 2*np.pi, len(views), endpoint=False).tolist()
    angles += angles[:1]
    
    fig, axes = plt.subplots(1, 2, figsize=(18, 8), subplot_kw=dict(polar=True))
    
    # Left: SSIM
    ax1 = axes[0]
    for strategy, label, color in zip(STRATEGIES, STRATEGY_LABELS, [COLORS[s] for s in STRATEGIES]):
        values = [cat_df[(cat_df['Strategy'] == strategy) & (cat_df['View'] == v)]['SSIM'].mean() 
                 for v in views]
        values += values[:1]
        ax1.plot(angles, values, 'o-', linewidth=3.5, label=label, color=color, markersize=8)
        ax1.fill(angles, values, alpha=0.15, color=color)
    
    clean_labels = [label_map.get(v, v)[:18] for v in views]
    ax1.set_xticks(angles[:-1])
    ax1.set_xticklabels(clean_labels, fontsize=13)
    ax1.set_title('SSIM', fontsize=18, fontweight='bold', pad=25)
    ax1.legend(loc='upper right', bbox_to_anchor=(1.25, 1.05), fontsize=14, 
              framealpha=0.95, edgecolor='black', fancybox=False)
    ax1.grid(True, alpha=0.3, linewidth=1.5)
    ax1.tick_params(axis='y', labelsize=12)
    
    # Right: LLM Quality
    ax2 = axes[1]
    for strategy, label, color in zip(STRATEGIES, STRATEGY_LABELS, [COLORS[s] for s in STRATEGIES]):
        values = [cat_df[(cat_df['Strategy'] == strategy) & (cat_df['View'] == v)]['LLM_Composite'].mean() 
                 for v in views]
        values += values[:1]
        ax2.plot(angles, values, 'o-', linewidth=3.5, label=label, color=color, markersize=8)
        ax2.fill(angles, values, alpha=0.15, color=color)
    
    ax2.set_xticks(angles[:-1])
    ax2.set_xticklabels(clean_labels, fontsize=13)
    ax2.set_title('LLM Quality', fontsize=18, fontweight='bold', pad=25)
    ax2.legend(loc='upper right', bbox_to_anchor=(1.25, 1.05), fontsize=14, 
              framealpha=0.95, edgecolor='black', fancybox=False)
    ax2.grid(True, alpha=0.3, linewidth=1.5)
    ax2.tick_params(axis='y', labelsize=12)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.savefig(output_file.with_suffix('.pdf'), format='pdf', bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    print(f"✓ {output_file.name}")

# =============================================================================
# HEATMAP - PUBLICATION QUALITY
# =============================================================================
def create_single_heatmap(df: pd.DataFrame, category: str, metric: str, output_file: Path):
    """
    Create a single publication-quality heatmap.
    Large fonts, clear labels, professional styling.
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
    fig_height = max(5, n_rows * 0.7)
    fig_width = 7
    
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    
    # Create heatmap with publication settings
    sns.heatmap(
        pivot,
        annot=True,
        fmt='.3f',
        cmap='RdYlGn',
        center=pivot.values.mean(),
        annot_kws={'size': 15, 'fontweight': 'bold'},
        linewidths=2.5,
        linecolor='white',
        cbar_kws={'label': metric, 'shrink': 0.8},
        square=False,
        ax=ax
    )
    
    # Clean up axes
    ax.set_xlabel('')
    ax.set_ylabel('')
    
    # Style the tick labels - LARGER FONTS
    ax.set_xticklabels(STRATEGY_LABELS, fontsize=16, fontweight='bold', rotation=0)
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=14, rotation=0)
    
    # Adjust colorbar label
    cbar = ax.collections[0].colorbar
    cbar.ax.set_ylabel(metric, fontsize=16, fontweight='bold')
    cbar.ax.tick_params(labelsize=13)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.savefig(output_file.with_suffix('.pdf'), format='pdf', bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    print(f"✓ {output_file.name}")


def create_dual_heatmap(df: pd.DataFrame, category: str, output_file: Path):
    """
    Create side-by-side heatmaps for SSIM and LLM Quality.
    Publication-quality with large fonts.
    """
    cat_df = df[df['Category'] == category]
    label_map = get_label_map(category)
    
    n_rows = len(cat_df['View'].unique())
    fig_height = max(5, n_rows * 0.7)
    fig, axes = plt.subplots(1, 2, figsize=(15, fig_height))
    
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
            annot_kws={'size': 14, 'fontweight': 'bold'},
            linewidths=2.5,
            linecolor='white',
            cbar_kws={'label': cbar_label, 'shrink': 0.8},
            ax=ax
        )
        
        # NO title, NO axis labels
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.set_xticklabels(STRATEGY_LABELS, fontsize=15, fontweight='bold', rotation=0)
        ax.set_yticklabels(ax.get_yticklabels(), fontsize=13, rotation=0)
        
        # Colorbar styling
        cbar = ax.collections[0].colorbar
        cbar.ax.set_ylabel(cbar_label, fontsize=15, fontweight='bold')
        cbar.ax.tick_params(labelsize=12)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.savefig(output_file.with_suffix('.pdf'), format='pdf', bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    print(f"✓ {output_file.name}")


# =============================================================================
# BAR CHART - PUBLICATION QUALITY
# =============================================================================
def create_bar_chart(df: pd.DataFrame, category: str, metric: str, output_file: Path):
    """
    Create publication-quality grouped bar chart.
    """
    cat_df = df[df['Category'] == category]
    label_map = get_label_map(category)
    views = sorted(cat_df['View'].unique())
    
    fig, ax = plt.subplots(figsize=(max(10, len(views) * 1.5), 6))
    
    x = np.arange(len(views))
    width = 0.25
    
    for i, (strategy, label, color) in enumerate(zip(STRATEGIES, STRATEGY_LABELS, 
                                                      [COLORS[s] for s in STRATEGIES])):
        means = [cat_df[(cat_df['Strategy'] == strategy) & (cat_df['View'] == v)][metric].mean() 
                for v in views]
        ax.bar(x + i*width, means, width, label=label, color=color, alpha=0.8,
              edgecolor='white', linewidth=1.5)
    
    # Clean labels
    clean_labels = [label_map.get(v, v) for v in views]
    
    ax.set_ylabel("LLM Quality", fontsize=18, fontweight='bold')
    ax.set_xticks(x + width)
    ax.set_xticklabels(clean_labels, fontsize=15, rotation=45, ha='right')
    # 
    ax.legend(
    loc="upper center", 
    bbox_to_anchor=(0.5, 1.15),  # 0.5 = horizontal center, 1.15 = move up vertically
    fontsize=14,  
    ncol=3, 
    frameon=False, 
    fancybox=False
)
    ax.grid(axis='y', alpha=0.25, linestyle='--', linewidth=1.5)
    ax.set_axisbelow(True)
    ax.tick_params(axis='both', labelsize=18, width=1.5, length=6)
    
    for spine in ax.spines.values():
        spine.set_linewidth(2)
        spine.set_color('black')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.savefig(output_file.with_suffix('.pdf'), format='pdf', bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    print(f"✓ {output_file.name}")


# =============================================================================
# RADAR CHART - PUBLICATION QUALITY
# =============================================================================
def create_radar_chart(df: pd.DataFrame, category: str, metric: str, output_file: Path):
    """
    Create publication-quality radar chart.
    """
    cat_df = df[df['Category'] == category]
    label_map = get_label_map(category)
    views = sorted(cat_df['View'].unique())
    
    if len(views) < 3:
        print(f"  ⊘ Skipping radar for {category} (< 3 views)")
        return
    
    angles = np.linspace(0, 2*np.pi, len(views), endpoint=False).tolist()
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    
    for strategy, label, color in zip(STRATEGIES, STRATEGY_LABELS, [COLORS[s] for s in STRATEGIES]):
        values = [cat_df[(cat_df['Strategy'] == strategy) & (cat_df['View'] == v)][metric].mean() 
                 for v in views]
        values += values[:1]
        ax.plot(angles, values, 'o-', linewidth=3.5, label=label, color=color, markersize=8)
        ax.fill(angles, values, alpha=0.15, color=color)
    
    # Clean labels (shortened if needed)
    clean_labels = [label_map.get(v, v)[:18] for v in views]
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(clean_labels, fontsize=13)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.05), fontsize=14,
             framealpha=0.95, edgecolor='black', fancybox=False)
    ax.grid(True, alpha=0.3, linewidth=1.5)
    ax.tick_params(axis='y', labelsize=12)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.savefig(output_file.with_suffix('.pdf'), format='pdf', bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    print(f"✓ {output_file.name}")


# =============================================================================
# WINNER PIE CHART - PUBLICATION QUALITY
# =============================================================================
def create_winner_pie(df: pd.DataFrame, category: str, metric: str, output_file: Path):
    """
    Create publication-quality pie chart showing which strategy wins most.
    """
    cat_df = df[df['Category'] == category]
    
    pivot = cat_df.pivot_table(index='View', columns='Strategy', values=metric, aggfunc='mean')
    pivot = pivot[STRATEGIES].dropna()
    
    if len(pivot) == 0:
        return
    
    winners = pivot.idxmax(axis=1)
    winner_counts = winners.value_counts()
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    colors = [COLORS[s] for s in winner_counts.index]
    labels = [STRATEGY_LABELS[STRATEGIES.index(s)] for s in winner_counts.index]
    
    wedges, texts, autotexts = ax.pie(
        winner_counts.values,
        labels=labels,
        autopct='%1.1f%%',
        colors=colors,
        startangle=90,
        textprops={'fontsize': 15, 'fontweight': 'bold'},
        wedgeprops={'edgecolor': 'white', 'linewidth': 3}
    )
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(14)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.savefig(output_file.with_suffix('.pdf'), format='pdf', bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    print(f"✓ {output_file.name}")

# =============================================================================
# COMBINED TREND PLOT - UPDATED (FIXED LEGEND)
# =============================================================================
def create_combined_trend_plot(df: pd.DataFrame, category: str, output_file: Path,
                               view_order: list = None, x_labels: list = None):
    """
    Create combined trend plot: SSIM and LLM Quality on same chart with dual y-axes.
    LEGEND FIX: Placed above the plot to prevent overlapping.
    """
    cat_df = df[df['Category'] == category]
    
    if view_order:
        views = [v for v in view_order if v in cat_df['View'].unique()]
    else:
        views = sorted(cat_df['View'].unique())
    
    if len(views) < 2:
        return
    
    # Increase figure height slightly to accommodate the top legend
    fig, ax1 = plt.subplots(figsize=(12, 8))
    
    # SSIM on left y-axis
    lines = []
    labels = []
    
    for strategy, label, color in zip(STRATEGIES, STRATEGY_LABELS, [COLORS[s] for s in STRATEGIES]):
        ssim_values = [cat_df[(cat_df['Strategy'] == strategy) & (cat_df['View'] == v)]['SSIM'].mean() 
                      for v in views]
        l, = ax1.plot(range(len(views)), ssim_values, 'o-', linewidth=3.5, markersize=12,
                label=f'{label} (SSIM)', color=color, linestyle='-')
        lines.append(l)
        labels.append(f'{label} (SSIM)')
    
    ax1.set_xlabel('', fontsize=16, fontweight='bold')
    ax1.set_ylabel('SSIM', fontsize=20, fontweight='bold', color='black')
    ax1.tick_params(axis='y', labelcolor='black', labelsize=14, width=1.5, length=6)
    ax1.tick_params(axis='x', labelsize=15, width=1.5, length=6)
    ax1.grid(alpha=0.25, linestyle='--', linewidth=1.5)
    
    # LLM Quality on right y-axis
    ax2 = ax1.twinx()
    for strategy, label, color in zip(STRATEGIES, STRATEGY_LABELS, [COLORS[s] for s in STRATEGIES]):
        llm_values = [cat_df[(cat_df['Strategy'] == strategy) & (cat_df['View'] == v)]['LLM_Composite'].mean() 
                     for v in views]
        l, = ax2.plot(range(len(views)), llm_values, 's--', linewidth=3, markersize=10,
                label=f'{label} (LLM)', color=color, alpha=0.65, linestyle='--')
        lines.append(l)
        labels.append(f'{label} (LLM)')
    
    ax2.set_ylabel('LLM Quality', fontsize=18, fontweight='bold', color='black')
    ax2.tick_params(axis='y', labelcolor='black', labelsize=14, width=1.5, length=6)
    
    # X-axis labels
    ax1.set_xticks(range(len(views)))
    ax1.set_xticklabels(x_labels if x_labels else views, fontsize=15, fontweight='bold')
    
    # --- LEGEND FIX ---
    # Place legend ABOVE the plot (bbox_to_anchor)
    # ncol=3 spreads it out horizontally
    ax1.legend(lines, labels, 
              loc='upper center', 
              bbox_to_anchor=(0.5, 1.08),  # Push up above plot
              ncol=3,                      # 3 columns = neater layout
              fontsize=16,                 # Bigger font
              frameon=False,               # Clean look (no box)
              handletextpad=0.5,
              columnspacing=1.5)
    # ax1.legend(loc='upper center', 
    #           bbox_to_anchor=(0.5, -0.12),  # Move down below X-axis
    #           ncol=3,                       # Horizontal layout
    #           frameon=False,                # Clean look (no box)
    #           prop={'weight': 'bold', 'size': 18}) # BIGGER & BOLDER
    
    # ax1.grid(alpha=0.25, linestyle='--', linewidth=1.5)
    # ax1.tick_params(axis='both', labelsize=14, width=1.5, length=6)
    for spine in ax1.spines.values():
        spine.set_linewidth(2)
        spine.set_color('black')
    for spine in ax2.spines.values():
        spine.set_linewidth(2)
        spine.set_color('black')
    ax1.spines['top'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.savefig(output_file.with_suffix('.pdf'), format='pdf', bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    print(f"✓ {output_file.name}")


# =============================================================================
# SINGLE TREND CHART - UPDATED (FIXED LEGEND)
# =============================================================================
def create_trend_chart(df: pd.DataFrame, category: str, metric: str, output_file: Path, 
                       view_order: list = None, x_labels: list = None):
    """
    Create publication-quality trend line chart.
    LEGEND UPDATE: Placed BELOW the plot, BIGGER, and BOLDER.
    """
    cat_df = df[df['Category'] == category]
    
    if view_order:
        views = [v for v in view_order if v in cat_df['View'].unique()]
    else:
        views = sorted(cat_df['View'].unique())
    
    if len(views) < 2:
        return
    
    # Increase height slightly to make room for bottom legend
    fig, ax = plt.subplots(figsize=(10, 7.5)) 
    
    for strategy, label, color in zip(STRATEGIES, STRATEGY_LABELS, [COLORS[s] for s in STRATEGIES]):
        values = [cat_df[(cat_df['Strategy'] == strategy) & (cat_df['View'] == v)][metric].mean() 
                 for v in views]
        ax.plot(range(len(views)), values, 'o-', linewidth=3.5, markersize=12,
               label=label, color=color)
    
    ax.set_ylabel(metric, fontsize=18, fontweight='bold')
    ax.set_xticks(range(len(views)))
    ax.set_xticklabels(x_labels if x_labels else views, fontsize=15, fontweight='bold')
    
    # --- LEGEND FIX: DOWN, BIGGER, BOLDER ---
    # bbox_to_anchor=(0.5, -0.15) places it below the x-axis
    # prop={'weight': 'bold', 'size': 18} makes text bold and large
    ax.legend(loc='upper center', 
              bbox_to_anchor=(0.5, -0.12),  # Move down below X-axis
              ncol=3,                       # Horizontal layout
              frameon=False,                # Clean look (no box)
              prop={'weight': 'bold', 'size': 18}) # BIGGER & BOLDER
    
    ax.grid(alpha=0.25, linestyle='--', linewidth=1.5)
    ax.tick_params(axis='both', labelsize=14, width=1.5, length=6)
    
    for spine in ax.spines.values():
        spine.set_linewidth(2)
        spine.set_color('black')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Adjust layout to ensure the bottom legend isn't cut off
    plt.tight_layout()
    
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.savefig(output_file.with_suffix('.pdf'), format='pdf', bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    print(f"✓ {output_file.name}")
# =============================================================================
# TREND LINE CHART - PUBLICATION QUALITY
# =============================================================================

# =============================================================================
# GENERATE ALL PLOTS FOR A CATEGORY
# =============================================================================
def generate_category_plots(df: pd.DataFrame, category: str):
    """Generate all publication-quality plots for a category."""
    
    output_dir = OUTPUT_DIR / category
    output_dir.mkdir(exist_ok=True)
    
    print(f"\n{'='*60}")
    print(f"  {category.upper()}")
    print(f"{'='*60}")
    
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
    
    # Combined metric plots
    print(f"  → Combined plots...")
    create_combined_metric_plot(df, category, output_dir / f'{category}_combined_bars.png')
    create_combined_scatter_plot(df, category, output_dir / f'{category}_combined_scatter.png')
    create_combined_dual_radar(df, category, output_dir / f'{category}_combined_radar.png')
    
    # Special: Trend charts for ordered categories
    if category == 'scope':
        create_trend_chart(df, category, 'SSIM', output_dir / f'{category}_ssim_trend.png',
                          view_order=['part', 'entire', 'entire+'],
                          x_labels=['Part', 'Entire', 'Entire+'])
        create_trend_chart(df, category, 'LLM_Composite', output_dir / f'{category}_llm_trend.png',
                          view_order=['part', 'entire', 'entire+'],
                          x_labels=['Part', 'Entire', 'Entire+'])
        create_combined_trend_plot(df, category, output_dir / f'{category}_combined_trend.png',
                                  view_order=['part', 'entire', 'entire+'],
                                  x_labels=['Part', 'Entire', 'Entire+'])
    
    if category == 'granularity':
        create_trend_chart(df, category, 'SSIM', output_dir / f'{category}_ssim_trend.png',
                          view_order=['low', 'medium', 'high'],
                          x_labels=['Low', 'Medium', 'High'])
        create_trend_chart(df, category, 'LLM_Composite', output_dir / f'{category}_llm_trend.png',
                          view_order=['low', 'medium', 'high'],
                          x_labels=['Low', 'Medium', 'High'])
        create_combined_trend_plot(df, category, output_dir / f'{category}_combined_trend.png',
                                  view_order=['low', 'medium', 'high'],
                                  x_labels=['Low', 'Medium', 'High'])


# =============================================================================
# MAIN
# =============================================================================
def main(data_dir: str):
    """Generate all publication-quality plots."""
    
    data_path = Path(data_dir)
    
    print("="*70)
    print("  PUBLICATION-QUALITY PLOT GENERATOR (300 DPI)")
    print("  Few-Shot (Blue) | Agent (Red) | ArchView (Green)")
    print("="*70)
    
    df = load_data(data_path)
    
    print(f"\n📊 Loaded {len(df)} rows")
    print(f"📁 Categories: {df['Category'].unique().tolist()}")
    
    # Generate plots for each category
    for category in ['notation', 'concern', 'qas', 'scope', 'granularity']:
        if category in df['Category'].unique():
            generate_category_plots(df, category)
    
    print(f"\n{'='*70}")
    print(f"✅ ALL PLOTS SAVED TO: {OUTPUT_DIR.absolute()}")
    print(f"📄 Both PNG (300 DPI) and PDF (vector) versions created")
    print("="*70)
    print("\n💡 Recommendation: Use PDF files for paper submission!")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Usage: python publication_heatmap_generator.py <data_directory>")
        print("\nExample: python publication_heatmap_generator.py .")