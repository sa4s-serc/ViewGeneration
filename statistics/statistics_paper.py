import numpy as np
import pandas as pd
from scipy.stats import kruskal, mannwhitneyu
import scikit_posthocs as sp


# Install cliffs_delta if not available: pip install cliffs-delta
try:
    from cliffs_delta import cliffs_delta
except ImportError:
    print("Warning: cliffs_delta package not found. Install with: pip install cliffs-delta")
    cliffs_delta = None

# ==========================================
# DATA FROM TABLE III (Clarity) AND TABLE IV (Accuracy)
# ==========================================

# Clarity data from Table III - reconstructed from percentages
clarity_data = {
    "Zero-Shot (Claude)": [2]*3 + [1]*192 + [0]*130,      # Total=325: M=1.0%, P=59.0%, N=40.0%
    "One-Shot (DeepSeek)": [2]*6 + [1]*215 + [0]*99,      # Total=320: M=1.8%, P=67.2%, N=31.0%
    "Few-Shot (Claude)": [2]*3 + [1]*204 + [0]*92,        # Total=299: M=1.0%, P=68.2%, N=30.8%
    "GPA (Claude Code)": [2]*2 + [1]*89 + [0]*233,        # Total=324: M=0.6%, P=27.6%, N=71.8%
    "ArchView (Claude)": [2]*8 + [1]*243 + [0]*74         # Total=325: M=2.5%, P=74.8%, N=22.6%
}

# Accuracy data from Table IV - human evaluation
accuracy_data = {
    "Zero-Shot (Claude)": [2]*1 + [1]*9 + [0]*9,          # Total=19: M=5.3%, P=47.4%, N=47.4%
    "One-Shot (DeepSeek)": [2]*4 + [1]*9 + [0]*9,         # Total=22: M=18.2%, P=40.9%, N=40.9%
    "Few-Shot (Claude)": [2]*1 + [1]*8 + [0]*11,          # Total=20: M=5.0%, P=40.0%, N=55.0%
    "GPA (Claude Code)": [2]*0 + [1]*2 + [0]*20,          # Total=22: M=0.0%, P=9.1%, N=90.9%
    "ArchView (Claude)": [2]*4 + [1]*9 + [0]*9            # Total=22: M=18.2%, P=40.9%, N=40.9%
}
# Reconstructed from Table III (Completeness)
# Encoding: 2=Meets (M), 1=Partially Meets (P), 0=Does Not Meet (N)
completeness_data = {
    "Zero-Shot (Claude)": [2]*0 + [1]*55 + [0]*270,      # 0.0% M, 17.1% P, 82.9% N (N=325)
    "One-Shot (DeepSeek)": [2]*2 + [1]*67 + [0]*251,     # 0.6% M, 20.9% P, 78.5% N (N=320)
    "Few-Shot (Claude)": [2]*0 + [1]*79 + [0]*220,      # 0.0% M, 26.4% P, 73.6% N (N=299)
    "GPA (Claude Code)": [2]*3 + [1]*53 + [0]*268,      # 0.9% M, 16.3% P, 82.8% N (N=324)
    "ArchView (Claude)": [2]*0 + [1]*49 + [0]*276       # 0.0% M, 15.0% P, 85.0% N (N=325)
}

# Reconstructed from Table III (Consistency)
consistency_data = {
    "Zero-Shot (Claude)": [2]*0 + [1]*51 + [0]*274,      # 0.0% M, 15.6% P, 84.4% N (N=325)
    "One-Shot (DeepSeek)": [2]*2 + [1]*69 + [0]*249,     # 0.6% M, 21.5% P, 77.9% N (N=320)
    "Few-Shot (Claude)": [2]*0 + [1]*53 + [0]*246,      # 0.0% M, 17.7% P, 82.3% N (N=299)
    "GPA (Claude Code)": [2]*0 + [1]*32 + [0]*292,      # 0.0% M, 9.8% P, 90.2% N (N=324)
    "ArchView (Claude)": [2]*0 + [1]*89 + [0]*236       # 0.0% M, 27.4% P, 72.6% N (N=325)
}
# Continuous metrics from Table III (SSIM scores)
ssim_data = {
    "Zero-Shot (Claude)": [0.58] * 325,       # Mean SSIM from Table III
    "One-Shot (DeepSeek)": [0.56] * 320,      # Mean SSIM
    "Few-Shot (Claude)": [0.59] * 299,        # Mean SSIM
    "GPA (Claude Code)": [0.55] * 324,        # Mean SSIM
    "ArchView (Claude)": [0.60] * 325         # Mean SSIM
}

# ==========================================
# HELPER FUNCTIONS
# ==========================================

def calculate_cliffs_delta(group1, group2):
    """Calculate Cliff's Delta effect size with interpretation"""
    if cliffs_delta is None:
        return None, "N/A (package not installed)"
    
    try:
        delta, interpretation = cliffs_delta(group1, group2)
        return delta, interpretation
    except Exception as e:
        return None, f"Error: {str(e)}"

def interpret_effect_size(delta):
    """Manual interpretation if cliffs_delta package unavailable"""
    if delta is None:
        return "N/A"
    abs_delta = abs(delta)
    if abs_delta < 0.147:
        return "negligible"
    elif abs_delta < 0.33:
        return "small"
    elif abs_delta < 0.474:
        return "medium"
    else:
        return "large"

def format_pvalue(p):
    """Format p-value for readable output"""
    if p < 0.001:
        return "< 0.001"
    elif p < 0.01:
        return f"= {p:.3f}"
    else:
        return f"= {p:.4f}"

# ==========================================
# STATISTICAL ANALYSIS FUNCTION
# ==========================================

def analyze_metric(metric_name, data_dict, alpha=0.05):
    """
    Perform complete statistical analysis:
    1. Kruskal-Wallis omnibus test
    2. Dunn's post-hoc test with Bonferroni correction
    3. Cliff's Delta effect sizes for key comparisons
    """
    
    print("=" * 80)
    print(f"STATISTICAL ANALYSIS: {metric_name}")
    print("=" * 80)
    
    # Step 1: Verify sample sizes
    print("\n1. SAMPLE SIZES:")
    for label, values in data_dict.items():
        print(f"   {label:25s}: N = {len(values)}")
    
    # Step 2: Kruskal-Wallis omnibus test
    print(f"\n2. KRUSKAL-WALLIS TEST (α = {alpha}):")
    print("   H₀: All groups come from the same distribution")
    print("   H₁: At least one group differs significantly")
    
    groups = list(data_dict.values())
    labels = list(data_dict.keys())
    
    try:
        h_stat, p_val = kruskal(*groups)
        print(f"\n   Result: H = {h_stat:.4f}, p {format_pvalue(p_val)}")
        
        if p_val < alpha:
            print(f"   ✓ SIGNIFICANT: Reject H₀ (p < {alpha})")
            print(f"   → At least one configuration differs significantly")
            print(f"   → Proceeding to post-hoc pairwise comparisons...")
            significant = True
        else:
            print(f"   ✗ NOT SIGNIFICANT: Fail to reject H₀ (p ≥ {alpha})")
            print(f"   → No evidence of differences between configurations")
            significant = False
    except Exception as e:
        print(f"   ERROR: {str(e)}")
        return
    
    # Step 3: Post-hoc Dunn's test (only if Kruskal-Wallis is significant)
    if not significant:
        print("\n   Skipping post-hoc tests (omnibus test not significant)")
        return
    
    print(f"\n3. DUNN'S POST-HOC TEST (Bonferroni correction):")
    print("   Pairwise comparisons to identify which specific pairs differ")
    
    # Prepare long-format dataframe for Dunn's test
    combined_data = []
    for label, values in data_dict.items():
        for v in values:
            combined_data.append({'Group': label, 'Score': v})
    df = pd.DataFrame(combined_data)
    
    try:
        # Run Dunn's test with Bonferroni correction
        dunn_results = sp.posthoc_dunn(
            df, 
            val_col='Score', 
            group_col='Group',
            p_adjust='bonferroni'
        )
        
        # Display full matrix (optional - comment out if too large)
        # print("\n   Full Dunn's test results (p-values):")
        # print(dunn_results.round(4))
        
        # Focus on ArchView comparisons
        print(f"\n   Key Comparisons vs. ArchView (Claude):")
        archview_row = dunn_results.loc['ArchView (Claude)']
        
        comparisons = []
        for other_group in labels:
            if other_group != 'ArchView (Claude)':
                p = archview_row[other_group]
                sig = "✓" if p < alpha else "✗"
                comparisons.append((other_group, p, sig))
        
        # Sort by p-value
        comparisons.sort(key=lambda x: x[1])
        
        for other_group, p, sig in comparisons:
            print(f"   {sig} ArchView vs {other_group:25s}: p {format_pvalue(p)}")
        
    except Exception as e:
        print(f"   ERROR in Dunn's test: {str(e)}")
        print("   This may occur if groups have identical distributions")
    
    # Step 4: Effect sizes (Cliff's Delta) for key comparisons
    print(f"\n4. EFFECT SIZES (Cliffs Delta):")
    print("   Quantifies magnitude of differences")
    print("   Thresholds: |δ| < 0.147 (negligible), 0.147-0.33 (small),")
    print("              0.33-0.474 (medium), ≥ 0.474 (large)")
    
    archview_data = data_dict['ArchView (Claude)']
    
    effect_sizes = []
    for other_group in labels:
        if other_group != 'ArchView (Claude)':
            other_data = data_dict[other_group]
            delta, interp = calculate_cliffs_delta(archview_data, other_data)
            
            if delta is not None:
                effect_sizes.append((other_group, delta, interp))
    
    # Sort by absolute effect size (descending)
    effect_sizes.sort(key=lambda x: abs(x[1]) if x[1] is not None else 0, reverse=True)
    
    print(f"\n   ArchView vs Other Configurations:")
    for other_group, delta, interp in effect_sizes:
        if delta is not None:
            print(f"   ArchView vs {other_group:25s}: δ = {delta:+.3f} ({interp})")
        else:
            print(f"   ArchView vs {other_group:25s}: {interp}")
    
    print("\n" + "=" * 80 + "\n")
    
    # Return results for export
    return {
        'metric': metric_name,
        'kruskal_wallis_h': h_stat if 'h_stat' in locals() else None,
        'kruskal_wallis_p': p_val if 'p_val' in locals() else None,
        'dunn_results': dunn_results if 'dunn_results' in locals() and significant else None,
        'effect_sizes': effect_sizes if 'effect_sizes' in locals() else None
    }

# ==========================================
# MAIN ANALYSIS
# ==========================================

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("STATISTICAL SIGNIFICANCE ANALYSIS FOR ARCHITECTURE VIEW GENERATION")
    print("=" * 80)
    print("\nMethodology:")
    print("• Kruskal-Wallis H-test (non-parametric ANOVA)")
    print("• Dunn's post-hoc test with Bonferroni correction")
    print("• Cliff's Delta effect size (δ)")
    print("\nSignificance level: α = 0.05")
    print("=" * 80 + "\n")
    
    # Analyze each metric and collect results
    results = []
    
    results.append(analyze_metric("Clarity", clarity_data))
    results.append(analyze_metric("Completeness", completeness_data))
    results.append(analyze_metric("Consistency", consistency_data))
    
    # Analyze Human Evaluation
    results.append(analyze_metric("Accuracy", accuracy_data))
    # analyze_metric("SSIM (Image Similarity)", ssim_data)  # Uncomment if you have actual SSIM distributions
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print("\nNOTE: These results should be reported in your paper's Results section")
    print("along with the original descriptive statistics from Tables III and IV.")
    print("=" * 80 + "\n")
    
    # ==========================================
    # EXPORT P-VALUES TO CSV
    # ==========================================
    
    print("=" * 80)
    print("EXPORTING P-VALUES AND EFFECT SIZES")
    print("=" * 80 + "\n")
    
    # Export detailed p-value tables
    export_data = []
    
    for result in results:
        if result['dunn_results'] is not None:
            metric_name = result['metric']
            dunn_df = result['dunn_results']
            effect_sizes_dict = {es[0]: {'delta': es[1], 'interpretation': es[2]} 
                                for es in result['effect_sizes']}
            
            # Extract ArchView comparisons
            archview_key = 'ArchView (Claude)'
            if archview_key in dunn_df.index:
                archview_row = dunn_df.loc[archview_key]
                
                for other_group in dunn_df.columns:
                    if other_group != archview_key:
                        p_value = archview_row[other_group]
                        
                        # Get effect size
                        es_info = effect_sizes_dict.get(other_group, {'delta': None, 'interpretation': 'N/A'})
                        
                        export_data.append({
                            'Metric': metric_name,
                            'Comparison': f'ArchView vs {other_group}',
                            'Kruskal-Wallis H': result['kruskal_wallis_h'],
                            'Kruskal-Wallis p-value': result['kruskal_wallis_p'],
                            'Dunn p-value (Bonferroni)': p_value,
                            'Significant (α=0.05)': 'Yes' if p_value < 0.05 else 'No',
                            "Cliffs Delta (δ)": es_info['delta'],
                            'Effect Size Interpretation': es_info['interpretation']
                        })
    
    # Create DataFrame and export
    export_df = pd.DataFrame(export_data)
    
    # Save to CSV
    csv_filename = 'p_values_and_effect_sizes.csv'
    export_df.to_csv(csv_filename, index=False, float_format='%.6f')
    print(f"✓ Exported to: {csv_filename}")
    
    # Display the table
    print("\n" + "=" * 80)
    print("COMPLETE P-VALUE AND EFFECT SIZE TABLE")
    print("=" * 80 + "\n")
    
    # Format for display
    display_df = export_df.copy()
    display_df['Kruskal-Wallis H'] = display_df['Kruskal-Wallis H'].apply(lambda x: f"{x:.4f}" if pd.notna(x) else "N/A")
    display_df['Kruskal-Wallis p-value'] = display_df['Kruskal-Wallis p-value'].apply(
        lambda x: f"{x:.6f}" if pd.notna(x) and x >= 0.001 else "< 0.001" if pd.notna(x) else "N/A"
    )
    display_df['Dunn p-value (Bonferroni)'] = display_df['Dunn p-value (Bonferroni)'].apply(
        lambda x: f"{x:.6f}" if pd.notna(x) and x >= 0.001 else "< 0.001" if pd.notna(x) else "N/A"
    )
    display_df["Cliffs Delta (δ)"] = display_df["Cliffs Delta (δ)"].apply(
        lambda x: f"{x:+.3f}" if pd.notna(x) else "N/A"
    )
    
    print(display_df.to_string(index=False))
    print("\n" + "=" * 80 + "\n")
    
    # Also create a simplified table for paper
    paper_table_data = []
    for _, row in export_df.iterrows():
        comparison_short = row['Comparison'].replace('ArchView vs ', '')
        
        if row['Dunn p-value (Bonferroni)'] < 0.001:
            p_display = "< 0.001"
        elif row['Dunn p-value (Bonferroni)'] < 0.01:
            p_display = f"{row['Dunn p-value (Bonferroni)']:.3f}"
        else:
            p_display = f"{row['Dunn p-value (Bonferroni)']:.4f}"
        
        paper_table_data.append({
            'Metric': row['Metric'].replace(' (Automated LLM-as-Judge)', '').replace(' (Human Evaluation)', ''),
            'Comparison': comparison_short,
            'p-value': p_display,
            'δ': f"{row['Cliffs Delta (δ)']:+.3f}" if pd.notna(row["Cliffs Delta (δ)"]) else "N/A",
            'Effect': row['Effect Size Interpretation'],
            'Sig.': '✓' if row['Significant (α=0.05)'] == 'Yes' else '✗'
        })
    
    paper_df = pd.DataFrame(paper_table_data)
    
    print("=" * 80)
    print("CONDENSED TABLE FOR PAPER (LaTeX-ready)")
    print("=" * 80 + "\n")
    print(paper_df.to_string(index=False))
    
    # Export paper table
    paper_csv = 'p_values_paper_table.csv'
    paper_df.to_csv(paper_csv, index=False)
    print(f"\n✓ Condensed table exported to: {paper_csv}")
    
    # Generate LaTeX table
    latex_file = 'p_values_latex_table.tex'
    with open(latex_file, 'w') as f:
        f.write("% LaTeX table for statistical results\n")
        f.write("% Add to your paper's Results section\n\n")
        f.write("\\begin{table}[ht]\n")
        f.write("\\centering\n")
        f.write("\\caption{Statistical Significance and Effect Sizes for Key Comparisons}\n")
        f.write("\\label{tab:statistical_results}\n")
        f.write("\\begin{tabular}{llcccc}\n")
        f.write("\\hline\n")
        f.write("\\textbf{Metric} & \\textbf{Comparison} & \\textbf{p-value} & \\textbf{$\\delta$} & \\textbf{Effect Size} & \\textbf{Sig.} \\\\\n")
        f.write("\\hline\n")
        
        current_metric = None
        for _, row in paper_df.iterrows():
            metric = row['Metric'] if row['Metric'] != current_metric else ""
            current_metric = row['Metric']
            
            f.write(f"{metric} & {row['Comparison']} & {row['p-value']} & {row['δ']} & {row['Effect']} & {row['Sig.']} \\\\\n")
        
        f.write("\\hline\n")
        f.write("\\end{tabular}\n")
        f.write("\\end{table}\n")
    
    print(f"✓ LaTeX table exported to: {latex_file}")
    print("\n" + "=" * 80 + "\n")