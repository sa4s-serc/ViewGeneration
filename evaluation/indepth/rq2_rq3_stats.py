import pandas as pd
import numpy as np
from scipy.stats import kruskal, mannwhitneyu
import scikit_posthocs as sp
from itertools import combinations
import warnings
warnings.filterwarnings('ignore')

try:
    from cliffs_delta import cliffs_delta
    HAS_CLIFFS_DELTA = True
except ImportError:
    print("Warning: cliffs_delta not installed. Install with: pip install cliffs-delta")
    HAS_CLIFFS_DELTA = False

# ==============================================
# CONFIGURATION
# ==============================================

# Best models from RQ1 analysis
MODELS_TO_ANALYZE = {
    'Few-Shot (Claude)': 'fewshot_claude',
    'GPA (Claude Code)': 'agent_claude',
    'ArchView (Claude)': 'approach_claude'
}

# Formal rating mapping
RATING_MAP = {
    "Meets Expectations": 2,
    "Partially Meets Expectations": 1,
    "Does Not Meet Expectations": 0
}

# Categories to analyze - matching your actual column names
CATEGORIES_CONFIG = {
    'Architectural Notation': {
        'column': 'Architectural Notation',
        'min_samples': 10  # Only analyze notations with ≥10 samples
    },
    'Granularity': {
        'column': 'Granularity',
        'min_samples': 5
    },
    'Concern': {
        'column': 'Concern',
        'min_samples': 10  # Only test concerns with ≥10 repos
    },
    'QAs': {
        'column': 'QAs',
        'min_samples': 10
    }
}

# ==============================================
# HELPER FUNCTIONS
# ==============================================

def calculate_llm_quality_from_raw(df, model_prefix):
    """
    Calculate LLM Quality as average of 3Cs (Clarity, Completeness, Consistency)
    by mapping string ratings to numeric values
    """
    temp_df = df.copy()
    
    # Map each 3C rating to numeric value
    for c in ['Clarity', 'Completeness', 'Consistency']:
        col_name = f"{model_prefix}_LLM_{c}_Rating"
        if col_name in temp_df.columns:
            temp_df[col_name + '_numeric'] = temp_df[col_name].map(RATING_MAP)
    
    # Calculate mean of the three numeric ratings
    quality_cols = [f"{model_prefix}_LLM_{c}_Rating_numeric" 
                    for c in ['Clarity', 'Completeness', 'Consistency']]
    
    # Only calculate if all three columns exist
    existing_cols = [c for c in quality_cols if c in temp_df.columns]
    if len(existing_cols) == 3:
        temp_df['LLM_Quality'] = temp_df[existing_cols].mean(axis=1)
    else:
        temp_df['LLM_Quality'] = np.nan
    
    return temp_df


def simplify_categories(value):
    """
    Simplify complex categories by taking the first/primary value
    E.g., "deployment, connectivity" -> "deployment"
         "boxes_and_arrows, icons_and_arrows" -> "boxes_and_arrows"
    """
    if pd.isna(value) or value == '':
        return 'unknown'
    
    # Take first value if comma-separated
    if ',' in str(value):
        return str(value).split(',')[0].strip()
    return str(value).strip()


def filter_categories_by_sample_size(df, category_col, min_samples=10):
    """
    Keep only categories that have at least min_samples repositories
    """
    value_counts = df[category_col].value_counts()
    valid_categories = value_counts[value_counts >= min_samples].index.tolist()
    
    filtered_df = df[df[category_col].isin(valid_categories)].copy()
    
    print(f"  Filtered from {df[category_col].nunique()} to {len(valid_categories)} categories")
    print(f"  (kept categories with N ≥ {min_samples})")
    print(f"  Valid categories: {valid_categories}")
    
    return filtered_df, valid_categories


def calculate_effect_size_pair(group1, group2):
    """Calculate Cliff's Delta between two groups"""
    if not HAS_CLIFFS_DELTA:
        return None, "N/A"
    
    try:
        delta, interpretation = cliffs_delta(group1, group2)
        return delta, interpretation
    except:
        return None, "Error"


def perform_category_analysis(df, category_name, category_config):
    """
    Perform complete statistical analysis for one category (e.g., Notation)
    Tests each model separately across category values
    """
    print("\n" + "=" * 80)
    print(f"CATEGORY: {category_name}")
    print("=" * 80)
    
    category_col = category_config['column']
    min_samples = category_config['min_samples']
    
    # Simplify complex categories (take primary value)
    df_work = df.copy()
    df_work[f'{category_col}_simplified'] = df_work[category_col].apply(simplify_categories)
    
    # Filter to keep only categories with sufficient samples
    df_filtered, valid_cats = filter_categories_by_sample_size(
        df_work, 
        f'{category_col}_simplified',
        min_samples
    )
    
    if len(valid_cats) < 2:
        print(f"⚠ Insufficient categories for testing (need ≥2, have {len(valid_cats)})")
        return []
    
    results = []
    
    # Test each model separately
    for model_label, model_prefix in MODELS_TO_ANALYZE.items():
        print(f"\n{'─' * 80}")
        print(f"MODEL: {model_label} ({model_prefix})")
        print(f"{'─' * 80}")
        
        # Calculate LLM Quality for this model
        df_model = calculate_llm_quality_from_raw(df_filtered, model_prefix)
        
        # Test both SSIM and LLM Quality
        metrics_to_test = [
            ('SSIM', f"{model_prefix}_SSIM"),
            ('LLM Quality', 'LLM_Quality')
        ]
        
        for metric_name, metric_col in metrics_to_test:
            if metric_col not in df_model.columns:
                continue
            
            # Drop NaN values
            df_valid = df_model[[f'{category_col}_simplified', metric_col]].dropna()
            
            if len(df_valid) < 10:
                print(f"  ⚠ {metric_name}: Insufficient data (N={len(df_valid)})")
                continue
            
            # Group data by category
            grouped = df_valid.groupby(f'{category_col}_simplified')[metric_col]
            groups = [group.values for name, group in grouped if len(group) >= 3]
            group_names = [name for name, group in grouped if len(group) >= 3]
            
            if len(groups) < 2:
                print(f"  ⚠ {metric_name}: Insufficient groups (need ≥2)")
                continue
            
            # Print sample sizes
            print(f"\n  {metric_name}:")
            print(f"    Sample sizes:")
            for name, group in zip(group_names, groups):
                print(f"      {name:30s}: N = {len(group):3d}, "
                      f"Mean = {np.mean(group):.4f}, Median = {np.median(group):.4f}")
            
            # Kruskal-Wallis omnibus test
            try:
                h_stat, p_val = kruskal(*groups)
                is_sig = p_val < 0.05
                
                print(f"\n    Kruskal-Wallis: H = {h_stat:.4f}, p = {p_val:.6f}", end='')
                if is_sig:
                    print(" ✓ SIGNIFICANT")
                else:
                    print(" (not significant)")
                
                # Store result
                result = {
                    'RQ': 'RQ2' if category_name in ['Architectural Notation', 'Granularity'] else 'RQ3',
                    'Category': category_name,
                    'Model': model_label,
                    'Metric': metric_name,
                    'Num_Categories': len(groups),
                    'Total_N': sum(len(g) for g in groups),
                    'H_statistic': h_stat,
                    'p_value': p_val,
                    'Significant': 'Yes' if is_sig else 'No'
                }
                results.append(result)
                
                # Post-hoc tests if significant
                if is_sig and len(groups) >= 2:
                    print(f"\n    Post-hoc Dunn's Test (Bonferroni correction):")
                    
                    try:
                        # Prepare for Dunn's test
                        dunn_results = sp.posthoc_dunn(
                            df_valid,
                            val_col=metric_col,
                            group_col=f'{category_col}_simplified',
                            p_adjust='bonferroni'
                        )
                        
                        # Find significant pairs
                        sig_pairs = []
                        for i, cat1 in enumerate(group_names):
                            for j, cat2 in enumerate(group_names):
                                if i < j and cat1 in dunn_results.index and cat2 in dunn_results.columns:
                                    p_pair = dunn_results.loc[cat1, cat2]
                                    if p_pair < 0.05:
                                        sig_pairs.append((cat1, cat2, p_pair))
                        
                        if sig_pairs:
                            print(f"      Significant pairs (p < 0.05):")
                            for cat1, cat2, p_pair in sorted(sig_pairs, key=lambda x: x[2]):
                                print(f"        • {cat1} vs {cat2}: p = {p_pair:.6f}")
                                
                                # Calculate effect size
                                if HAS_CLIFFS_DELTA:
                                    grp1 = df_valid[df_valid[f'{category_col}_simplified']==cat1][metric_col].values
                                    grp2 = df_valid[df_valid[f'{category_col}_simplified']==cat2][metric_col].values
                                    delta, interp = calculate_effect_size_pair(grp1, grp2)
                                    if delta is not None:
                                        print(f"          Cliff's δ = {delta:+.3f} ({interp})")
                        else:
                            print(f"      No pairwise differences remain significant after correction")
                    
                    except Exception as e:
                        print(f"      Error in Dunn's test: {e}")
                    
                    # Also show best vs worst category comparison
                    print(f"\n    Effect Size (Best vs Worst):")
                    medians = [(name, np.median(vals), vals) for name, vals in zip(group_names, groups)]
                    medians.sort(key=lambda x: x[1], reverse=True)
                    
                    best_name, best_med, best_vals = medians[0]
                    worst_name, worst_med, worst_vals = medians[-1]
                    
                    print(f"      Best:  {best_name:30s} (median = {best_med:.4f})")
                    print(f"      Worst: {worst_name:30s} (median = {worst_med:.4f})")
                    
                    if HAS_CLIFFS_DELTA:
                        delta, interp = calculate_effect_size_pair(best_vals, worst_vals)
                        if delta is not None:
                            improvement_pct = ((best_med - worst_med) / worst_med) * 100
                            print(f"      Cliff's δ = {delta:+.3f} ({interp})")
                            print(f"      Improvement: {improvement_pct:+.1f}%")
            
            except Exception as e:
                print(f"    Error in Kruskal-Wallis: {e}")
    
    return results


# ==============================================
# MAIN ANALYSIS
# ==============================================

def main():
    print("=" * 80)
    print("STATISTICAL ANALYSIS: RQ2 AND RQ3")
    print("=" * 80)
    print("\nAnalyzing architectural view generation across:")
    print("  RQ2: Notation complexity and Granularity")
    print("  RQ3: Architectural Concerns and Quality Attributes")
    print("\nMethodology:")
    print("  • Kruskal-Wallis H-test (omnibus)")
    print("  • Dunn's post-hoc test with Bonferroni correction")
    print("  • Cliff's Delta effect sizes")
    print(f"  • Significance level: α = 0.05")
    print("=" * 80)
    
    # Load data
    print("\nLoading data...")
    df = pd.read_csv("final_combined_all_models.csv")
    print(f"✓ Loaded {len(df)} repositories")
    
    all_results = []
    
    # Analyze each category
    for cat_name, cat_config in CATEGORIES_CONFIG.items():
        try:
            results = perform_category_analysis(df, cat_name, cat_config)
            all_results.extend(results)
        except Exception as e:
            print(f"\n⚠ Error analyzing {cat_name}: {e}")
            import traceback
            traceback.print_exc()
    
    # ==============================================
    # EXPORT RESULTS
    # ==============================================
    
    if all_results:
        print("\n" + "=" * 80)
        print("EXPORTING RESULTS")
        print("=" * 80)
        
        results_df = pd.DataFrame(all_results)
        
        # Export full results
        output_file = 'rq2_rq3_statistical_results_complete.csv'
        results_df.to_csv(output_file, index=False)
        print(f"\n✓ Full results exported to: {output_file}")
        
        # Create summary
        print("\n" + "=" * 80)
        print("SUMMARY OF SIGNIFICANT FINDINGS")
        print("=" * 80)
        
        sig_results = results_df[results_df['Significant'] == 'Yes']
        
        if len(sig_results) > 0:
            print(f"\n✓ Found {len(sig_results)} significant results:\n")
            
            for _, row in sig_results.iterrows():
                print(f"{'[' + row['RQ'] + ']':8s} {row['Category']:25s} | "
                      f"{row['Model']:20s} | {row['Metric']:15s}")
                print(f"         H = {row['H_statistic']:6.2f}, p = {row['p_value']:.6f}, "
                      f"N_categories = {row['Num_Categories']}, Total_N = {row['Total_N']}")
        else:
            print("\n⚠ No significant differences found.")
            print("\nPossible reasons:")
            print("  • True lack of differences across categories")
            print("  • High variability within categories")
            print("  • Sample sizes too small for some categories")
        
        # Summary by category
        print("\n" + "=" * 80)
        print("SUMMARY BY CATEGORY AND RQ")
        print("=" * 80)
        
        for rq in ['RQ2', 'RQ3']:
            print(f"\n{rq}:")
            rq_results = results_df[results_df['RQ'] == rq]
            
            for cat in rq_results['Category'].unique():
                cat_results = rq_results[rq_results['Category'] == cat]
                sig_count = len(cat_results[cat_results['Significant'] == 'Yes'])
                total = len(cat_results)
                
                print(f"  {cat:30s}: {sig_count}/{total} significant")
                
                # Show which model-metric combinations were significant
                sig_cat = cat_results[cat_results['Significant'] == 'Yes']
                for _, row in sig_cat.iterrows():
                    print(f"    ✓ {row['Model']:20s} - {row['Metric']:15s}: "
                          f"p = {row['p_value']:.6f}")
        
        # Create paper-ready summary table
        paper_summary = []
        for _, row in sig_results.iterrows():
            if row['p_value'] < 0.001:
                p_display = "< 0.001"
            elif row['p_value'] < 0.01:
                p_display = f"{row['p_value']:.3f}"
            else:
                p_display = f"{row['p_value']:.4f}"
            
            paper_summary.append({
                'RQ': row['RQ'],
                'Category': row['Category'],
                'Model': row['Model'].replace(' (Claude)', '').replace(' (Claude Code)', ''),
                'Metric': row['Metric'],
                'H': f"{row['H_statistic']:.2f}",
                'p-value': p_display,
                'N': row['Total_N']
            })
        
        if paper_summary:
            paper_df = pd.DataFrame(paper_summary)
            paper_file = 'rq2_rq3_paper_summary.csv'
            paper_df.to_csv(paper_file, index=False)
            print(f"\n✓ Paper-ready summary exported to: {paper_file}")
            
            print("\n" + "=" * 80)
            print("PAPER-READY TABLE")
            print("=" * 80)
            print("\n" + paper_df.to_string(index=False))
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print("\nNext steps:")
    print("1. Review 'rq2_rq3_statistical_results_complete.csv' for all details")
    print("2. Use 'rq2_rq3_paper_summary.csv' for your Results section")
    print("3. Report H-statistics, p-values, and significant pairwise comparisons")
    print("4. Update your RQ2 and RQ3 'Answer' boxes with statistical evidence")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()