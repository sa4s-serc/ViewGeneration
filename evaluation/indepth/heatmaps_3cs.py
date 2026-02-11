"""
LLM Quality Rating Heatmaps: Does Not Meet Criteria
====================================================

Creates heatmaps showing the COUNT of "Does Not Meet" ratings for:
- Clarity
- Completeness  
- Consistency

Across all experimental settings (12) and view categories.
Lower counts = better (fewer failures)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-whitegrid')
OUTPUT_DIR = Path("./analysis_llm_ratings")
OUTPUT_DIR.mkdir(exist_ok=True)


def load_all_data(data_dir: Path) -> pd.DataFrame:
    """Load all simple_table CSVs and combine into one dataframe."""
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
            row_data = {
                'Setting': row['Model'],
                'Category': category,
                'View': view,
                'Category_View': f"{category}:{view}",
            }
            
            # Extract all LLM ratings
            for aspect in ['Clarity', 'Completeness', 'Consistency']:
                for rating in ['DoesNotMeet', 'Meets', 'PartiallyMeets']:
                    col = f'LLM_{aspect}_Rating_{rating}'
                    if col in row.index:
                        row_data[f'{aspect}_{rating}'] = row[col]
            
            # Also get SSIM for reference
            if 'SSIM' in row.index:
                row_data['SSIM'] = row['SSIM']
            
            rows.append(row_data)
    
    return pd.DataFrame(rows)


def create_doesnotmeet_heatmap_by_category(df: pd.DataFrame, aspect: str):
    """
    Create heatmap: Settings (rows) × Category_View (columns)
    Values = Count of DoesNotMeet
    """
    col = f'{aspect}_DoesNotMeet'
    
    if col not in df.columns:
        print(f"Column {col} not found!")
        return
    
    # Pivot: rows = Setting, columns = Category_View
    pivot = df.pivot_table(index='Setting', columns='Category_View', values=col, aggfunc='sum')
    
    # Sort settings logically
    setting_order = [
        'zeroshot_claude', 'zeroshot_gpt', 'zero_shot_deepseek',
        '1shot_claude', '1shot_gpt', '1shot_deepseek',
        'fewshot_claude', 'fewshot_gpt', 'fewshot_deepseek',
        'approach_claude', 'approach_gpt', 'approach_deepseek',
        'Agent_claude'
    ]
    # Match case-insensitively
    available_settings = pivot.index.tolist()
    ordered_settings = []
    for s in setting_order:
        for avail in available_settings:
            if avail.lower() == s.lower():
                ordered_settings.append(avail)
                break
    # Add any remaining
    for avail in available_settings:
        if avail not in ordered_settings:
            ordered_settings.append(avail)
    
    pivot = pivot.reindex(ordered_settings)
    
    # Sort columns by category
    col_order = sorted(pivot.columns, key=lambda x: (x.split(':')[0], x.split(':')[1]))
    pivot = pivot[col_order]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(22, 12))
    
    # Use reverse colormap (lower = better = green, higher = worse = red)
    sns.heatmap(pivot, annot=True, fmt='.0f', cmap='RdYlGn_r', ax=ax,
                cbar_kws={'label': f'{aspect} - Does Not Meet Count'},
                annot_kws={'size': 8}, linewidths=0.5)
    
    ax.set_title(f'{aspect}: "Does Not Meet" Counts by Setting × View\n'
                 f'(Lower = Better, Green = Good, Red = Bad)', 
                 fontsize=14, fontweight='bold')
    ax.set_xlabel('View Type (Category:Name)', fontsize=11)
    ax.set_ylabel('Experimental Setting', fontsize=11)
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.yticks(fontsize=9)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f'heatmap_{aspect.lower()}_doesnotmeet_by_view.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: heatmap_{aspect.lower()}_doesnotmeet_by_view.png")


def create_doesnotmeet_heatmap_by_category_aggregated(df: pd.DataFrame, aspect: str):
    """
    Create heatmap: Settings (rows) × Category (columns) - aggregated
    Values = Total Count of DoesNotMeet per category
    """
    col = f'{aspect}_DoesNotMeet'
    
    if col not in df.columns:
        print(f"Column {col} not found!")
        return
    
    # Pivot: rows = Setting, columns = Category (aggregated)
    pivot = df.pivot_table(index='Setting', columns='Category', values=col, aggfunc='sum')
    
    # Sort settings logically
    setting_order = [
        'zeroshot_claude', 'zeroshot_gpt', 'zero_shot_deepseek',
        '1shot_claude', '1shot_gpt', '1shot_deepseek',
        'fewshot_claude', 'fewshot_gpt', 'fewshot_deepseek',
        'approach_claude', 'approach_gpt', 'approach_deepseek',
        'Agent_claude'
    ]
    available_settings = pivot.index.tolist()
    ordered_settings = []
    for s in setting_order:
        for avail in available_settings:
            if avail.lower() == s.lower():
                ordered_settings.append(avail)
                break
    for avail in available_settings:
        if avail not in ordered_settings:
            ordered_settings.append(avail)
    
    pivot = pivot.reindex(ordered_settings)
    
    # Add row totals
    pivot['TOTAL'] = pivot.sum(axis=1)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 10))
    
    sns.heatmap(pivot, annot=True, fmt='.0f', cmap='RdYlGn_r', ax=ax,
                cbar_kws={'label': f'{aspect} - Does Not Meet Count'},
                annot_kws={'size': 10}, linewidths=0.5)
    
    ax.set_title(f'{aspect}: "Does Not Meet" Counts by Setting × Category\n'
                 f'(Lower = Better)', 
                 fontsize=14, fontweight='bold')
    ax.set_xlabel('Category', fontsize=11)
    ax.set_ylabel('Experimental Setting', fontsize=11)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=9)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f'heatmap_{aspect.lower()}_doesnotmeet_by_category.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: heatmap_{aspect.lower()}_doesnotmeet_by_category.png")


def create_combined_overview(df: pd.DataFrame):
    """
    Create a single figure with 3 heatmaps side by side (aggregated by category)
    """
    aspects = ['Clarity', 'Completeness', 'Consistency']
    
    fig, axes = plt.subplots(1, 3, figsize=(20, 10))
    
    for ax, aspect in zip(axes, aspects):
        col = f'{aspect}_DoesNotMeet'
        
        if col not in df.columns:
            ax.text(0.5, 0.5, f'{aspect} data not found', transform=ax.transAxes, ha='center')
            continue
        
        # Pivot
        pivot = df.pivot_table(index='Setting', columns='Category', values=col, aggfunc='sum')
        
        # Sort settings
        setting_order = [
            'zeroshot_claude', 'zeroshot_gpt', 'zero_shot_deepseek',
            '1shot_claude', '1shot_gpt', '1shot_deepseek',
            'fewshot_claude', 'fewshot_gpt', 'fewshot_deepseek',
            'approach_claude', 'approach_gpt', 'approach_deepseek',
            'Agent_claude'
        ]
        available_settings = pivot.index.tolist()
        ordered_settings = []
        for s in setting_order:
            for avail in available_settings:
                if avail.lower() == s.lower():
                    ordered_settings.append(avail)
                    break
        for avail in available_settings:
            if avail not in ordered_settings:
                ordered_settings.append(avail)
        
        pivot = pivot.reindex(ordered_settings)
        
        sns.heatmap(pivot, annot=True, fmt='.0f', cmap='RdYlGn_r', ax=ax,
                    cbar_kws={'label': 'Count'}, annot_kws={'size': 8}, linewidths=0.5)
        
        ax.set_title(f'{aspect}\n"Does Not Meet"', fontsize=12, fontweight='bold')
        ax.set_xlabel('Category', fontsize=10)
        ax.set_ylabel('Setting' if ax == axes[0] else '', fontsize=10)
        ax.tick_params(axis='x', rotation=45)
        ax.tick_params(axis='y', labelsize=8)
    
    plt.suptitle('LLM Quality Ratings: "Does Not Meet" Counts\n(Lower = Better, Green = Good, Red = Bad)',
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'heatmap_combined_doesnotmeet.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: heatmap_combined_doesnotmeet.png")


def create_all_ratings_summary(df: pd.DataFrame):
    """
    Create summary table showing all three ratings (Meets, Partially, DoesNotMeet)
    for each aspect, aggregated by setting.
    """
    aspects = ['Clarity', 'Completeness', 'Consistency']
    ratings = ['Meets', 'PartiallyMeets', 'DoesNotMeet']
    
    # Aggregate by setting
    summary_data = []
    for setting in df['Setting'].unique():
        setting_df = df[df['Setting'] == setting]
        row = {'Setting': setting}
        
        for aspect in aspects:
            for rating in ratings:
                col = f'{aspect}_{rating}'
                if col in df.columns:
                    row[f'{aspect}_{rating}'] = setting_df[col].sum()
        
        summary_data.append(row)
    
    summary_df = pd.DataFrame(summary_data)
    
    # Sort settings
    setting_order = [
        'zeroshot_claude', 'zeroshot_gpt', 'zero_shot_deepseek',
        '1shot_claude', '1shot_gpt', '1shot_deepseek',
        'fewshot_claude', 'fewshot_gpt', 'fewshot_deepseek',
        'approach_claude', 'approach_gpt', 'approach_deepseek',
        'Agent_claude'
    ]
    
    def sort_key(s):
        s_lower = s.lower()
        for i, order_s in enumerate(setting_order):
            if order_s.lower() == s_lower:
                return i
        return 999
    
    summary_df['sort_key'] = summary_df['Setting'].apply(sort_key)
    summary_df = summary_df.sort_values('sort_key').drop('sort_key', axis=1)
    
    # Save to CSV
    summary_df.to_csv(OUTPUT_DIR / 'llm_ratings_summary.csv', index=False)
    print("Saved: llm_ratings_summary.csv")
    
    # Create visual table
    fig, ax = plt.subplots(figsize=(18, 12))
    ax.axis('off')
    
    # Select columns to display
    display_cols = ['Setting'] + [f'{a}_{r}' for a in aspects for r in ratings]
    display_df = summary_df[display_cols].copy()
    
    # Shorten column names for display
    display_df.columns = ['Setting'] + [f'{a[:4]}_{r[:4]}' for a in aspects for r in ratings]
    
    table = ax.table(cellText=display_df.values, colLabels=display_df.columns,
                     loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(7)
    table.scale(1.2, 1.5)
    
    ax.set_title('LLM Ratings Summary: All Categories Combined\n'
                 '(Clar=Clarity, Comp=Completeness, Cons=Consistency | '
                 'Meet=Meets, Part=PartiallyMeets, Does=DoesNotMeet)',
                 fontsize=12, fontweight='bold', y=0.98)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'llm_ratings_summary_table.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: llm_ratings_summary_table.png")
    
    return summary_df


def create_meets_heatmaps(df: pd.DataFrame):
    """
    Also create heatmaps for "Meets" ratings (higher = better)
    """
    aspects = ['Clarity', 'Completeness', 'Consistency']
    
    fig, axes = plt.subplots(1, 3, figsize=(20, 10))
    
    for ax, aspect in zip(axes, aspects):
        col = f'{aspect}_Meets'
        
        if col not in df.columns:
            ax.text(0.5, 0.5, f'{aspect} data not found', transform=ax.transAxes, ha='center')
            continue
        
        # Pivot
        pivot = df.pivot_table(index='Setting', columns='Category', values=col, aggfunc='sum')
        
        # Sort settings
        setting_order = [
            'zeroshot_claude', 'zeroshot_gpt', 'zero_shot_deepseek',
            '1shot_claude', '1shot_gpt', '1shot_deepseek',
            'fewshot_claude', 'fewshot_gpt', 'fewshot_deepseek',
            'approach_claude', 'approach_gpt', 'approach_deepseek',
            'Agent_claude'
        ]
        available_settings = pivot.index.tolist()
        ordered_settings = []
        for s in setting_order:
            for avail in available_settings:
                if avail.lower() == s.lower():
                    ordered_settings.append(avail)
                    break
        for avail in available_settings:
            if avail not in ordered_settings:
                ordered_settings.append(avail)
        
        pivot = pivot.reindex(ordered_settings)
        
        # Use normal colormap (higher = better = green)
        sns.heatmap(pivot, annot=True, fmt='.0f', cmap='RdYlGn', ax=ax,
                    cbar_kws={'label': 'Count'}, annot_kws={'size': 8}, linewidths=0.5)
        
        ax.set_title(f'{aspect}\n"Meets"', fontsize=12, fontweight='bold')
        ax.set_xlabel('Category', fontsize=10)
        ax.set_ylabel('Setting' if ax == axes[0] else '', fontsize=10)
        ax.tick_params(axis='x', rotation=45)
        ax.tick_params(axis='y', labelsize=8)
    
    plt.suptitle('LLM Quality Ratings: "Meets" Counts\n(Higher = Better, Green = Good, Red = Bad)',
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'heatmap_combined_meets.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: heatmap_combined_meets.png")


def main(data_dir: str):
    """Run all analyses."""
    data_path = Path(data_dir)
    
    print("="*70)
    print("LLM QUALITY RATINGS HEATMAPS")
    print("="*70)
    
    print(f"\nLoading data from: {data_path}")
    df = load_all_data(data_path)
    
    print(f"\nLoaded {len(df)} rows")
    print(f"Settings: {df['Setting'].nunique()}")
    print(f"Categories: {df['Category'].unique().tolist()}")
    print(f"Views: {df['Category_View'].nunique()}")
    
    # Check available columns
    print(f"\nAvailable LLM columns:")
    llm_cols = [c for c in df.columns if 'Clarity' in c or 'Completeness' in c or 'Consistency' in c]
    for col in llm_cols:
        print(f"  {col}: {df[col].sum():.0f} total")
    
    print("\n" + "="*70)
    print("GENERATING HEATMAPS...")
    print("="*70)
    
    # Create individual heatmaps for each aspect (detailed by view)
    for aspect in ['Clarity', 'Completeness', 'Consistency']:
        create_doesnotmeet_heatmap_by_category(df, aspect)
        create_doesnotmeet_heatmap_by_category_aggregated(df, aspect)
    
    # Create combined overview
    create_combined_overview(df)
    
    # Create Meets heatmaps
    create_meets_heatmaps(df)
    
    # Create summary table
    create_all_ratings_summary(df)
    
    print(f"\n" + "="*70)
    print(f"ALL OUTPUTS SAVED TO: {OUTPUT_DIR.absolute()}")
    print("="*70)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Usage: python llm_ratings_heatmaps.py <data_directory>")
        print("\nExample: python llm_ratings_heatmaps.py .")