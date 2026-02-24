import pandas as pd
import numpy as np
from scipy.stats import kruskal
import scikit_posthocs as sp
import warnings
warnings.filterwarnings('ignore')

try:
    from cliffs_delta import cliffs_delta
    HAS_CLIFFS_DELTA = True
except ImportError:
    HAS_CLIFFS_DELTA = False

# Configuration
MODELS_TO_ANALYZE = {
    'Few-Shot (Claude)': 'fewshot_claude',
    'GPA (Claude Code)': 'agent_claude',
    'ArchView (Claude)': 'approach_claude'
}

RATING_MAP = {
    "Meets Expectations": 2,
    "Partially Meets Expectations": 1,
    "Does Not Meet Expectations": 0
}

def calculate_llm_quality(df, model_prefix):
    """Calculate LLM Quality from 3Cs ratings"""
    temp_df = df.copy()
    for c in ['Clarity', 'Completeness', 'Consistency']:
        col_name = f"{model_prefix}_LLM_{c}_Rating"
        if col_name in temp_df.columns:
            temp_df[col_name + '_numeric'] = temp_df[col_name].map(RATING_MAP)
    
    quality_cols = [f"{model_prefix}_LLM_{c}_Rating_numeric" 
                    for c in ['Clarity', 'Completeness', 'Consistency']]
    existing_cols = [c for c in quality_cols if c in temp_df.columns]
    
    if len(existing_cols) == 3:
        temp_df['LLM_Quality'] = temp_df[existing_cols].mean(axis=1)
    else:
        temp_df['LLM_Quality'] = np.nan
    
    return temp_df

def simplify_categories(value):
    """Take primary category from comma-separated values"""
    if pd.isna(value) or value == '':
        return 'unknown'
    if ',' in str(value):
        return str(value).split(',')[0].strip()
    return str(value).strip()

def get_detailed_comparisons(df, category_col, metric_col, model_name, category_name):
    """
    Extract detailed pairwise comparisons with rankings
    Returns which categories are significantly better/worse than others
    """
    results = []
    
    # Filter valid data
    df_valid = df[[category_col, metric_col]].dropna()
    
    if len(df_valid) < 10:
        return results
    
    # Get category statistics
    stats_by_category = df_valid.groupby(category_col)[metric_col].agg([
        ('N', 'count'),
        ('Mean', 'mean'),
        ('Median', 'median'),
        ('Std', 'std')
    ]).round(4)
    
    # Only keep categories with N >= 10
    stats_by_category = stats_by_category[stats_by_category['N'] >= 10]
    
    if len(stats_by_category) < 2:
        return results
    
    # Sort by median performance (descending)
    stats_by_category = stats_by_category.sort_values('Median', ascending=False)
    stats_by_category['Rank'] = range(1, len(stats_by_category) + 1)
    
    # Perform Kruskal-Wallis
    groups = []
    group_names = []
    for cat in stats_by_category.index:
        group_data = df_valid[df_valid[category_col] == cat][metric_col].values
        if len(group_data) >= 10:
            groups.append(group_data)
            group_names.append(cat)
    
    if len(groups) < 2:
        return results
    
    h_stat, p_val = kruskal(*groups)
    
    # Store ranking information
    for cat in stats_by_category.index:
        results.append({
            'Category_Type': category_name,
            'Model': model_name,
            'Metric': metric_col.split('_')[-1] if '_' in metric_col else metric_col,
            'Category_Value': cat,
            'Rank': int(stats_by_category.loc[cat, 'Rank']),
            'N': int(stats_by_category.loc[cat, 'N']),
            'Median': stats_by_category.loc[cat, 'Median'],
            'Mean': stats_by_category.loc[cat, 'Mean'],
            'Std': stats_by_category.loc[cat, 'Std'],
            'Overall_H': h_stat,
            'Overall_p': p_val
        })
    
    # If significant, get pairwise comparisons
    if p_val < 0.05:
        try:
            dunn_results = sp.posthoc_dunn(
                df_valid,
                val_col=metric_col,
                group_col=category_col,
                p_adjust='bonferroni'
            )
            
            # Find significant pairs and calculate effect sizes
            pairwise_results = []
            
            for i, cat1 in enumerate(group_names):
                for j, cat2 in enumerate(group_names):
                    if i < j and cat1 in dunn_results.index and cat2 in dunn_results.columns:
                        p_pair = dunn_results.loc[cat1, cat2]
                        
                        if p_pair < 0.05:  # Only report significant pairs
                            grp1 = df_valid[df_valid[category_col]==cat1][metric_col].values
                            grp2 = df_valid[df_valid[category_col]==cat2][metric_col].values
                            
                            # Determine which is better
                            med1 = np.median(grp1)
                            med2 = np.median(grp2)
                            better = cat1 if med1 > med2 else cat2
                            worse = cat2 if med1 > med2 else cat1
                            improvement = ((max(med1, med2) - min(med1, med2)) / min(med1, med2)) * 100
                            
                            # Calculate effect size
                            delta, interp = None, "N/A"
                            if HAS_CLIFFS_DELTA:
                                try:
                                    delta, interp = cliffs_delta(grp1, grp2)
                                except:
                                    pass
                            
                            pairwise_results.append({
                                'Category_Type': category_name,
                                'Model': model_name,
                                'Metric': metric_col.split('_')[-1] if '_' in metric_col else metric_col,
                                'Better_Category': better,
                                'Worse_Category': worse,
                                'Better_Median': max(med1, med2),
                                'Worse_Median': min(med1, med2),
                                'Improvement_%': improvement,
                                'p_value': p_pair,
                                'Cliffs_Delta': delta if delta is not None else np.nan,
                                'Effect_Size': interp
                            })
            
            return results, pairwise_results
        
        except Exception as e:
            print(f"Error in pairwise analysis: {e}")
            return results, []
    
    return results, []

def main():
    print("=" * 80)
    print("DETAILED CATEGORY RANKINGS AND PAIRWISE COMPARISONS")
    print("=" * 80)
    
    # Load data
    df = pd.read_csv("final_combined_all_models.csv")
    print(f"\nLoaded {len(df)} repositories\n")
    
    all_rankings = []
    all_pairwise = []
    
    # Categories to analyze
    categories = {
        'Architectural Notation': 'Architectural Notation',
        'Granularity': 'Granularity',
        'Concern': 'Concern',
        'QAs': 'QAs'
    }
    
    for cat_name, cat_col in categories.items():
        print(f"\n{'='*80}")
        print(f"ANALYZING: {cat_name}")
        print(f"{'='*80}")
        
        # Simplify categories
        df_work = df.copy()
        df_work[f'{cat_col}_simplified'] = df_work[cat_col].apply(simplify_categories)
        
        for model_label, model_prefix in MODELS_TO_ANALYZE.items():
            print(f"\n--- {model_label} ---")
            
            # Calculate LLM Quality
            df_model = calculate_llm_quality(df_work, model_prefix)
            
            # Analyze SSIM
            ssim_col = f"{model_prefix}_SSIM"
            if ssim_col in df_model.columns:
                print(f"\nSSIM Analysis:")
                rankings, pairwise = get_detailed_comparisons(
                    df_model, 
                    f'{cat_col}_simplified',
                    ssim_col,
                    model_label,
                    cat_name
                )
                
                if rankings:
                    all_rankings.extend(rankings)
                    print(f"  Category Rankings (by median SSIM):")
                    for r in sorted(rankings, key=lambda x: x['Rank']):
                        print(f"    {r['Rank']}. {r['Category_Value']:30s} "
                              f"(N={r['N']:3d}, Median={r['Median']:.4f})")
                
                if pairwise:
                    all_pairwise.extend(pairwise)
                    print(f"\n  Significant Pairwise Differences:")
                    for p in sorted(pairwise, key=lambda x: x['p_value']):
                        print(f"    ✓ {p['Better_Category']:25s} > {p['Worse_Category']:25s}")
                        print(f"      Improvement: {p['Improvement_%']:5.1f}%, "
                              f"p={p['p_value']:.4f}, δ={p['Cliffs_Delta']:.3f} ({p['Effect_Size']})")
            
            # Analyze LLM Quality
            if 'LLM_Quality' in df_model.columns:
                print(f"\nLLM Quality Analysis:")
                rankings, pairwise = get_detailed_comparisons(
                    df_model,
                    f'{cat_col}_simplified',
                    'LLM_Quality',
                    model_label,
                    cat_name
                )
                
                if rankings:
                    all_rankings.extend(rankings)
                    print(f"  Category Rankings (by median LLM Quality):")
                    for r in sorted(rankings, key=lambda x: x['Rank']):
                        print(f"    {r['Rank']}. {r['Category_Value']:30s} "
                              f"(N={r['N']:3d}, Median={r['Median']:.4f})")
                
                if pairwise:
                    all_pairwise.extend(pairwise)
                    print(f"\n  Significant Pairwise Differences:")
                    for p in sorted(pairwise, key=lambda x: x['p_value']):
                        print(f"    ✓ {p['Better_Category']:25s} > {p['Worse_Category']:25s}")
                        print(f"      Improvement: {p['Improvement_%']:5.1f}%, "
                              f"p={p['p_value']:.4f}, δ={p['Cliffs_Delta']:.3f} ({p['Effect_Size']})")
    
    # Export results
    print("\n" + "=" * 80)
    print("EXPORTING DETAILED RESULTS")
    print("=" * 80)
    
    if all_rankings:
        rankings_df = pd.DataFrame(all_rankings)
        rankings_df.to_csv('category_rankings_detailed.csv', index=False)
        print(f"\n✓ Category rankings exported to: category_rankings_detailed.csv")
    
    if all_pairwise:
        pairwise_df = pd.DataFrame(all_pairwise)
        pairwise_df.to_csv('pairwise_comparisons_detailed.csv', index=False)
        print(f"✓ Pairwise comparisons exported to: pairwise_comparisons_detailed.csv")
        
        # Create summary for paper
        print("\n" + "=" * 80)
        print("SUMMARY: BEST PERFORMING CATEGORIES")
        print("=" * 80)
        
        # Group by category type and show best performers
        for cat_type in rankings_df['Category_Type'].unique():
            print(f"\n{cat_type}:")
            cat_data = rankings_df[rankings_df['Category_Type'] == cat_type]
            
            # Show best category for each model-metric combination
            for model in cat_data['Model'].unique():
                model_data = cat_data[cat_data['Model'] == model]
                
                for metric in model_data['Metric'].unique():
                    metric_data = model_data[model_data['Metric'] == metric]
                    best = metric_data[metric_data['Rank'] == 1].iloc[0]
                    worst = metric_data[metric_data['Rank'] == metric_data['Rank'].max()].iloc[0]
                    
                    print(f"  {model:25s} - {metric:15s}:")
                    print(f"    Best:  {best['Category_Value']:25s} (Median={best['Median']:.4f})")
                    print(f"    Worst: {worst['Category_Value']:25s} (Median={worst['Median']:.4f})")
                    
                    improvement = ((best['Median'] - worst['Median']) / worst['Median']) * 100
                    print(f"    Gap: {improvement:+.1f}%")
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()