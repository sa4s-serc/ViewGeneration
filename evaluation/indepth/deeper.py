import pandas as pd
import numpy as np

def create_simple_tables():
    """
    Read final_combined_all_models.csv and create 3 tables:
    - One for high, one for medium, one for low
    - Rows = 13 models
    - Columns = metrics (averages for numeric, counts for ratings)
    """
    
    print("=" * 80)
    print("CREATING SIMPLE TABLES")
    print("=" * 80)
    
    # Read the combined CSV
    df = pd.read_csv('final_combined_all_models.csv')
    
    print(f"\nTotal rows: {len(df)}")
    print(f"Total columns: {len(df.columns)}")
    
    # Define the 13 model prefixes - MUST MATCH ACTUAL COLUMN NAMES
    model_prefixes = [
        '1shot_claude',
        '1shot_deepseek',
        '1shot_gpt',
        'agent_claude',  # Capital A!
        'approach_claude',
        'approach_deepseek',
        'approach_gpt',
        'fewshot_claude',
        'fewshot_deepseek',
        'fewshot_gpt',
        'zeroshot_claude',
        'zeroshot_deepseek',  # Underscore in "zeroshot"!
        'zeroshot_gpt'
    ]
    
    print(f"\nModels: {len(model_prefixes)}")
    
    # Create tables for each granularity level
    granularity_levels = ['high', 'medium', 'low']
    
    for granularity in granularity_levels:
        print(f"\n{'=' * 80}")
        print(f"CREATING TABLE FOR: {granularity.upper()}")
        print(f"{'=' * 80}")
        
        # Filter by granularity
        subset = df[df['Granularity'] == granularity]
        print(f"Rows in {granularity}: {len(subset)}")
        
        if len(subset) == 0:
            print(f"  ⚠️  No data for {granularity}, skipping...")
            continue
        
        # Build table
        table_rows = []
        
        for model_prefix in model_prefixes:
            print(f"  Processing: {model_prefix}")
            row = {'Model': model_prefix}
            
            # Find all columns for this model
            model_columns = [col for col in df.columns if col.startswith(f"{model_prefix}_")]
            
            print(f"    Found {len(model_columns)} columns")
            
            for col in model_columns:
                # Extract the metric name by removing the model prefix
                metric_name = col.replace(f"{model_prefix}_", "")
                
                # Check if this is an LLM rating column
                if 'LLM_' in metric_name and 'Rating' in metric_name:
                    # This is a rating column - count values
                    values = subset[col].dropna()
                    
                    if len(values) > 0:
                        value_counts = values.value_counts()
                        
                        # Count each rating type
                        row[f"{metric_name}_DoesNotMeet"] = value_counts.get('Does Not Meet Expectations', 0)
                        row[f"{metric_name}_PartiallyMeets"] = value_counts.get('Partially Meets Expectations', 0)
                        row[f"{metric_name}_Meets"] = value_counts.get('Meets Expectations', 0)
                    else:
                        row[f"{metric_name}_DoesNotMeet"] = 0
                        row[f"{metric_name}_PartiallyMeets"] = 0
                        row[f"{metric_name}_Meets"] = 0
                
                elif any(m in metric_name for m in ['SSIM', 'PSNR', 'RMSE', 'SAM', 'SRE', 'UIQ']):
                    # This is a numeric metric - calculate average
                    values = subset[col].dropna()
                    
                    if len(values) > 0:
                        row[metric_name] = values.mean()
                    else:
                        row[metric_name] = np.nan
            
            table_rows.append(row)
        
        # Create DataFrame
        table_df = pd.DataFrame(table_rows)
        
        # Reorder columns: Model first, then SSIM, PSNR, etc., then LLM ratings
        base_cols = ['Model']
        numeric_cols = [col for col in table_df.columns if any(m in col for m in ['SSIM', 'PSNR', 'RMSE', 'SAM', 'SRE', 'UIQ']) and 'LLM' not in col]
        llm_cols = [col for col in table_df.columns if 'LLM' in col]
        
        ordered_cols = base_cols + sorted(numeric_cols) + sorted(llm_cols)
        table_df = table_df[ordered_cols]
        
        # Save to CSV
        output_file = f'simple_table_{granularity}.csv'
        table_df.to_csv(output_file, index=False)
        
        print(f"\n  ✓ Saved: {output_file}")
        print(f"  Shape: {len(table_df)} rows × {len(table_df.columns)} columns")
        
        # Show column breakdown
        print(f"\n  Column breakdown:")
        print(f"    - Numeric metrics: {len(numeric_cols)}")
        print(f"    - LLM rating columns: {len(llm_cols)}")
        
        # Show sample numeric columns
        print(f"\n  Sample numeric columns:")
        for col in sorted(numeric_cols)[:5]:
            print(f"    {col}")
        
        # Show sample LLM columns
        print(f"\n  Sample LLM rating columns:")
        for col in sorted(llm_cols)[:5]:
            print(f"    {col}")
        
        # Show preview of data
        print(f"\n  Preview (first 3 models, first 8 columns):")
        preview_cols = table_df.columns[:8]
        print(table_df[preview_cols].head(3).to_string(index=False))
    
    print(f"\n{'=' * 80}")
    print("✓ COMPLETE!")
    print(f"{'=' * 80}")
    print(f"\nGenerated files:")
    print(f"  - simple_table_high.csv")
    print(f"  - simple_table_medium.csv")
    print(f"  - simple_table_low.csv")
    
    print(f"\nEach table has:")
    print(f"  - 13 rows (one per model)")
    print(f"  - Numeric metrics: average values")
    print(f"  - LLM ratings: counts (DoesNotMeet, PartiallyMeets, Meets, Exceeds)")

if __name__ == "__main__":
    create_simple_tables()


import pandas as pd
import numpy as np

def create_simple_tables():
    """
    Read final_combined_all_models.csv and create 3 tables:
    - one for each Architecture Scope: entire, part, entire+
    - Rows = 13 models
    - Columns = metrics (averages for numeric, counts for ratings)
    """
    
    print("=" * 80)
    print("CREATING SIMPLE TABLES (ARCHITECTURE SCOPE)")
    print("=" * 80)
    
    # Read the combined CSV
    df = pd.read_csv('final_combined_all_models.csv')
    
    print(f"\nTotal rows: {len(df)}")
    print(f"Total columns: {len(df.columns)}")
    
    # Hardcoded 13 model prefixes
    model_prefixes = [
        '1shot_claude',
        '1shot_deepseek',
        '1shot_gpt',
        'agent_claude',
        'approach_claude',
        'approach_deepseek',
        'approach_gpt',
        'fewshot_claude',
        'fewshot_deepseek',
        'fewshot_gpt',
        'zeroshot_claude',
        'zeroshot_deepseek',
        'zeroshot_gpt'
    ]
    
    print(f"\nModels: {len(model_prefixes)}")
    
    # NEW: Architecture Scope categories
    scope_levels = ['entire', 'part', 'entire+']
    
    for scope in scope_levels:
        print(f"\n{'=' * 80}")
        print(f"CREATING TABLE FOR ARCHITECTURE SCOPE: {scope.upper()}")
        print(f"{'=' * 80}")
        
        # Filter by Architecture Scope (not granularity anymore)
        subset = df[df['Architecture Scope'] == scope]
        print(f"Rows in {scope}: {len(subset)}")
        
        if len(subset) == 0:
            print(f"  ⚠️  No data for {scope}, skipping...")
            continue
        
        table_rows = []
        
        for model_prefix in model_prefixes:
            print(f"  Processing: {model_prefix}")
            row = {'Model': model_prefix}
            
            model_columns = [col for col in df.columns if col.startswith(f"{model_prefix}_")]
            print(f"    Found {len(model_columns)} columns")
            
            for col in model_columns:
                metric_name = col.replace(f"{model_prefix}_", "")
                
                # LLM rating column
                if 'LLM_' in metric_name and 'Rating' in metric_name:
                    values = subset[col].dropna()
                    
                    if len(values) > 0:
                        counts = values.value_counts()
                        row[f"{metric_name}_DoesNotMeet"] = counts.get('Does Not Meet Expectations', 0)
                        row[f"{metric_name}_PartiallyMeets"] = counts.get('Partially Meets Expectations', 0)
                        row[f"{metric_name}_Meets"] = counts.get('Meets Expectations', 0)
                    else:
                        row[f"{metric_name}_DoesNotMeet"] = 0
                        row[f"{metric_name}_PartiallyMeets"] = 0
                        row[f"{metric_name}_Meets"] = 0
                
                # Numeric metrics
                elif any(m in metric_name for m in ['SSIM', 'PSNR', 'RMSE', 'SAM', 'SRE', 'UIQ']):
                    values = subset[col].dropna()
                    row[metric_name] = values.mean() if len(values) > 0 else np.nan
            
            table_rows.append(row)
        
        table_df = pd.DataFrame(table_rows)
        
        base_cols = ['Model']
        numeric_cols = [
            col for col in table_df.columns 
            if any(m in col for m in ['SSIM', 'PSNR', 'RMSE', 'SAM', 'SRE', 'UIQ']) and 'LLM' not in col
        ]
        llm_cols = [col for col in table_df.columns if 'LLM' in col]
        
        ordered_cols = base_cols + sorted(numeric_cols) + sorted(llm_cols)
        table_df = table_df[ordered_cols]
        
        output_file = f'simple_table_scope_{scope}.csv'
        table_df.to_csv(output_file, index=False)
        
        print(f"\n  ✓ Saved: {output_file}")
        print(f"  Shape: {len(table_df)} rows × {len(table_df.columns)} columns")
        
        print(f"\n  Column breakdown:")
        print(f"    - Numeric metrics: {len(numeric_cols)}")
        print(f"    - LLM rating columns: {len(llm_cols)}")
        
        print(f"\n  Preview (first 3 models, first 8 columns):")
        preview_cols = table_df.columns[:8]
        print(table_df[preview_cols].head(3).to_string(index=False))
    
    print(f"\n{'=' * 80}")
    print("✓ COMPLETE! (ARCHITECTURE SCOPE)")
    print("=" * 80)


if __name__ == "__main__":
    create_simple_tables()


import pandas as pd
import numpy as np

def create_simple_tables_arch_notation():
    """
    Read final_combined_all_models.csv and create tables grouped by Architectural Notation.
    - Rows = 13 models
    - Columns = metrics (averages for numeric, counts for ratings)
    """

    print("=" * 80)
    print("CREATING SIMPLE TABLES (ARCHITECTURAL NOTATION)")
    print("=" * 80)

    df = pd.read_csv('final_combined_all_models.csv')

    print(f"\nTotal rows: {len(df)}")
    print(f"Total columns: {len(df.columns)}")

    # 13 fixed model prefixes (unchanged)
    model_prefixes = [
        '1shot_claude',
        '1shot_deepseek',
        '1shot_gpt',
        'agent_claude',
        'approach_claude',
        'approach_deepseek',
        'approach_gpt',
        'fewshot_claude',
        'fewshot_deepseek',
        'fewshot_gpt',
        'zeroshot_claude',
        'zeroshot_deepseek',
        'zeroshot_gpt'
    ]

    print(f"\nModels: {len(model_prefixes)}")

    # Architectural Notation groups
    notation_levels = [
        'boxes_and_arrows',
        'icons_and_arrows',
        'boxes',
        'UML',
        'icons_and_arrows, boxes',
        'boxes_and_arrows, icons_and_arrows',
        'boxes, icons_and_arrows',
        'boxes_and_arrows, boxes',
        'boxes, boxes_and_arrows'
    ]

    for notation in notation_levels:
        print(f"\n{'=' * 80}")
        print(f"CREATING TABLE FOR ARCHITECTURAL NOTATION: {notation}")
        print(f"{'=' * 80}")

        subset = df[df['Architectural Notation'] == notation]
        print(f"Rows in {notation}: {len(subset)}")

        if len(subset) == 0:
            print(f"  ⚠️ No data for {notation}, skipping...")
            continue

        table_rows = []

        for model_prefix in model_prefixes:
            print(f"  Processing: {model_prefix}")
            row = {'Model': model_prefix}

            model_columns = [
                col for col in df.columns if col.startswith(f"{model_prefix}_")
            ]
            print(f"    Found {len(model_columns)} columns")

            for col in model_columns:
                metric_name = col.replace(f"{model_prefix}_", "")

                # LLM rating columns
                if 'LLM_' in metric_name and 'Rating' in metric_name:
                    values = subset[col].dropna()
                    if len(values) > 0:
                        counts = values.value_counts()
                        row[f"{metric_name}_DoesNotMeet"] = counts.get('Does Not Meet Expectations', 0)
                        row[f"{metric_name}_PartiallyMeets"] = counts.get('Partially Meets Expectations', 0)
                        row[f"{metric_name}_Meets"] = counts.get('Meets Expectations', 0)
                    else:
                        row[f"{metric_name}_DoesNotMeet"] = 0
                        row[f"{metric_name}_PartiallyMeets"] = 0
                        row[f"{metric_name}_Meets"] = 0

                # Numeric metrics
                elif any(m in metric_name for m in ['SSIM', 'PSNR', 'RMSE', 'SAM', 'SRE', 'UIQ']):
                    values = subset[col].dropna()
                    row[metric_name] = values.mean() if len(values) > 0 else np.nan

            table_rows.append(row)

        table_df = pd.DataFrame(table_rows)

        # Column organization
        base_cols = ['Model']
        numeric_cols = [
            col for col in table_df.columns
            if any(m in col for m in ['SSIM', 'PSNR', 'RMSE', 'SAM', 'SRE', 'UIQ'])
            and 'LLM' not in col
        ]
        llm_cols = [col for col in table_df.columns if 'LLM' in col]

        ordered_cols = base_cols + sorted(numeric_cols) + sorted(llm_cols)
        table_df = table_df[ordered_cols]

        # Save
        output_file = f"simple_table_archnotation_{notation.replace(',', '_').replace(' ', '')}.csv"
        table_df.to_csv(output_file, index=False)

        print(f"\n  ✓ Saved: {output_file}")
        print(f"  Shape: {len(table_df)} rows × {len(table_df.columns)} columns")

        # Preview
        preview_cols = table_df.columns[:8]
        print("\n  Preview (first 3 models, first 8 columns):")
        print(table_df[preview_cols].head(3).to_string(index=False))

    print("\n" + "=" * 80)
    print("✓ COMPLETE! (ARCHITECTURAL NOTATION TABLES)")
    print("=" * 80)


if __name__ == "__main__":
    create_simple_tables_arch_notation()

import pandas as pd
import numpy as np

def create_simple_tables_concern():
    """
    Creates tables for each atomic Concern value.
    Handles rows with multiple concerns by splitting them.
    For each concern:
       - Rows = 13 models
       - Columns = numeric metric averages + LLM rating counts
    """

    print("=" * 80)
    print("CREATING SIMPLE TABLES (CONCERN)")
    print("=" * 80)

    df = pd.read_csv("final_combined_all_models.csv")
    print(f"\nTotal rows: {len(df)}")

    # --- Step 1: Normalize multi-concern cells ---
    print("\nExtracting unique concerns...")

    # Split by comma, strip whitespace
    df["Concern_list"] = df["Concern"].astype(str).apply(
        lambda x: [c.strip() for c in x.split(",")]
    )

    # Collect all atomic concerns
    all_concerns = sorted({c for lst in df["Concern_list"] for c in lst})
    print(f"Found {len(all_concerns)} unique concerns:")
    print(all_concerns)

    # 13 fixed model prefixes
    model_prefixes = [
        '1shot_claude', '1shot_deepseek', '1shot_gpt',
        'agent_claude',
        'approach_claude', 'approach_deepseek', 'approach_gpt',
        'fewshot_claude', 'fewshot_deepseek', 'fewshot_gpt',
        'zeroshot_claude', 'zeroshot_deepseek', 'zeroshot_gpt'
    ]

    # Process each concern separately
    for concern in all_concerns:
        print(f"\n{'=' * 80}")
        print(f"CREATING TABLE FOR CONCERN: {concern.upper()}")
        print(f"{'=' * 80}")

        # Filter rows where this concern appears
        subset = df[df["Concern_list"].apply(lambda lst: concern in lst)]
        print(f"Rows for {concern}: {len(subset)}")

        if len(subset) == 0:
            print(f"  ⚠️ No data for {concern}, skipping...")
            continue

        table_rows = []

        for model_prefix in model_prefixes:
            print(f"  Processing: {model_prefix}")
            row = {"Model": model_prefix}

            model_columns = [c for c in df.columns if c.startswith(f"{model_prefix}_")]
            print(f"    Found {len(model_columns)} columns")

            for col in model_columns:
                metric_name = col.replace(f"{model_prefix}_", "")

                # LLM rating metrics
                if "LLM_" in metric_name and "Rating" in metric_name:
                    values = subset[col].dropna()

                    if len(values) > 0:
                        counts = values.value_counts()
                        row[f"{metric_name}_DoesNotMeet"] = counts.get("Does Not Meet Expectations", 0)
                        row[f"{metric_name}_PartiallyMeets"] = counts.get("Partially Meets Expectations", 0)
                        row[f"{metric_name}_Meets"] = counts.get("Meets Expectations", 0)
                    else:
                        row[f"{metric_name}_DoesNotMeet"] = 0
                        row[f"{metric_name}_PartiallyMeets"] = 0
                        row[f"{metric_name}_Meets"] = 0

                # Numeric metrics
                elif any(k in metric_name for k in ["SSIM", "PSNR", "RMSE", "SAM", "SRE", "UIQ"]):
                    vals = subset[col].dropna()
                    row[metric_name] = vals.mean() if len(vals) > 0 else np.nan

            table_rows.append(row)

        # Build DataFrame
        table_df = pd.DataFrame(table_rows)

        # Order columns
        base_cols = ["Model"]
        numeric_cols = [
            c for c in table_df.columns
            if any(m in c for m in ["SSIM", "PSNR", "RMSE", "SAM", "SRE", "UIQ"])
            and "LLM" not in c
        ]
        llm_cols = [c for c in table_df.columns if "LLM" in c]

        ordered_cols = base_cols + sorted(numeric_cols) + sorted(llm_cols)
        table_df = table_df[ordered_cols]

        # Save CSV
        safe_concern = concern.replace(" ", "_")
        save_name = f"simple_table_concern_{safe_concern}.csv"
        table_df.to_csv(save_name, index=False)

        print(f"\n  ✓ Saved: {save_name}")
        print(f"  Shape: {table_df.shape}")

        print("\n  Preview:")
        print(table_df.head(3).to_string(index=False))

    print("\n" + "=" * 80)
    print("✓ COMPLETE! (CONCERN TABLES GENERATED)")
    print("=" * 80)


if __name__ == "__main__":
    create_simple_tables_concern()

import pandas as pd
import numpy as np

def create_simple_tables_qas():
    """
    Creates tables for each atomic QA value.
    Handles multiple QAs per row by splitting them.
    For each QA:
        - 13 rows (models)
        - Numeric averages + LLM rating counts
    """

    print("=" * 80)
    print("CREATING SIMPLE TABLES (QAs)")
    print("=" * 80)

    # Load dataset
    df = pd.read_csv("final_combined_all_models.csv")
    print(f"\nTotal rows: {len(df)}")

    # --- Normalize the 'QAs' column ---
    print("\nExtracting unique QAs...")

    # Split comma-separated values
    df["QAs_list"] = df["QAs"].astype(str).apply(
        lambda x: [qa.strip() for qa in x.split(",")]
    )

    # Collect all unique atomic QAs
    all_qas = sorted({qa for lst in df["QAs_list"] for qa in lst})
    print(f"Found {len(all_qas)} unique QAs:")
    print(all_qas)

    # 13 fixed model prefixes
    model_prefixes = [
        '1shot_claude', '1shot_deepseek', '1shot_gpt',
        'agent_claude',
        'approach_claude', 'approach_deepseek', 'approach_gpt',
        'fewshot_claude', 'fewshot_deepseek', 'fewshot_gpt',
        'zeroshot_claude', 'zeroshot_deepseek', 'zeroshot_gpt'
    ]

    # Process each QA separately
    for qa in all_qas:
        print(f"\n{'=' * 80}")
        print(f"CREATING TABLE FOR QA: {qa.upper()}")
        print(f"{'=' * 80}")

        # Filter rows where this QA appears
        subset = df[df["QAs_list"].apply(lambda lst: qa in lst)]
        print(f"Rows for {qa}: {len(subset)}")

        if len(subset) == 0:
            print(f"  ⚠️ No data for {qa}, skipping...")
            continue

        table_rows = []

        for model_prefix in model_prefixes:
            print(f"  Processing model: {model_prefix}")

            row = {"Model": model_prefix}

            # Model-specific columns
            model_columns = [c for c in df.columns if c.startswith(f"{model_prefix}_")]
            print(f"    Found {len(model_columns)} columns")

            for col in model_columns:
                metric_name = col.replace(f"{model_prefix}_", "")

                # Handle LLM rating columns
                if "LLM_" in metric_name and "Rating" in metric_name:
                    vals = subset[col].dropna()

                    if len(vals) > 0:
                        vc = vals.value_counts()
                        row[f"{metric_name}_DoesNotMeet"] = vc.get("Does Not Meet Expectations", 0)
                        row[f"{metric_name}_PartiallyMeets"] = vc.get("Partially Meets Expectations", 0)
                        row[f"{metric_name}_Meets"] = vc.get("Meets Expectations", 0)
                    else:
                        row[f"{metric_name}_DoesNotMeet"] = 0
                        row[f"{metric_name}_PartiallyMeets"] = 0
                        row[f"{metric_name}_Meets"] = 0

                # Handle numeric metrics
                elif any(k in metric_name for k in ["SSIM", "PSNR", "RMSE", "SAM", "SRE", "UIQ"]):
                    vals = subset[col].dropna()
                    row[metric_name] = vals.mean() if len(vals) > 0 else np.nan

            table_rows.append(row)

        # Build DataFrame
        table_df = pd.DataFrame(table_rows)

        # Order columns
        base_cols = ["Model"]
        numeric_cols = [
            c for c in table_df.columns
            if any(k in c for k in ["SSIM", "PSNR", "RMSE", "SAM", "SRE", "UIQ"])
            and "LLM" not in c
        ]
        llm_cols = [c for c in table_df.columns if "LLM" in c]

        ordered_cols = base_cols + sorted(numeric_cols) + sorted(llm_cols)
        table_df = table_df[ordered_cols]

        # Save file
        safe_qa = qa.replace(" ", "_")
        file_name = f"simple_table_qas_{safe_qa}.csv"
        table_df.to_csv(file_name, index=False)

        print(f"\n  ✓ Saved: {file_name}")
        print(f"  Shape: {table_df.shape}")

        print("\n  Preview:")
        print(table_df.head(3).to_string(index=False))

    print("\n" + "=" * 80)
    print("✓ COMPLETE! (QAs TABLES GENERATED)")
    print("=" * 80)


if __name__ == "__main__":
    create_simple_tables_qas()
