import os
import subprocess
import shutil
import pandas as pd
import re
import tiktoken

INPUT_CSV = "./filtered_output.csv"
COLUMN_NAME = "Image URL"
OUTPUT_CSV = "repo_token_counts.csv"

def extract_repo_url(link):
    match = re.match(r"(https://github\.com/[^/]+/[^/]+)", link)
    return match.group(1) + "/" if match else link

def count_tokens(text):
    """Counts tokens using OpenAI's tokenizer for GPT-4."""
    encoding = tiktoken.encoding_for_model("gpt-4")
    return len(encoding.encode(text,allowed_special={'<|endoftext|>'}))

def clone_repository(link):
    """Clones a GitHub repository to a local directory and returns the path."""
    try:
        repo_name = link.split('github.com/')[-1].rstrip('/')
        local_repo_path = f"./repos/{repo_name.replace('/', '_')}"
        
        if os.path.exists(local_repo_path):
            shutil.rmtree(local_repo_path)
        
        clone_cmd = ["git", "clone", link, local_repo_path]
        clone_result = subprocess.run(clone_cmd, capture_output=True, text=True)
        
        if clone_result.returncode != 0:
            print(f"[ERROR] Failed to clone {link}: {clone_result.stderr}")
            return None
        
        return local_repo_path
    except Exception as e:
        print(f"[EXCEPTION] {e}")
        return None

def is_likely_data_file(content, filename):
    """Check if a file content looks like it contains mostly data."""
    
    # If it's a known config/source file, don't skip it
    if any(filename.lower().endswith(ext) for ext in ['.py', '.js', '.java', '.cpp', '.c', '.h', '.md', '.txt', '.rst']):
        return False
    
    lines = content.split('\n')
    if len(lines) < 10:
        return False
    
    # Check for patterns that suggest data files
    comma_lines = sum(1 for line in lines if line.count(',') > 5)
    pipe_lines = sum(1 for line in lines if line.count('|') > 3)
    tab_lines = sum(1 for line in lines if line.count('\t') > 3)
    
    # If more than 50% of lines look like structured data, consider it a data file
    data_lines = comma_lines + pipe_lines + tab_lines
    return data_lines > len(lines) * 0.5

def extract_code_contents(root_folder):
    """Extract contents from all files except data files, build files, and binary files."""
    
    # File extensions to EXCLUDE
    EXCLUDE_EXTENSIONS = {
        # Data files
        '.csv', '.tsv', '.xlsx', '.xls', '.json',
        '.sqlite', '.db', '.sql', '.parquet', '.avro', '.orc',
        
        # Build/package files
        '.lock', '.gradle', '.maven', '.sbt',
        
        # Binary files
        '.exe', '.dll', '.so', '.dylib', '.a', '.lib', '.obj', '.o',
        '.bin', '.dat', '.zip', '.tar', '.gz', '.bz2', '.xz', '.7z',
        '.rar', '.jar', '.war', '.ear',
        
        # Image files
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.ico',
        '.webp', '.raw', '.cr2', '.nef', '.arw',
        
        # Audio/Video files
        '.mp3', '.wav', '.flac', '.aac', '.ogg', '.mp4', '.avi', '.mkv',
        '.mov', '.wmv', '.flv', '.webm', '.m4a', '.wma',
        
        # Document files (if you want to exclude these too)
        '.pdf', '.ppt', '.pptx', '.xls', '.xlsx',
        
        # Font files
        '.ttf', '.otf', '.woff', '.woff2', '.eot',
        
        # Other binary/data formats
        '.pickle', '.pkl', '.npy', '.npz', '.mat', '.rds', '.feather'
    }
    
    # Specific filenames to EXCLUDE (build files)
    EXCLUDE_FILENAMES = {
        'package-lock.json', 'yarn.lock', 'composer.lock', 'Pipfile.lock',
        'poetry.lock', 'pnpm-lock.yaml', 'npm-shrinkwrap.json',
        'Makefile', 'makefile', 'CMakeLists.txt', 'build.gradle',
        'pom.xml', 'build.xml', 'ant.xml', 'build.sbt',
        'requirements.txt', 'environment.yml', 'conda-environment.yml',
        'Dockerfile', 'docker-compose.yml', 'docker-compose.yaml',
        '.gitignore', '.dockerignore', '.eslintignore', '.prettierignore'
    }
    
    # Directories to skip
    SKIP_DIRS = {
        '.git', 'node_modules', '__pycache__', '.pytest_cache', 
        'venv', 'env', '.venv', 'dist', 'build', 'target', 
        '.next', '.nuxt', 'coverage', 'vendor', 'packages',
        'data', 'datasets', 'assets', 'static', 'public'  # Common data/asset directories
    }
    
    contents = []
    processed_files = 0
    skipped_files = 0
    
    for dirpath, dirnames, filenames in os.walk(root_folder):
        # Remove directories we want to skip from dirnames
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            _, ext = os.path.splitext(filename.lower())
            
            # Skip if extension is in exclude list
            if ext in EXCLUDE_EXTENSIONS:
                skipped_files += 1
                continue
                
            # Skip if filename is in exclude list
            if filename.lower() in EXCLUDE_FILENAMES:
                skipped_files += 1
                continue
                
            # Additional check for package.json and similar files
            if filename.lower().endswith(('.json', '.lock', '.xml')) and any(
                build_word in filename.lower() 
                for build_word in ['package', 'composer',  'build', 'gradle', 'maven']
            ):
                skipped_files += 1
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    
                    # Skip files that are too large (likely data files)
                    if len(content) > 2_000_000:  # 2MB limit
                        print(f"[WARNING] Skipping large file: {filename}")
                        skipped_files += 1
                        continue
                    
                    # Skip files that look like they contain mostly data
                    if is_likely_data_file(content, filename):
                        print(f"[INFO] Skipping data-like file: {filename}")
                        skipped_files += 1
                        continue
                    
                    contents.append(content)
                    processed_files += 1
                    
            except Exception as e:
                print(f"[WARNING] Could not read {filename}: {e}")
                skipped_files += 1
    
    print(f"[INFO] Processed {processed_files} files, skipped {skipped_files} files")
    return "\n".join(contents)

def process_repository(link):
    repo_url = extract_repo_url(link)
    print(f"[INFO] Processing: {repo_url}")
    
    repo_path = clone_repository(repo_url)
    if repo_path is None:
        return {"repo_url": repo_url, "token_count": "ERROR"}
    
    code_contents = extract_code_contents(repo_path)
    token_count = count_tokens(code_contents)
    
    print(f"[DONE] Tokens: {token_count} for {repo_url}")
    return {"repo_url": repo_url, "token_count": token_count}

def append_result_to_csv(result, is_first_write=False):
    """Append a single result to the output CSV file."""
    result_df = pd.DataFrame([result])
    
    if is_first_write:
        # Write with header for the first entry
        result_df.to_csv(OUTPUT_CSV, index=False, mode='w')
    else:
        # Append without header for subsequent entries
        result_df.to_csv(OUTPUT_CSV, index=False, mode='a', header=False)

def get_processed_repos():
    """Get the list of already processed repositories to avoid duplicates."""
    if not os.path.exists(OUTPUT_CSV):
        return set()
    
    try:
        existing_df = pd.read_csv(OUTPUT_CSV)
        return set(existing_df['repo_url'].tolist())
    except Exception as e:
        print(f"[WARNING] Could not read existing output file: {e}")
        return set()

def main():
    os.makedirs("./repos", exist_ok=True)
    
    try:
        df = pd.read_csv(INPUT_CSV, delimiter=";", encoding="utf-8", on_bad_lines="skip")
    except Exception as e:
        print(f"[ERROR] Could not read input CSV: {e}")
        return
    
    if COLUMN_NAME not in df.columns:
        print(f"[ERROR] Column '{COLUMN_NAME}' not found in CSV.")
        return
    
    # Get already processed repositories to avoid duplicates
    processed_repos = get_processed_repos()
    print(f"[INFO] Found {len(processed_repos)} already processed repositories")
    
    is_first_write = len(processed_repos) == 0
    total_repos = len(df)
    current_repo = 0
    
    for _, row in df.iterrows():
        current_repo += 1
        link = row[COLUMN_NAME]
        repo_url = extract_repo_url(link)
        
        # Skip if already processed
        if repo_url in processed_repos:
            print(f"[SKIP] {current_repo}/{total_repos} - Already processed: {repo_url}")
            continue
        
        print(f"[PROGRESS] {current_repo}/{total_repos} - Processing new repository")
        result = process_repository(link)
        
        # Write result immediately after processing
        try:
            append_result_to_csv(result, is_first_write)
            is_first_write = False  # Only the first write should include headers
            print(f"[SAVED] Result written to {OUTPUT_CSV}")
        except Exception as e:
            print(f"[ERROR] Failed to write result to CSV: {e}")
    
    print(f"[SUCCESS] Processing complete. Results saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()