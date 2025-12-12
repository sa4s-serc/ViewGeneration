import pandas as pd
import os

def analyze_all_justification_files(directory='./'):
    """
    Analyze agreement in all justification CSV files.
    """
    files = [
        'clarity_justifications.csv',
        'completeness_justifications.csv',
        'consistency_justifications.csv',
        'accuracy_justifications.csv',
        'detail_justifications.csv'
    ]
    
    print("\n" + "="*80)
    print("DISAGREEMENT ANALYSIS ACROSS ALL DIMENSIONS")
    print("="*80)
    
    total_disagreements = 0
    total_evaluations = 0
    
    for filename in files:
        filepath = os.path.join(directory, filename)
        
        if not os.path.exists(filepath):
            print(f"\nWarning: {filepath} not found, skipping...")
            continue
        
        df = pd.read_csv(filepath)
        
        # Determine the agreement column name
        if 'agreement_match' in df.columns:
            agree_col = 'agreement_match'
        elif 'rating_match' in df.columns:
            agree_col = 'rating_match'
        else:
            print(f"\nWarning: No agreement column found in {filename}")
            continue
        
        false_count = (df[agree_col] == False).sum()
        true_count = (df[agree_col] == True).sum()
        total = len(df)
        
        dimension = filename.replace('_justifications.csv', '').capitalize()
        
        print(f"\n{dimension}:")
        print(f"  Disagreements: {false_count:3d} / {total:3d} ({false_count/total*100:5.1f}%)")
        print(f"  Agreements:    {true_count:3d} / {total:3d} ({true_count/total*100:5.1f}%)")
        
        total_disagreements += false_count
        total_evaluations += total
    
    print("\n" + "="*80)
    print(f"TOTAL DISAGREEMENTS: {total_disagreements} / {total_evaluations} ({total_disagreements/total_evaluations*100:.1f}%)")
    print("="*80)

# Run the analysis
analyze_all_justification_files()
