"""
Publication-Ready Cross-Table Generator
========================================

Features:
1. COMPACT / TIGHT BOXES (Physically smaller)
2. LARGE AXIS FONTS
3. Legend: Right Side (Bottom Aligned)
4. 300 DPI high-resolution output
"""

from matplotlib.lines import Line2D
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set matplotlib defaults for publication quality
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.linewidth'] = 1.5

OUTPUT_DIR = Path("./publication_crosstables")
OUTPUT_DIR.mkdir(exist_ok=True)
# 'pastel' index 6 is typically a soft lavender, index 0 is a soft pink/red

 
cubehelix_colors = sns.color_palette("cubehelix", 13).as_hex()

# If you want it to look more "lavender" (starting lighter and staying purple)
Spectral_colors = sns.color_palette(
    sns.cubehelix_palette(13, start=0.5, rot=-0.2, light=0.9, dark=0.6)
).as_hex()
# Spectral_colors = sns.color_palette("crest", 13).as_hex()



# ============================================================================
# CONFIGURATION
# ============================================================================

FULL_LABELS = {
    'zeroshot_claude': 'Zero-shot\nClaude',
    'zeroshot_deepseek': 'Zero-shot\nDeepSeek',
    'zeroshot_gpt': 'Zero-shot\nGPT',
    '1shot_claude': 'One-shot\nClaude',
    '1shot_deepseek': 'One-shot\nDeepSeek',
    '1shot_gpt': 'One-shot\nGPT',
    'fewshot_claude': 'Few-shot\nClaude',
    'fewshot_deepseek': 'Few-shot\nDeepSeek',
    'fewshot_gpt': 'Few-shot\nGPT',
    'approach_claude': 'ArchView\nClaude',
    'approach_deepseek': 'ArchView\nDeepSeek',
    'approach_gpt': 'ArchView\nGPT',
    'agent_claude': 'Agent\nClaude'
}

COMPACT_LABELS = {
    'zeroshot_claude': 'ZS-C', 'zeroshot_deepseek': 'ZS-D', 'zeroshot_gpt': 'ZS-G',
    '1shot_claude': '1S-C', '1shot_deepseek': '1S-D', '1shot_gpt': '1S-G',
    'fewshot_claude': 'FS-C', 'fewshot_deepseek': 'FS-D', 'fewshot_gpt': 'FS-G',
    'approach_claude': 'AV-C', 'approach_deepseek': 'AV-D', 'approach_gpt': 'AV-G',
    'agent_claude': 'Ag-C'
}

CONFIG_COLORS = {
    'zeroshot_claude': Spectral_colors[0], 'zeroshot_deepseek': Spectral_colors[1], 'zeroshot_gpt': Spectral_colors[2],
    '1shot_claude': Spectral_colors[3], '1shot_deepseek': Spectral_colors[4], '1shot_gpt': Spectral_colors[5],
    'fewshot_claude': Spectral_colors[6], 'fewshot_deepseek': Spectral_colors[7], 'fewshot_gpt': Spectral_colors[8],
    'approach_claude': Spectral_colors[9], 'approach_deepseek': Spectral_colors[10], 'approach_gpt': Spectral_colors[11],
    'agent_claude': Spectral_colors[12]
}

def normalize_setting_name(model_name: str) -> str:
    model_name = model_name.lower().replace(' ', '_').replace('-', '_')
    if 'zeroshot' in model_name or 'zero_shot' in model_name: strategy = 'zeroshot'
    elif '1shot' in model_name or 'one_shot' in model_name or 'oneshot' in model_name: strategy = '1shot'
    elif 'fewshot' in model_name or 'few_shot' in model_name: strategy = 'fewshot'
    elif 'approach' in model_name or 'archview' in model_name: strategy = 'approach'
    elif 'agent' in model_name: strategy = 'agent'
    else: return None
    
    if 'claude' in model_name: model = 'claude'
    elif 'deepseek' in model_name: model = 'deepseek'
    elif 'gpt' in model_name: model = 'gpt'
    else: return None
    return f"{strategy}_{model}"

def load_data(data_dir: Path) -> pd.DataFrame:
    rows = []
    for f in data_dir.glob("simple_table_*.csv"):
        name = f.stem.replace("simple_table_", "")
        df = pd.read_csv(f)
        if name.startswith("concern_"): category, view = 'concern', name.replace("concern_", "")
        elif name.startswith("qas_"): category, view = 'qas', name.replace("qas_", "")
        else: continue
        
        for _, row in df.iterrows():
            model_name = row['Model'].lower().replace(' ', '_').replace('-', '_')
            setting = normalize_setting_name(model_name)
            if setting is None: continue
            
            row_data = {'Setting': setting, 'Category': category, 'View': view, 'SSIM': row.get('SSIM', np.nan)}
            
            clarity = row.get('LLM_Clarity_Rating_Meets', 0) + 0.5 * row.get('LLM_Clarity_Rating_PartiallyMeets', 0)
            completeness = row.get('LLM_Completeness_Rating_Meets', 0) + 0.5 * row.get('LLM_Completeness_Rating_PartiallyMeets', 0)
            consistency = row.get('LLM_Consistency_Rating_Meets', 0) + 0.5 * row.get('LLM_Consistency_Rating_PartiallyMeets', 0)
            
            total_clarity = row.get('LLM_Clarity_Rating_Meets', 0) + row.get('LLM_Clarity_Rating_PartiallyMeets', 0) + row.get('LLM_Clarity_Rating_DoesNotMeet', 0)
            total_comp = row.get('LLM_Completeness_Rating_Meets', 0) + row.get('LLM_Completeness_Rating_PartiallyMeets', 0) + row.get('LLM_Completeness_Rating_DoesNotMeet', 0)
            total_cons = row.get('LLM_Consistency_Rating_Meets', 0) + row.get('LLM_Consistency_Rating_PartiallyMeets', 0) + row.get('LLM_Consistency_Rating_DoesNotMeet', 0)
            
            if total_clarity > 0 and total_comp > 0 and total_cons > 0:
                row_data['LLM_Composite'] = np.mean([clarity / total_clarity, completeness / total_comp, consistency / total_cons])
            else:
                row_data['LLM_Composite'] = np.nan
            rows.append(row_data)
    return pd.DataFrame(rows)

def create_heatmap(cross_df: pd.DataFrame, output_name: str, label_style: str = 'full'):
    concerns = sorted(cross_df['Concern'].unique())
    qas = sorted(cross_df['QA'].unique())
    
    qa_labels = {
        'compatibility': 'Compatibility', 'flexibility': 'Flexibility', 
        'functional_suitability': 'Func.\nSuitability', 'interaction_capability': 'Interact.\nCapability',
        'maintainability': 'Maintainability', 'performance_efficiency': 'Perf.\nEfficiency',
        'reliability': 'Reliability', 'security': 'Security'
    }
    concern_labels = {
        'connectivity': 'Connectivity', 'control_flow': 'Control Flow', 'data_flow': 'Data Flow',
        'deployment': 'Deployment', 'general': 'General', 'performance': 'Performance',
        'scheduling': 'Scheduling', 'security': 'Security'
    }

    # --- COMPACT FIGURE SIZE CALCULATION ---
    # Reduced multiplier from 1.5 -> 1.1 (Width)
    # Reduced multiplier from 1.1 -> 0.85 (Height)
    # Added +5.0 to width to safely accommodate the right-side legend
    fig_width = len(qas) * 1.1 + 5.0  
    fig_height = max(5, len(concerns) * 0.85 + 1.0)
    
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    
    pivot_settings = cross_df.pivot(index='Concern', columns='QA', values='Best_Setting')
    pivot_scores = cross_df.pivot(index='Concern', columns='QA', values='Score')
    
    label_dict = FULL_LABELS if label_style == 'full' else COMPACT_LABELS
    
    # Draw invisible base
    ax.imshow(np.zeros((len(concerns), len(qas))), aspect='auto', alpha=0)
    
    for i, concern in enumerate(concerns):
        for j, qa in enumerate(qas):
            if concern in pivot_settings.index and qa in pivot_settings.columns:
                setting = pivot_settings.loc[concern, qa]
                score = pivot_scores.loc[concern, qa]
                
                if pd.notna(setting) and setting != 'N/A' and pd.notna(score):
                    label = label_dict.get(setting, setting)
                    color = CONFIG_COLORS.get(setting, 'white')
                    text = f"{label}\n{score:.3f}"
                else:
                    color = 'white'
                    text = ""
            else:
                color = 'white'
                text = ""

            # Draw Box
            ax.add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1, 
                                      facecolor=color, edgecolor='gray', linewidth=1.5))
            
            # Add Text inside box
            if text:
                # Keep box text size reasonable so it fits in the tighter box
                fontsize = 10 if label_style == 'full' else 12
                ax.text(j, i, text, ha='center', va='center', 
                       fontsize=fontsize, fontweight='bold', color='black', linespacing=1.1)
    
    # --- INCREASED AXIS FONTS ---
    ax.set_xticks(range(len(qas)))
    ax.set_yticks(range(len(concerns)))
    
    # Ticks: 13pt (Big)
    ax.set_xticklabels([qa_labels.get(qa, qa) for qa in qas], rotation=00, ha='center', fontsize=10, fontweight='bold')
    ax.set_yticklabels([concern_labels.get(c, c) for c in concerns], rotation=65,fontsize=10, fontweight='bold')
    
    ax.set_xlim(-0.5, len(qas)-0.5)
    ax.set_ylim(len(concerns)-0.5, -0.5)
    
    # Labels: 16pt (Larger)
    ax.set_xlabel('Quality Attribute', fontsize=10, fontweight='bold', labelpad=12)
    ax.set_ylabel('Concern', fontsize=10, fontweight='bold', labelpad=12)

    # Grid and Spines
    ax.set_xticks([x + 0.5 for x in range(len(qas)-1)], minor=True)
    ax.set_yticks([y + 0.5 for y in range(len(concerns)-1)], minor=True)
    ax.grid(which='minor', color='gray', linestyle='-', linewidth=1.5)
    for spine in ax.spines.values():
        spine.set_linewidth(2)

    # --- LEGEND: RIGHT SIDE, BOTTOM ALIGNED ---
    selected_settings = [
        "1shot_deepseek", "1shot_gpt",
        "fewshot_claude", "fewshot_deepseek", "fewshot_gpt",
        "approach_claude", "approach_gpt"
    ]
    
    legend_handles = []
    legend_labels = []
    
    for setting in selected_settings:
        if setting not in CONFIG_COLORS: continue
        color = CONFIG_COLORS[setting]
        label = FULL_LABELS[setting].replace("\n", " ") if label_style == "full" else COMPACT_LABELS[setting]
        
        legend_handles.append(Line2D([0], [0], marker='s', markersize=10, linestyle='none', 
                                    markerfacecolor=color, markeredgecolor='black', markeredgewidth=1))
        legend_labels.append(label)
    
    # Position: Outside Right (x=1.02), Bottom Aligned (y=0)
    legend = ax.legend(
        legend_handles, legend_labels,
        loc='lower left',             
        bbox_to_anchor=(1.02, 0),    
        ncol=1,                        
        fontsize=10,                   
        title="Settings",
        title_fontsize=10,             
        frameon=False,
        labelspacing=0.8               
    )
    for text in legend.get_texts():
        text.set_fontweight("bold")
    legend.get_title().set_fontweight("bold")

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f'crosstable_{output_name}_{label_style}.png', dpi=300, bbox_inches='tight')
    plt.savefig(OUTPUT_DIR / f'crosstable_{output_name}_{label_style}.pdf', bbox_inches='tight')
    plt.close()
    print(f"  ✓ Saved: crosstable_{output_name}_{label_style}")

def create_publication_crosstable(df: pd.DataFrame, metric: str = 'LLM_Composite', output_name: str = 'llm', label_style: str = 'full'):
    concern_df = df[df['Category'] == 'concern']
    qas_df = df[df['Category'] == 'qas']
    concerns, qas = sorted(concern_df['View'].unique()), sorted(qas_df['View'].unique())
    
    cross_results = []
    for concern in concerns:
        for qa in qas:
            concern_data = concern_df[concern_df['View'] == concern].groupby('Setting')[metric].mean()
            qa_data = qas_df[qas_df['View'] == qa].groupby('Setting')[metric].mean()
            common_settings = set(concern_data.index) & set(qa_data.index)
            
            best_setting, best_score = 'N/A', -np.inf
            for setting in common_settings:
                c, q = concern_data.get(setting, np.nan), qa_data.get(setting, np.nan)
                if pd.notna(c) and pd.notna(q):
                    combined = (c + q) / 2
                    if combined > best_score: best_score, best_setting = combined, setting
            
            cross_results.append({'Concern': concern, 'QA': qa, 'Best_Setting': best_setting if best_setting else 'N/A', 'Score': best_score if best_score > -np.inf else np.nan})
            
    create_heatmap(pd.DataFrame(cross_results), output_name, label_style)

def create_combined_metric(df: pd.DataFrame):
    df = df.copy()
    llm_min, llm_max = df['LLM_Composite'].min(), df['LLM_Composite'].max()
    df['LLM_Normalized'] = (df['LLM_Composite'] - llm_min) / (llm_max - llm_min)
    df['Combined'] = (df['SSIM'] + df['LLM_Normalized']) / 2
    return df

def main(data_dir: str):
    data_path = Path(data_dir)
    print("Generating Publication Cross-Tables (Compact Boxes, Large Axis Fonts)...")
    df = load_data(data_path)
    
    create_publication_crosstable(df, metric='LLM_Composite', output_name='llm', label_style='full')
    create_publication_crosstable(df, metric='SSIM', output_name='ssim', label_style='full')
    
    df_combined = create_combined_metric(df)
    create_publication_crosstable(df_combined, metric='Combined', output_name='combined', label_style='full')
    print("Done.")

if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else ".")