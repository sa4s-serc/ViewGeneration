import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.stats import mannwhitneyu
import warnings
warnings.filterwarnings('ignore')

# Set publication-quality defaults
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 14
plt.rcParams['axes.linewidth'] = 1.5
plt.rcParams['xtick.major.width'] = 1.5
plt.rcParams['ytick.major.width'] = 1.5

# Professional, distinguishable color palette
STRATEGY_COLORS = { 
    'few-shot': '#5DA5DA',   # Blue
    'agent': '#F15854',      # Red
    'approach': '#60BD68'    # Green
}

STRATEGY_LABELS = {
    'few-shot': 'Few-Shot(FS)',
    'agent': 'Agent (GPA)',
    'approach': 'ArchView (AV)'
}


def load_and_filter_data(data_dir: Path) -> pd.DataFrame:
    rows = []
    for f in data_dir.glob("simple_table_*.csv"):
        name = f.stem.replace("simple_table_", "")
        df = pd.read_csv(f)

        # Category parsing
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
                continue

            # Base model
            if 'claude' in model_name:
                base_model = 'Claude'
            elif 'deepseek' in model_name:
                base_model = 'DeepSeek'
            elif 'gpt' in model_name:
                base_model = 'GPT'
            else:
                continue

            # LLM scoring
            scores = {}
            for aspect in ['Clarity', 'Completeness', 'Consistency']:
                m = f'LLM_{aspect}_Rating_Meets'
                p = f'LLM_{aspect}_Rating_PartiallyMeets'
                d = f'LLM_{aspect}_Rating_DoesNotMeet'
                if all(c in row.index for c in [m, p, d]):
                    total = row[m] + row[p] + row[d]
                    if total > 0:
                        scores[aspect] = (2*row[m] + row[p]) / (2 * total)

            rows.append({
                'Setting': row['Model'].lower(),
                'Strategy': strategy,
                'Base_Model': base_model,
                'Category': category,
                'View': view,
                'SSIM': row.get('SSIM', np.nan),
                'Clarity': scores.get('Clarity', np.nan),
                'Completeness': scores.get('Completeness', np.nan),
                'Consistency': scores.get('Consistency', np.nan),
            })

    return pd.DataFrame(rows)


def plot_4_metrics_publication_quality(df: pd.DataFrame, 
                                       output_png: str = 'metrics_comparison_hq.png',
                                       dpi: int = 300):
    
    # Create figure with proper sizing for publications (inches)
    # Typical two-column width: 7 inches, single column: 3.5 inches
    fig, axes = plt.subplots(2, 2, figsize=(14, 11))
    axes = axes.flatten()

    metrics = ['SSIM', 'Clarity', 'Completeness', 'Consistency']
    strategies = ['few-shot', 'agent', 'approach']

    for ax, metric in zip(axes, metrics):
        if metric not in df.columns or df[metric].isna().all():
            ax.set_visible(False)
            continue

        data_to_plot = [df[df['Strategy'] == s][metric].dropna() for s in strategies]

        # Create boxplot with custom styling
        bp = ax.boxplot(
            data_to_plot,
            labels=[STRATEGY_LABELS[s] for s in strategies],
            patch_artist=True,
            widths=0.6,
            showfliers=True,
            boxprops=dict(linewidth=2),
            whiskerprops=dict(linewidth=2),
            capprops=dict(linewidth=2),
            medianprops=dict(linewidth=2.5, color='black'),
            flierprops=dict(marker='o', markersize=6, linestyle='none', 
                          markeredgewidth=1, markeredgecolor='black', alpha=0.5)
        )

        # Apply colors to boxes
        for patch, s in zip(bp['boxes'], strategies):
            patch.set_facecolor(STRATEGY_COLORS[s])
            patch.set_alpha(0.7)
            patch.set_edgecolor(STRATEGY_COLORS[s])

        # Add mean markers (black diamonds)
        means = [d.mean() if len(d) > 0 else 0 for d in data_to_plot]
        ax.scatter([1, 2, 3], means, 
                  color='black', 
                  marker='D', 
                  s=100, 
                  zorder=10,
                  edgecolors='white',
                  linewidths=1.5)

        # Statistical significance
        # y_values = [val for data in data_to_plot for val in data if not np.isnan(val)]
        # if y_values:
        #     y_max = max(y_values)
        #     y_min = min(y_values)
        #     y_range = y_max - y_min
        #     y_step = y_range * 0.12

        #     line_count = 0
        #     comparisons = [(0, 1), (0, 2), (1, 2)]
            
        #     for s1_idx, s2_idx in comparisons:
        #         if len(data_to_plot[s1_idx]) > 0 and len(data_to_plot[s2_idx]) > 0:
        #             _, p = mannwhitneyu(data_to_plot[s1_idx], data_to_plot[s2_idx], 
        #                                alternative='two-sided')
        #             if p < 0.05:
        #                 line_count += 1
        #                 y_pos = y_max + y_step * line_count
                        
        #                 # Draw significance line
        #                 ax.plot([s1_idx + 1, s2_idx + 1], [y_pos, y_pos], 
        #                        'k-', linewidth=2)
                        
        #                 # Add significance stars
        #                 sig = '***' if p < 0.001 else '**' if p < 0.01 else '*'
        #                 ax.text((s1_idx + s2_idx + 2) / 2, y_pos, sig,
        #                        ha='center', va='bottom', fontsize=18, fontweight='bold')

        # Styling
        ax.set_title(metric, fontsize=20, fontweight='bold', pad=15)
        ax.set_ylabel(metric, fontsize=18, fontweight='bold')
        ax.tick_params(axis='both', which='major', labelsize=16, width=1.5, length=6)
        
        # Grid
        ax.yaxis.grid(True, linestyle='--', alpha=0.3, linewidth=1)
        ax.set_axisbelow(True)
        
        # Spines
        for spine in ax.spines.values():
            spine.set_linewidth(1.5)
            spine.set_color('black')

    plt.tight_layout(pad=3.0)
    
    # Save with high DPI
    plt.savefig(output_png, dpi=dpi, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    print(f"✓ Saved high-resolution PNG ({dpi} DPI): {output_png}")
    
    # Also save as PDF (vector format - best for papers)
    output_pdf = output_png.replace('.png', '.pdf')
    plt.savefig(output_pdf, format='pdf', bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print(f"✓ Saved vector PDF (best for papers): {output_pdf}")
    
    # Save as SVG too
    output_svg = output_png.replace('.png', '.svg')
    plt.savefig(output_svg, format='svg', bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print(f"✓ Saved vector SVG: {output_svg}")
    
    plt.close()


# Main
if __name__ == "__main__":
    import sys
    data_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    
    print("=" * 70)
    print("  PUBLICATION-READY METRICS COMPARISON (300 DPI)")
    print("=" * 70)
    print("\n📊 Loading data...")
    df = load_and_filter_data(data_dir)
    print(f"   Loaded {len(df)} rows")
    
    print("\n🎨 Generating publication-quality figure...")
    plot_4_metrics_publication_quality(df, dpi=300)
    
    print("\n✅ Done! Your publication-ready figures are ready.")
    print("\nFiles generated:")
    print("  • metrics_comparison_hq.png (300 DPI, for viewing)")
    print("  • metrics_comparison_hq.pdf (vector, for paper submission)")
    print("  • metrics_comparison_hq.svg (vector, alternative format)")
    print("\nRecommendation: Use the PDF version for your paper!")
    print("=" * 70)