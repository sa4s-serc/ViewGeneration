import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ==============================================================
#  LOAD ALL THREE LEVEL CSVs
# ==============================================================

level_files = {
    "Level 1": "simple_table_high.csv",
    "Level 2": "simple_table_low.csv",
    "Level 3": "simple_table_medium.csv"
}

dfs = []
for level, file in level_files.items():
    df = pd.read_csv(file)
    df["Level"] = level
    dfs.append(df)

# merged dataset
df = pd.concat(dfs, ignore_index=True)

# ==============================================================
#   COLUMN GROUPS
# ==============================================================

clarity_cols = [
    "LLM_Clarity_Rating_DoesNotMeet",
    "LLM_Clarity_Rating_Meets",
    "LLM_Clarity_Rating_PartiallyMeets"
]

completeness_cols = [
    "LLM_Completeness_Rating_DoesNotMeet",
    "LLM_Completeness_Rating_Meets",
    "LLM_Completeness_Rating_PartiallyMeets"
]

consistency_cols = [
    "LLM_Consistency_Rating_DoesNotMeet",
    "LLM_Consistency_Rating_Meets",
    "LLM_Consistency_Rating_PartiallyMeets"
]

metrics = {
    "Clarity": clarity_cols,
    "Completeness": completeness_cols,
    "Consistency": consistency_cols
}

rating_map = {
    "DoesNotMeet": "Does Not Meet",
    "Meets": "Meets",
    "PartiallyMeets": "Partially Meets"
}

# ==============================================================
# 1. PER LLM × PER METRIC × PER RATING TYPE ACROSS LEVELS
# ==============================================================

def plot_llm_metric_across_levels():
    for metric_name, cols in metrics.items():
        for rating_col in cols:

            rating_label = rating_col.split("_")[-1]
            rating_label = rating_map[rating_label]

            plt.figure(figsize=(14,6))
            sns.barplot(
                data=df,
                x="Model",
                y=rating_col,
                hue="Level"
            )

            plt.title(f"{metric_name} — {rating_label} Across Levels")
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()

            plt.savefig(f"./images/{metric_name}_{rating_label.replace(' ','_')}_across_levels.png", dpi=300)
            plt.close()

# ==============================================================
# 2. METRIC COMPARISON (LLMs × Levels) — GROUPED BARS
# ==============================================================

def plot_metric_grouped(metric_name, cols):

    melted = df.melt(
        id_vars=["Model", "Level"],
        value_vars=cols,
        var_name="Rating",
        value_name="Count"
    )

    melted["Rating"] = melted["Rating"].apply(
        lambda x: rating_map[x.split("_")[-1]]
    )

    plt.figure(figsize=(14,6))
    sns.barplot(data=melted, x="Model", y="Count", hue="Level")

    plt.title(f"{metric_name} Comparison Across Levels (Total Count)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    plt.savefig(f"./images/{metric_name}_grouped_across_levels.png", dpi=300)
    plt.close()


# ==============================================================
# 3. STACKED BARS PER LLM PER LEVEL
# ==============================================================

def plot_stacked(metric_name, cols):

    for level in df["Level"].unique():

        dsub = df[df["Level"] == level][["Model"] + cols].set_index("Model")

        labels = ["Does Not Meet", "Meets", "Partially Meets"]
        colmap = dict(zip(cols, labels))

        plt.figure(figsize=(14,6))
        bottom = None

        for col in cols:
            plt.bar(
                dsub.index,
                dsub[col],
                bottom=bottom,
                label=colmap[col]
            )
            bottom = dsub[col] if bottom is None else bottom + dsub[col]

        plt.title(f"{metric_name} — Stacked Ratings ({level})")
        plt.xticks(rotation=45, ha="right")
        plt.ylabel("Raw Count")
        plt.legend()
        plt.tight_layout()

        plt.savefig(f"./images/{metric_name}_stacked_{level.replace(' ','_')}.png", dpi=300)
        plt.close()

# ==============================================================
# 4. RADAR CHARTS — MEETS ACROSS LEVELS FOR EACH LLM
# ==============================================================

def radar_charts():

    meets_cols = {
        "Clarity": "LLM_Clarity_Rating_Meets",
        "Completeness": "LLM_Completeness_Rating_Meets",
        "Consistency": "LLM_Consistency_Rating_Meets"
    }

    labels = list(meets_cols.keys())
    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    for model in df["Model"].unique():

        model_data = df[df["Model"] == model]

        for level in model_data["Level"].unique():

            row = model_data[model_data["Level"] == level][meets_cols.values()].iloc[0]
            values = row.tolist()
            values += values[:1]

            plt.figure(figsize=(6,6))
            ax = plt.subplot(111, polar=True)

            ax.plot(angles, values, linewidth=2)
            ax.fill(angles, values, alpha=0.25)

            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(labels)

            plt.title(f"{model} — Meets Radar ({level})")
            plt.tight_layout()
            plt.savefig(f"./images/{model}_radar_{level.replace(' ','_')}.png", dpi=300)
            plt.close()

# ==============================================================
# RUN EVERYTHING
# ==============================================================

plot_llm_metric_across_levels()

for metric_name, cols in metrics.items():
    plot_metric_grouped(metric_name, cols)
    plot_stacked(metric_name, cols)

radar_charts()

print("Generated ALL inter-level comparison plots.")
