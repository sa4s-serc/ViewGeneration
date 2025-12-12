import json
import csv
import sys
from pathlib import Path

def clean_repo_name(repo_name):
    """Clean repository name by replacing slashes and backslashes with underscores."""
    return repo_name.replace('/', '_').replace('\\', '_').rstrip('_')

def read_jsonl(file_path):
    """Read JSONL file and return list of dictionaries."""
    data = []
    print(f"Reading JSONL file: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            
            try:
                json_obj = json.loads(line)
                # Add cleaned repo name
                if "Repository Name" in json_obj:
                    json_obj["Clean_Repo_Name"] = clean_repo_name(json_obj["Repository Name"])
                data.append(json_obj)
            except json.JSONDecodeError as e:
                print(f"Warning: Skipping invalid JSON on line {line_num}: {e}")
    
    print(f"  Found {len(data)} records")
    return data

def read_metrics_csv(file_path):
    """Read metrics CSV file and return dictionary keyed by ImageName."""
    metrics = {}
    print(f"\nReading metrics CSV: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            image_name = row.get('ImageName', '')
            if image_name:
                metrics[image_name] = row
    
    print(f"  Found {len(metrics)} metric records")
    return metrics

def read_llm_judge_data(base_dir):
    """Read LLM judge comparison data from outputs_3cs directory."""
    llm_data = {}
    base_path = Path(base_dir)
    
    print(f"\nReading LLM judge data from: {base_dir}")
    
    if not base_path.exists():
        print(f"  Warning: Directory not found")
        return llm_data
    
    # Look for comparison.json files
    comparison_files = list(base_path.rglob("*_comparison.json"))
    
    if not comparison_files:
        print(f"  Warning: No *_comparison.json files found")
        return llm_data
    
    print(f"  Found {len(comparison_files)} comparison files")
    
    for comp_file in comparison_files:
        try:
            with open(comp_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Extract repo name from filename
                # Files are named like: pau-minoves_jseats_comparison.json
                # We want: pau-minoves_jseats
                filename = comp_file.stem  # Gets filename without extension
                
                # Remove '_comparison' suffix if present
                if filename.endswith('_comparison'):
                    repo_name = filename[:-11]  # Remove last 11 characters ('_comparison')
                else:
                    repo_name = filename
                
                if repo_name:
                    llm_data[repo_name] = data
                    print(f"    Loaded: {repo_name}")
                    
        except json.JSONDecodeError as e:
            print(f"  Warning: Error reading {comp_file}: {e}")
        except Exception as e:
            print(f"  Warning: Error processing {comp_file}: {e}")
    
    print(f"  Successfully loaded {len(llm_data)} LLM judge records")
    return llm_data

def combine_data(jsonl_data, metrics_data, llm_judge_data):
    """Combine all data sources."""
    combined = []
    
    # Columns to exclude
    exclude_columns = {"summary", "Assigned to", "Image URL"}
    
    print(f"\nCombining data...")
    matched_metrics = 0
    matched_llm = 0
    
    for entry in jsonl_data:
        combined_entry = {}
        
        # Copy entry data, excluding unwanted columns
        for key, value in entry.items():
            if key not in exclude_columns:
                combined_entry[key] = value
        
        clean_name = combined_entry.get("Clean_Repo_Name", "")
        
        # Match with metrics CSV
        if clean_name in metrics_data:
            metrics = metrics_data[clean_name]
            # Add metrics fields with "zero shot gpt_3.5_sonnet" prefix (excluding ImageName)
            for key, value in metrics.items():
                if key != 'ImageName':
                    combined_entry[f"zeroShot_deepseek_{key}"] = value
            matched_metrics += 1
        
        # Match with LLM judge data
        if clean_name in llm_judge_data:
            llm_eval = llm_judge_data[clean_name]
            
            # Add LLM judge evaluations with "zero shot gpt_3.5_sonnet" prefix
            if "Clarity" in llm_eval:
                combined_entry["zeroShot_deepseek_LLM_Clarity_Rating"] = llm_eval["Clarity"].get("rating", "")
            
            if "Completeness" in llm_eval:
                combined_entry["zeroShot_deepseek_LLM_Completeness_Rating"] = llm_eval["Completeness"].get("rating", "")
            
            if "Consistency" in llm_eval:
                combined_entry["zeroShot_deepseek_LLM_Consistency_Rating"] = llm_eval["Consistency"].get("rating", "")
            
            matched_llm += 1
        
        combined.append(combined_entry)
    
    print(f"  Total records: {len(combined)}")
    print(f"  Matched with metrics: {matched_metrics}")
    print(f"  Matched with LLM judge: {matched_llm}")
    
    return combined

def write_to_csv(data, output_file):
    """Write combined data to CSV."""
    if not data:
        print("No data to write")
        return
    
    # Get all unique keys across all records
    all_keys = set()
    for record in data:
        all_keys.update(record.keys())
    
    # Sort keys for consistent column order
    headers = sorted(all_keys)
    
    print(f"\nWriting to CSV: {output_file}")
    print(f"  Columns: {len(headers)}")
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"  Successfully written!")

def main():
    # Default paths
    jsonl_file = '../../../../Architectural_knowledge_extraction/generated_summaries.jsonl'
    metrics_csv = 'zeroShot_deepseek_output_images_similarity_results.csv'
    llm_judge_dir = 'LLM_as_a_Judge_openai_outputs_3cs'
    output_file = 'combined_data.csv'
    
    # Parse command-line arguments
    if len(sys.argv) > 1:
        jsonl_file = sys.argv[1]
    if len(sys.argv) > 2:
        metrics_csv = sys.argv[2]
    if len(sys.argv) > 3:
        llm_judge_dir = sys.argv[3]
    if len(sys.argv) > 4:
        output_file = sys.argv[4]
    
    print("=" * 70)
    print("DATA COMBINATION SCRIPT")
    print("=" * 70)
    
    # Check if files exist
    if not Path(jsonl_file).exists():
        print(f"Error: JSONL file not found: {jsonl_file}")
        print("\nUsage: python combine_data.py <jsonl_file> <metrics_csv> <llm_judge_dir> [output_csv]")
        return
    
    if not Path(metrics_csv).exists():
        print(f"Error: Metrics CSV not found: {metrics_csv}")
        return
    
    # Read all data sources
    jsonl_data = read_jsonl(jsonl_file)
    metrics_data = read_metrics_csv(metrics_csv)
    llm_judge_data = read_llm_judge_data(llm_judge_dir)
    
    # Combine data
    combined_data = combine_data(jsonl_data, metrics_data, llm_judge_data)
    
    # Write to CSV
    write_to_csv(combined_data, output_file)
    
    print("\n" + "=" * 70)
    print(f"COMPLETE! Output saved to: {output_file}")
    print("=" * 70)

if __name__ == "__main__":
    main()