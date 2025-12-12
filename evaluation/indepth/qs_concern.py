import matplotlib.pyplot as plt
import numpy as np

# ==========================================
# 1. DATA ENTRY
# ==========================================
strategies = ['Few-Shot(FS)', 'Agent (GPA)', 'ArchView (AV)']
colors = ['#1f77b4', '#ff7f0e', '#2ca02c'] 

concern_categories = ['Connectivity', 'Control\nFlow', 'Data\nFlow', 'Deployment', 'General', 'Performance', 'Scheduling', 'Security']
concern_ssim_data = [[0.547, 0.521, 0.573], [0.637, 0.604, 0.659], [0.625, 0.581, 0.619], [0.600, 0.550, 0.606], [0.532, 0.503, 0.528], [0.605, 0.513, 0.558], [0.542, 0.542, 0.605], [0.588, 0.561, 0.592]]
concern_llm_data = [[0.193, 0.105, 0.180], [0.190, 0.080, 0.225], [0.184, 0.046, 0.218], [0.209, 0.106, 0.221], [0.187, 0.115, 0.184], [0.208, 0.117, 0.229], [0.042, 0.000, 0.083], [0.143, 0.078, 0.167]]

qa_categories = ['Compatibility', 'Flexibility', 'Func.\nSuitability', 'Interact.\nCap.', 'Maintainability', 'Perf.\nEfficiency', 'Reliability', 'Security']
qa_ssim_data = [[0.504, 0.498, 0.571], [0.553, 0.508, 0.574], [0.631, 0.594, 0.649], [0.567, 0.534, 0.567], [0.580, 0.548, 0.583], [0.616, 0.545, 0.599], [0.603, 0.564, 0.631], [0.566, 0.519, 0.569]]
qa_llm_data = [[0.167, 0.067, 0.222], [0.140, 0.132, 0.144], [0.194, 0.076, 0.208], [0.188, 0.067, 0.210], [0.200, 0.108, 0.210], [0.196, 0.086, 0.194], [0.190, 0.095, 0.167], [0.153, 0.117, 0.160]]

def transform_data(categories, raw_data):
    return [[raw_data[cat_idx][strat_idx] for cat_idx in range(len(categories))] for strat_idx in range(3)]

data_sets = [
    (transform_data(concern_categories, concern_ssim_data), concern_categories, "Concern - SSIM", [0.4, 0.7]),
    (transform_data(concern_categories, concern_llm_data),  concern_categories, "Concern - LLM Quality", [0, 0.25]),
    (transform_data(qa_categories, qa_ssim_data),           qa_categories,      "Quality Attr. - SSIM", [0.4, 0.7]),
    (transform_data(qa_categories, qa_llm_data),            qa_categories,      "Quality Attr. - LLM Quality", [0, 0.25]),
]

# ==========================================
# 2. PLOTTING
# ==========================================
plt.rcParams['font.family'] = 'sans-serif'
# Increase figure height slightly to accommodate labels
fig, axs = plt.subplots(1, 4, figsize=(26, 9), subplot_kw=dict(polar=True))

# Increase wspace (width space) to stop labels from hitting neighbor plots
plt.subplots_adjust(wspace=0.4, left=0.05, right=0.95, top=0.80, bottom=0.15)

for idx, (data, categories, title, ylims) in enumerate(data_sets):
    ax = axs[idx]
    N = len(categories)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += [angles[0]] 
    
    # --- Plot Data ---
    for i, strategy in enumerate(strategies):
        values = data[i] + [data[i][0]]
        ax.plot(angles, values, color=colors[i], linewidth=3, label=strategy, marker='o', markersize=6)
        ax.fill(angles, values, color=colors[i], alpha=0.1)
    
    # --- Axis Setup ---
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    
    # Turn off default tick labels so we can replace them manually
    ax.set_xticklabels([])
    
    ax.set_ylim(ylims)
    ticks = np.linspace(ylims[0], ylims[1], 5)
    ax.set_yticks(ticks)
    ax.set_yticklabels([f"{t:.2f}" for t in ticks], size=9, color='grey')
    ax.grid(color='#D3D3D3', linestyle='-', linewidth=1.0)
    ax.spines['polar'].set_visible(False) 
    
    # Move title up further to avoid hitting top labels
    ax.set_title(title, size=18, weight='bold', pad=50)

    # --- MANUAL LABEL PLACEMENT ---
    # Define a padding distance (r_label) slightly outside the max ylim
    # Increasing this pushes text further away from the center
    label_padding = (ylims[1] - ylims[0]) * 0.15
    r_label = ylims[1] + label_padding

    for label, angle in zip(categories, angles[:-1]):
        angle_deg = np.degrees(angle)
        
        # 1. Base Rotation: Tangential
        rotation = -angle_deg
        
        # 2. Flip Logic: Keep text readable (not upside down)
        if 90 < angle_deg < 270:
            rotation += 180
            
        # 3. Place Text
        # va='bottom' ensures the text "sits" on the imaginary circle defined by r_label
        # This pushes it outward regardless of rotation.
        ax.text(
            angle, r_label, label, 
            size=13,
            rotation=rotation,
            rotation_mode='anchor', 
            ha='center', va='bottom' 
        )

# Legend
handles, labels = axs[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, 0.02), 
           ncol=3, fontsize=25, frameon=True, fancybox=True, edgecolor='black')

# Save
plt.savefig('radar_charts_fixed.pdf', format='pdf', bbox_inches='tight')
print("PDF saved as: radar_charts_fixed.pdf")
plt.show()