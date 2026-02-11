import pandas as pd
from pathlib import Path

def combine_rows_horizontally():
    """
    Combine 13 CSV files by taking row 1 from all files, row 2 from all files, etc.
    Each row in the output will have columns from all 13 input files.
    """
    
    # List of files in order
    csv_files = [
        'combined_data_1shot_Claude.csv',
        'combined_data_1shot_deepseek.csv',
        'combined_data_1shot_gpt.csv',
        'combined_data_agent_claude.csv',
        'combined_data_approach_claude.csv',
        'combined_data_approach_deepseek.csv',
        'combined_data_approach_gpt.csv',
        'combined_data_fewshot_claude.csv',
        'combined_data_fewshot_deepseek.csv',
        'combined_data_fewshot_gpt.csv',
        'combined_data_zeroshot_claude.csv',
        'combined_data_zeroshot_deepseek.csv',
        'combined_data_zeroshot_gpt.csv',
    ]
    
    # Model names for better column labeling
    model_names = {
        'combined_data_1shot_Claude.csv': '1shot_claude',
        'combined_data_1shot_deepseek.csv': '1shot_deepseek',
        'combined_data_1shot_gpt.csv': '1shot_gpt',
        'combined_data_agent_claude.csv': 'agent_claude',
        'combined_data_approach_claude.csv': 'approach_claude',
        'combined_data_approach_deepseek.csv': 'approach_deepseek',
        'combined_data_approach_gpt.csv': 'approach_gpt',
        'combined_data_fewshot_claude.csv': 'fewshot_claude',
        'combined_data_fewshot_deepseek.csv': 'fewshot_deepseek',
        'combined_data_fewshot_gpt.csv': 'fewshot_gpt',
        'combined_data_zeroshot_claude.csv': 'zeroshot_claude',
        'combined_data_zeroshot_deepseek.csv': 'zeroshot_deepseek',
        'combined_data_zeroshot_gpt.csv': 'zeroshot_gpt',
    }
    
    print("=" * 80)
    print("COMBINING ROWS HORIZONTALLY FROM 13 FILES")
    print("=" * 80)
    
    # Check which files exist
    existing_files = []
    missing_files = []
    
    for f in csv_files:
        if Path(f).exists():
            existing_files.append(f)
            print(f"  ✓ Found: {f}")
        else:
            missing_files.append(f)
            print(f"  ✗ Missing: {f}")
    
    if missing_files:
        print(f"\n⚠ Warning: {len(missing_files)} files not found.")
    
    if not existing_files:
        print("\n❌ Error: No CSV files found!")
        return
    
    print(f"\n{'=' * 80}")
    print("READING ALL FILES")
    print(f"{'=' * 80}")
    
    # Read all files
    dataframes = []
    for i, csv_file in enumerate(existing_files, 1):
        print(f"\n[{i}/{len(existing_files)}] Reading: {csv_file}")
        df = pd.read_csv(csv_file)
        print(f"  Rows: {len(df)}, Columns: {len(df.columns)}")
        
        # Get model name
        model_name = model_names.get(csv_file, f'model{i}')
        
        # Base columns to keep from first file only
        base_columns = ['Repository Name', 'Clean_Repo_Name', 'repo_url', 'summary_token_count', 
                       'Concern', 'Behavior', 'Architecture Scope', 'Architectural Notation',
                       'Architectural Styles', 'QAs', 'Granularity', 'Components Nature',
                       'Connectors Nature', 'Shapes', 'Colored?', 'Connectors Direction',
                       'Legend?', 'Nested Components?', 'Explicit Ports/Interfaces?',
                       'Explicit Connectors?', 'Design Overlays', 'Technologies', 'Notes']
        
        if i == 1:
            # First file: keep base columns + rename metric columns
            metric_cols = [col for col in df.columns if col not in base_columns]
            
            # Clean existing prefixes from metric columns
            cleaned_cols = {}
            for col in metric_cols:
                clean_col = col
                # Remove prefixes like 'oneShot_claude_', 'zeroShot_deepseek_', etc.
                for prefix in ['zeroShot_', 'oneShot_', 'fewShot_', 'agent_', 'approach_']:
                    for model in ['claude_', 'deepseek_', 'gpt_']:
                        pattern = prefix + model
                        if clean_col.startswith(pattern):
                            clean_col = clean_col[len(pattern):]
                            break
                cleaned_cols[col] = f"{model_name}_{clean_col}"
            
            # Rename metric columns
            df = df.rename(columns=cleaned_cols)
            dataframes.append(df)
            print(f"  Model: {model_name}")
            print(f"  Kept all {len(df.columns)} columns (base + metrics)")
        else:
            # Other files: only keep metric columns (drop base columns)
            metric_cols = [col for col in df.columns if col not in base_columns]
            
            # Clean existing prefixes from metric columns
            cleaned_cols = {}
            for col in metric_cols:
                clean_col = col
                # Remove prefixes
                for prefix in ['zeroShot_', 'oneShot_', 'fewShot_', 'agent_', 'approach_']:
                    for model in ['claude_', 'deepseek_', 'gpt_']:
                        pattern = prefix + model
                        if clean_col.startswith(pattern):
                            clean_col = clean_col[len(pattern):]
                            break
                cleaned_cols[col] = f"{model_name}_{clean_col}"
            
            # Keep only metric columns and rename them
            df = df[metric_cols].rename(columns=cleaned_cols)
            dataframes.append(df)
            print(f"  Model: {model_name}")
            print(f"  Kept {len(df.columns)} metric columns only")
    
    print(f"\n{'=' * 80}")
    print("CONCATENATING ROWS HORIZONTALLY")
    print(f"{'=' * 80}")
    
    # Verify all dataframes have the same number of rows
    row_counts = [len(df) for df in dataframes]
    print(f"\nRow counts: {row_counts}")
    
    if len(set(row_counts)) > 1:
        print(f"\n⚠️  WARNING: Files have different row counts!")
        print(f"  Min: {min(row_counts)}, Max: {max(row_counts)}")
        print(f"  Will use first {min(row_counts)} rows from each file.")
        # Truncate all dataframes to the minimum row count
        min_rows = min(row_counts)
        dataframes = [df.iloc[:min_rows] for df in dataframes]
    else:
        print(f"✅ All files have {row_counts[0]} rows - perfect!")
    
    # Concatenate horizontally (axis=1)
    print(f"\nConcatenating {len(dataframes)} dataframes horizontally...")
    combined_df = pd.concat(dataframes, axis=1)
    
    print(f"  Result: {len(combined_df)} rows × {len(combined_df.columns)} columns")
    
    # Write output
    output_file = 'final_combined_all_models.csv'
    
    print(f"\n{'=' * 80}")
    print("WRITING OUTPUT")
    print(f"{'=' * 80}")
    print(f"Output file: {output_file}")
    print(f"Total rows: {len(combined_df)}")
    print(f"Total columns: {len(combined_df.columns)}")
    
    combined_df.to_csv(output_file, index=False)
    
    print(f"\n✓ Successfully combined {len(existing_files)} CSV files!")
    
    # Statistics
    print(f"\n{'=' * 80}")
    print("SUMMARY")
    print(f"{'=' * 80}")
    
    print(f"\nColumn breakdown:")
    print(f"  Base columns: ~23 (from first file)")
    for i, csv_file in enumerate(existing_files):
        model_name = model_names.get(csv_file, f'model{i+1}')
        model_cols = [col for col in combined_df.columns if col.startswith(f"{model_name}_")]
        print(f"  {model_name}: {len(model_cols)} columns")
    
    print(f"\nTotal: {len(combined_df.columns)} columns")
    print(f"\n{'=' * 80}")
    print(f"✓ COMPLETE! Output saved to: {output_file}")
    print(f"{'=' * 80}")

if __name__ == "__main__":
    combine_rows_horizontally()