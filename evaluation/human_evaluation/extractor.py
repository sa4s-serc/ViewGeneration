"""
Justification Extraction and Analysis Script
============================================
This script extracts justifications from human evaluation JSON files
and creates separate CSV files for each dimension.
"""

import json
import pandas as pd
from collections import Counter

def load_json_data(filepath):
    """Load JSON data from file."""
    with open(filepath, 'r') as f:
        return json.load(f)

def extract_justifications_by_dimension(author1_file, author2_file, output_dir='justifications/'):
    """
    Extract justifications and create separate CSV files for each dimension.
    
    Creates 5 CSV files:
    1. clarity_justifications.csv
    2. completeness_justifications.csv
    3. consistency_justifications.csv
    4. accuracy_justifications.csv
    5. detail_justifications.csv
    
    Each CSV has columns: sample_id, setting_id, author1_response, author2_response
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    # Load data
    print("Loading data...")
    author1_data = load_json_data(author1_file)
    author2_data = load_json_data(author2_file)
    
    # Dimensions to extract
    dimensions = {
        'clarity': {
            'agree_field': 'clarityAgree',
            'justification_field': 'clarityJustification'
        },
        'completeness': {
            'agree_field': 'completenessAgree',
            'justification_field': 'completenessJustification'
        },
        'consistency': {
            'agree_field': 'consistencyAgree',
            'justification_field': 'consistencyJustification'
        },
        'accuracy': {
            'rating_field': 'accuracyRating',
            'justification_field': 'accuracyJustification'
        },
        'detail': {
            'rating_field': 'detailRating',
            'justification_field': 'detailJustification'
        }
    }
    
    # Process each dimension
    for dimension_name, fields in dimensions.items():
        print(f"\nProcessing {dimension_name}...")
        
        rows = []
        
        # Iterate through all samples
        for sample_id in author1_data.keys():
            if sample_id not in author2_data:
                print(f"Warning: Sample {sample_id} not found in author2 data")
                continue
            
            # Iterate through all settings for this sample
            for setting_id in author1_data[sample_id].keys():
                if setting_id not in author2_data[sample_id]:
                    print(f"Warning: Setting {setting_id} for sample {sample_id} not found in author2 data")
                    continue
                
                a1_eval = author1_data[sample_id][setting_id]
                a2_eval = author2_data[sample_id][setting_id]
                
                row = {
                    'sample_id': sample_id,
                    'setting_id': setting_id,
                }
                
                # For 3Cs (boolean agreement)
                if 'agree_field' in fields:
                    row['author1_agree'] = a1_eval.get(fields['agree_field'], None)
                    row['author2_agree'] = a2_eval.get(fields['agree_field'], None)
                    row['agreement_match'] = row['author1_agree'] == row['author2_agree']
                
                # For Accuracy and Detail (ratings)
                if 'rating_field' in fields:
                    row['author1_rating'] = a1_eval.get(fields['rating_field'], None)
                    row['author2_rating'] = a2_eval.get(fields['rating_field'], None)
                    row['rating_match'] = row['author1_rating'] == row['author2_rating']
                
                # Justifications
                row['author1_justification'] = a1_eval.get(fields['justification_field'], '')
                row['author2_justification'] = a2_eval.get(fields['justification_field'], '')
                
                rows.append(row)
        
        # Create DataFrame and save
        df = pd.DataFrame(rows)
        output_file = os.path.join(output_dir, f'{dimension_name}_justifications.csv')
        df.to_csv(output_file, index=False)
        print(f"Saved {len(df)} rows to {output_file}")
    
    print(f"\nAll justification files saved to {output_dir}")
    return True

def calculate_rating_statistics(author1_file, author2_file, output_dir='justifications/'):
    """
    Calculate statistics for Accuracy and Detail ratings for each author.
    
    Creates:
    - accuracy_detail_statistics.csv: Overall statistics
    - accuracy_detail_by_setting.csv: Statistics broken down by setting
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    print("\nCalculating rating statistics...")
    
    # Load data
    author1_data = load_json_data(author1_file)
    author2_data = load_json_data(author2_file)
    
    # Collect all ratings
    accuracy_ratings_a1 = []
    accuracy_ratings_a2 = []
    detail_ratings_a1 = []
    detail_ratings_a2 = []
    
    # Also collect by setting
    by_setting = {}
    
    for sample_id in author1_data.keys():
        if sample_id not in author2_data:
            continue
        
        for setting_id in author1_data[sample_id].keys():
            if setting_id not in author2_data[sample_id]:
                continue
            
            a1_eval = author1_data[sample_id][setting_id]
            a2_eval = author2_data[sample_id][setting_id]
            
            # Overall
            acc_a1 = a1_eval.get('accuracyRating')
            acc_a2 = a2_eval.get('accuracyRating')
            det_a1 = a1_eval.get('detailRating')
            det_a2 = a2_eval.get('detailRating')
            
            if acc_a1:
                accuracy_ratings_a1.append(acc_a1)
            if acc_a2:
                accuracy_ratings_a2.append(acc_a2)
            if det_a1:
                detail_ratings_a1.append(det_a1)
            if det_a2:
                detail_ratings_a2.append(det_a2)
            
            # By setting
            if setting_id not in by_setting:
                by_setting[setting_id] = {
                    'accuracy_a1': [],
                    'accuracy_a2': [],
                    'detail_a1': [],
                    'detail_a2': []
                }
            
            if acc_a1:
                by_setting[setting_id]['accuracy_a1'].append(acc_a1)
            if acc_a2:
                by_setting[setting_id]['accuracy_a2'].append(acc_a2)
            if det_a1:
                by_setting[setting_id]['detail_a1'].append(det_a1)
            if det_a2:
                by_setting[setting_id]['detail_a2'].append(det_a2)
    
    # Calculate overall statistics
    print("\n=== OVERALL STATISTICS ===\n")
    
    overall_stats = []
    
    # Accuracy - Author 1
    acc_a1_counter = Counter(accuracy_ratings_a1)
    total_a1 = len(accuracy_ratings_a1)
    overall_stats.append({
        'Author': 'Author 1',
        'Metric': 'Accuracy',
        'Meets': acc_a1_counter.get('Meets Expectations', 0) + acc_a1_counter.get('Meets', 0),
        'Partial': acc_a1_counter.get('Partially Meets Expectations', 0) + acc_a1_counter.get('Partial', 0),
        'Not Meet': acc_a1_counter.get('Does Not Meet Expectations', 0) + acc_a1_counter.get('Not Meet', 0),
        'Total': total_a1,
        'Meets %': (acc_a1_counter.get('Meets Expectations', 0) + acc_a1_counter.get('Meets', 0)) / total_a1 * 100 if total_a1 > 0 else 0,
        'Partial %': (acc_a1_counter.get('Partially Meets Expectations', 0) + acc_a1_counter.get('Partial', 0)) / total_a1 * 100 if total_a1 > 0 else 0,
        'Not Meet %': (acc_a1_counter.get('Does Not Meet Expectations', 0) + acc_a1_counter.get('Not Meet', 0)) / total_a1 * 100 if total_a1 > 0 else 0
    })
    
    # Accuracy - Author 2
    acc_a2_counter = Counter(accuracy_ratings_a2)
    total_a2 = len(accuracy_ratings_a2)
    overall_stats.append({
        'Author': 'Author 2',
        'Metric': 'Accuracy',
        'Meets': acc_a2_counter.get('Meets Expectations', 0) + acc_a2_counter.get('Meets', 0),
        'Partial': acc_a2_counter.get('Partially Meets Expectations', 0) + acc_a2_counter.get('Partial', 0),
        'Not Meet': acc_a2_counter.get('Does Not Meet Expectations', 0) + acc_a2_counter.get('Not Meet', 0),
        'Total': total_a2,
        'Meets %': (acc_a2_counter.get('Meets Expectations', 0) + acc_a2_counter.get('Meets', 0)) / total_a2 * 100 if total_a2 > 0 else 0,
        'Partial %': (acc_a2_counter.get('Partially Meets Expectations', 0) + acc_a2_counter.get('Partial', 0)) / total_a2 * 100 if total_a2 > 0 else 0,
        'Not Meet %': (acc_a2_counter.get('Does Not Meet Expectations', 0) + acc_a2_counter.get('Not Meet', 0)) / total_a2 * 100 if total_a2 > 0 else 0
    })
    
    # Detail - Author 1
    det_a1_counter = Counter(detail_ratings_a1)
    total_d1 = len(detail_ratings_a1)
    overall_stats.append({
        'Author': 'Author 1',
        'Metric': 'Level of Detail',
        'Meets': det_a1_counter.get('Meets Expectations', 0) + det_a1_counter.get('Meets', 0),
        'Partial': det_a1_counter.get('Partially Meets Expectations', 0) + det_a1_counter.get('Partial', 0),
        'Not Meet': det_a1_counter.get('Does Not Meet Expectations', 0) + det_a1_counter.get('Not Meet', 0),
        'Total': total_d1,
        'Meets %': (det_a1_counter.get('Meets Expectations', 0) + det_a1_counter.get('Meets', 0)) / total_d1 * 100 if total_d1 > 0 else 0,
        'Partial %': (det_a1_counter.get('Partially Meets Expectations', 0) + det_a1_counter.get('Partial', 0)) / total_d1 * 100 if total_d1 > 0 else 0,
        'Not Meet %': (det_a1_counter.get('Does Not Meet Expectations', 0) + det_a1_counter.get('Not Meet', 0)) / total_d1 * 100 if total_d1 > 0 else 0
    })
    
    # Detail - Author 2
    det_a2_counter = Counter(detail_ratings_a2)
    total_d2 = len(detail_ratings_a2)
    overall_stats.append({
        'Author': 'Author 2',
        'Metric': 'Level of Detail',
        'Meets': det_a2_counter.get('Meets Expectations', 0) + det_a2_counter.get('Meets', 0),
        'Partial': det_a2_counter.get('Partially Meets Expectations', 0) + det_a2_counter.get('Partial', 0),
        'Not Meet': det_a2_counter.get('Does Not Meet Expectations', 0) + det_a2_counter.get('Not Meet', 0),
        'Total': total_d2,
        'Meets %': (det_a2_counter.get('Meets Expectations', 0) + det_a2_counter.get('Meets', 0)) / total_d2 * 100 if total_d2 > 0 else 0,
        'Partial %': (det_a2_counter.get('Partially Meets Expectations', 0) + det_a2_counter.get('Partial', 0)) / total_d2 * 100 if total_d2 > 0 else 0,
        'Not Meet %': (det_a2_counter.get('Does Not Meet Expectations', 0) + det_a2_counter.get('Not Meet', 0)) / total_d2 * 100 if total_d2 > 0 else 0
    })
    
    # Save overall statistics
    overall_df = pd.DataFrame(overall_stats)
    overall_file = os.path.join(output_dir, 'accuracy_detail_statistics.csv')
    overall_df.to_csv(overall_file, index=False)
    
    print(overall_df.to_string(index=False))
    print(f"\nSaved to {overall_file}")
    
    # Calculate by-setting statistics
    print("\n=== BY-SETTING STATISTICS ===\n")
    
    setting_stats = []
    
    for setting_id, data in sorted(by_setting.items()):
        # Accuracy - Author 1
        acc_a1 = Counter(data['accuracy_a1'])
        total = len(data['accuracy_a1'])
        if total > 0:
            setting_stats.append({
                'Setting': setting_id,
                'Author': 'Author 1',
                'Metric': 'Accuracy',
                'Meets': acc_a1.get('Meets Expectations', 0) + acc_a1.get('Meets', 0),
                'Partial': acc_a1.get('Partially Meets Expectations', 0) + acc_a1.get('Partial', 0),
                'Not Meet': acc_a1.get('Does Not Meet Expectations', 0) + acc_a1.get('Not Meet', 0),
                'Total': total
            })
        
        # Accuracy - Author 2
        acc_a2 = Counter(data['accuracy_a2'])
        total = len(data['accuracy_a2'])
        if total > 0:
            setting_stats.append({
                'Setting': setting_id,
                'Author': 'Author 2',
                'Metric': 'Accuracy',
                'Meets': acc_a2.get('Meets Expectations', 0) + acc_a2.get('Meets', 0),
                'Partial': acc_a2.get('Partially Meets Expectations', 0) + acc_a2.get('Partial', 0),
                'Not Meet': acc_a2.get('Does Not Meet Expectations', 0) + acc_a2.get('Not Meet', 0),
                'Total': total
            })
        
        # Detail - Author 1
        det_a1 = Counter(data['detail_a1'])
        total = len(data['detail_a1'])
        if total > 0:
            setting_stats.append({
                'Setting': setting_id,
                'Author': 'Author 1',
                'Metric': 'Level of Detail',
                'Meets': det_a1.get('Meets Expectations', 0) + det_a1.get('Meets', 0),
                'Partial': det_a1.get('Partially Meets Expectations', 0) + det_a1.get('Partial', 0),
                'Not Meet': det_a1.get('Does Not Meet Expectations', 0) + det_a1.get('Not Meet', 0),
                'Total': total
            })
        
        # Detail - Author 2
        det_a2 = Counter(data['detail_a2'])
        total = len(data['detail_a2'])
        if total > 0:
            setting_stats.append({
                'Setting': setting_id,
                'Author': 'Author 2',
                'Metric': 'Level of Detail',
                'Meets': det_a2.get('Meets Expectations', 0) + det_a2.get('Meets', 0),
                'Partial': det_a2.get('Partially Meets Expectations', 0) + det_a2.get('Partial', 0),
                'Not Meet': det_a2.get('Does Not Meet Expectations', 0) + det_a2.get('Not Meet', 0),
                'Total': total
            })
    
    # Save by-setting statistics
    setting_df = pd.DataFrame(setting_stats)
    setting_file = os.path.join(output_dir, 'accuracy_detail_by_setting.csv')
    setting_df.to_csv(setting_file, index=False)
    
    print(setting_df.to_string(index=False))
    print(f"\nSaved to {setting_file}")
    
    return overall_df, setting_df

def print_summary_statistics(author1_file, author2_file):
    """
    Print a comprehensive summary of all statistics.
    """
    print("\n" + "="*80)
    print("COMPREHENSIVE RATING STATISTICS")
    print("="*80)
    
    # Calculate statistics
    overall_df, setting_df = calculate_rating_statistics(author1_file, author2_file)
    
    # Print formatted summary
    print("\n--- OVERALL SUMMARY ---\n")
    for _, row in overall_df.iterrows():
        print(f"{row['Author']} - {row['Metric']}:")
        print(f"  Meets: {row['Meets']} ({row['Meets %']:.1f}%)")
        print(f"  Partial: {row['Partial']} ({row['Partial %']:.1f}%)")
        print(f"  Not Meet: {row['Not Meet']} ({row['Not Meet %']:.1f}%)")
        print(f"  Total: {row['Total']}")
        print()
    
    return True

# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    AUTHOR1_FILE = "evaluation_author_2.json"
    AUTHOR2_FILE = "evaluation_author_1.json"
    OUTPUT_DIR = "justifications/"
    
    print("="*80)
    print("JUSTIFICATION EXTRACTION AND ANALYSIS")
    print("="*80)
    
    # Step 1: Extract justifications to separate CSV files
    print("\n[STEP 1] Extracting justifications by dimension...")
    extract_justifications_by_dimension(AUTHOR1_FILE, AUTHOR2_FILE, OUTPUT_DIR)
    
    # Step 2: Calculate and save rating statistics
    print("\n[STEP 2] Calculating rating statistics...")
    overall_df, setting_df = calculate_rating_statistics(AUTHOR1_FILE, AUTHOR2_FILE, OUTPUT_DIR)
    
    # Step 3: Print comprehensive summary
    print("\n[STEP 3] Generating summary report...")
    print_summary_statistics(AUTHOR1_FILE, AUTHOR2_FILE)
    
    print("\n" + "="*80)
    print("EXTRACTION COMPLETE!")
    print("="*80)
    print(f"\nGenerated files in '{OUTPUT_DIR}':")
    print("  1. clarity_justifications.csv")
    print("  2. completeness_justifications.csv")
    print("  3. consistency_justifications.csv")
    print("  4. accuracy_justifications.csv")
    print("  5. detail_justifications.csv")
    print("  6. accuracy_detail_statistics.csv")
    print("  7. accuracy_detail_by_setting.csv")
    print("\nYou can now review these files for manual analysis.")