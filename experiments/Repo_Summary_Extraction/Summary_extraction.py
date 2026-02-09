'''
This script processes GitHub repository links from a CSV file, extracts their contents, and generates structured summaries using the Gemini API. 
It includes enhanced logic to skip irrelevant files and handles large repositories by chunking the content.
 The results are saved in a JSONL file for further analysis.
 this is a 2-step heirarchial process of summarisation of the repositories. First, we chunk the content and generate partial summaries for each chunk. 
 Then, we merge these partial summaries into a final cohesive summary.'''
import os
import subprocess
import pandas as pd
import csv
import re
import json
import shutil
import google.generativeai as genai
import tiktoken
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def count_tokens(text):
    """Counts tokens using OpenAI's tokenizer for GPT-4."""
    encoding = tiktoken.encoding_for_model("gpt-4")
    return len(encoding.encode(text,allowed_special={'<|endoftext|>'}))
# Function to extract repository URL from a GitHub file URL
def extract_repo_url(link):
    match = re.match(r"(https://github\.com/[^/]+/[^/]+)", link)
    print(match.group(1))
    return match.group(1) + "/" if match else link

# Configure Gemini API
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    print("⚠️ Warning: GEMINI_API_KEY not found in environment variables or .env file.")
genai.configure(api_key=gemini_api_key)

TOKEN_LIMIT = 50000
def chunk_text(text, max_tokens=TOKEN_LIMIT):
    """Splits text into chunks of max_tokens length."""
    words = text.split()  # Split by words to avoid cutting in the middle of a word
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        if len(current_chunk) >= max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk = []

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def clone_repository(link):
    """Clones a GitHub repository to a local directory and returns the path."""
    try:
        repo_name = link.split('github.com/')[-1].rstrip('/')
        local_repo_path = f"./repos/{repo_name.replace('/', '_')}"

        # Remove the existing repository if it exists
        if os.path.exists(local_repo_path):
            shutil.rmtree(local_repo_path)

        # Create repos directory if it doesn't exist
        os.makedirs("./repos", exist_ok=True)

        # Clone the repository
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

def extract_contents(root_folder):
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
        'CMakeLists.txt', 'build.gradle', 'build.sbt',
        'Dockerfile', '.gitignore', '.dockerignore', '.eslintignore', '.prettierignore'
    }
    
    # Directories to skip
    SKIP_DIRS = {
        '.git', 'node_modules', '__pycache__', '.pytest_cache', 
        'venv', 'env', '.venv', 'dist',  'target', 
    }
    
    extracted_data = []
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
                    
                    # Add file header and content to extracted data
                    extracted_data.append(f"--- File: {file_path} ---\n")
                    extracted_data.append(content)
                    extracted_data.append("\n\n")
                    processed_files += 1
                    
            except Exception as e:
                print(f"[WARNING] Could not read {filename}: {e}")
                skipped_files += 1
    
    print(f"[INFO] Processed {processed_files} files, skipped {skipped_files} files")
    return "\n".join(extracted_data)

def get_chatgpt_response(repo_link):
    """Generates a structured analysis of the GitHub repository using its contents, with chunking."""
    try:
        # Step 1: Clone the Repository
        repo_path = clone_repository(repo_link)
        if repo_path is None:
            return "Error: Failed to clone repository"

        # Step 2: Extract Repository Structure
        try:
            if os.name == "nt":  # Windows
                structure_result = subprocess.run(["tree", "/F", repo_path], capture_output=True, text=True, shell=True)
            else:  # Linux/Mac
                structure_result = subprocess.run(["tree", "-L", "3", repo_path], capture_output=True, text=True)

            repo_structure = structure_result.stdout
        except Exception as e:
            repo_structure = f"Error generating repository structure: {e}"

        # Step 3: Extract Code File Contents (using enhanced logic)
        repo_contents = extract_contents(repo_path)

        # Step 4: Split Contents if Too Large
        chunks = chunk_text(repo_contents, max_tokens=TOKEN_LIMIT)
        partial_summaries = []

        model = genai.GenerativeModel("gemini-2.0-flash")

        # Step 5: Process Each Chunk Separately
        for i, chunk in enumerate(chunks):
            print(f"Processing chunk {i+1}/{len(chunks)}...")  # Log progress
            chunk_prompt = f"""
            This is part {i+1} of {len(chunks)} from the GitHub repository analysis.

            Repository Structure:
            {repo_structure}

            Repository Contents (Chunk {i+1}):
            {chunk}

            Please analyze this part and generate a summary that includes:
            - Key functionalities and components
            - Important files and their roles
            - Architectural insights (if relevant)
            - Any notable design patterns

            This is only one part of the full repository. Keep your response modular so that it can be merged with other parts.
            """
            try:
                response = model.generate_content([chunk_prompt])
                partial_summaries.append(response.text if hasattr(response, 'text') else "Error: No response text received.")
            except Exception as e:
                partial_summaries.append(f"Error processing chunk {i+1}: {e}")

        # Step 6: Combine All Partial Summaries
        final_summary = "\n\n".join(partial_summaries)

        # Step 7: Generate Final Merged Summary
        final_prompt = f"""
        The following are partial summaries from an analysis of a GitHub repository:

        {final_summary}

        Please merge these summaries into a single, well-structured report. Ensure that:
        - There is no repetition
        - The information flows logically
        - The final report provides a cohesive overview of the important components, functionality, and architecture.
        IMPORTANT: Your response must not exceed 4000 tokens. Prioritize the most critical information.
        """
        generation_config = {
          "max_output_tokens": 4000
        }
        final_response = model.generate_content([final_prompt], generation_config=generation_config)

        return final_response.text if hasattr(final_response, 'text') else "Error: No response text received."

    except Exception as e:
        return f"Error: {e}"

def process_repository(link):
    if pd.notna(link):
        repo_url = extract_repo_url(link)
        summary = get_chatgpt_response(repo_url)
        summary_token_count = count_tokens(summary)
        result = {
            "repo_url": repo_url,
            "summary": summary,
            "summary_token_count": summary_token_count
        }
        return result
def get_processed_repositories(output_file):
    """Get the list of already processed repositories from the existing output file."""
    processed_repos = set()
    
    if not os.path.exists(output_file):
        print(f"[INFO] No existing output file found. Starting fresh.")
        return processed_repos
    
    try:
        with open(output_file, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                try:
                    data = json.loads(line.strip())
                    if 'repo_url' in data:
                        processed_repos.add(data['repo_url'])
                except json.JSONDecodeError:
                    print(f"[WARNING] Skipping invalid JSON on line {line_num}")
                    continue
        
        print(f"[INFO] Found {len(processed_repos)} already processed repositories")
        return processed_repos
        
    except Exception as e:
        print(f"[WARNING] Could not read existing output file: {e}")
        return set()

def append_result_to_jsonl(result, output_file):
    """Append a single result to the output JSONL file."""
    try:
        with open(output_file, 'a', encoding='utf-8') as file:
            file.write(f"{json.dumps(result)}\n")
        print(f"[SAVED] Result written to {output_file}")
    except Exception as e:
        print(f"[ERROR] Failed to write result to file: {e}")
def main():
    default_input_csv = "../../dataset/filtered_output.csv"
    input_csv = input(f"Enter the path of the ground truth csv(to evaluate) [default: {default_input_csv}]: ").strip() or default_input_csv
    
    output_jsonl = "Summaries.jsonl"
    column_name = "Image URL"

    # Create repos directory if it doesn't exist
    os.makedirs("./repos", exist_ok=True)

    # Load the CSV data
    try:
        df = pd.read_csv(input_csv, delimiter=";", encoding="utf-8", on_bad_lines="skip")
    except Exception as e:
        print(f"[ERROR] Could not read input CSV: {e}")
        return

    if column_name not in df.columns:
        print(f"[ERROR] Column '{column_name}' not found in CSV file.")
        return

    # Get already processed repositories to avoid duplicates
    processed_repos = get_processed_repositories(output_jsonl)
    
    total_repos = len(df)
    current_repo = 0
    skipped_count = 0
    processed_count = 0

    for index, row in df.iterrows():
        current_repo += 1
        link = row[column_name]
        
        if pd.isna(link):
            print(f"[SKIP] {current_repo}/{total_repos} - Empty link")
            skipped_count += 1
            continue
            
        repo_url = extract_repo_url(link)
        
        # Skip if already processed
        if repo_url in processed_repos:
            print(f"[SKIP] {current_repo}/{total_repos} - Already processed: {repo_url}")
            skipped_count += 1
            continue

        print(f"[PROGRESS] {current_repo}/{total_repos} - Processing new repository: {repo_url}")
        
        try:
            result = process_repository(link)
            if result:
                append_result_to_jsonl(result, output_jsonl)
                processed_count += 1
                print(f"[SUCCESS] Repository processed successfully")
            else:
                print(f"[WARNING] No result returned for repository")
        except Exception as e:
            print(f"[ERROR] Failed to process repository {repo_url}: {e}")
            # Continue with the next repository instead of stopping

    print(f"\n[SUMMARY] Processing complete!")
    print(f"- Total repositories in CSV: {total_repos}")
    print(f"- Already processed (skipped): {skipped_count}")
    print(f"- Newly processed: {processed_count}")
    print(f"- Results saved in: {output_jsonl}")

if __name__ == "__main__":
    main()



