import os
import subprocess
import shutil
import pandas as pd
import re
import tiktoken

# Constants
TOKEN_LIMIT = 5000
INPUT_CSV = "./dataset/filtered_output_uml.csv"
COLUMN_NAME = "Image URL"
OUTPUT_CSV = "repo_token_counts.csv"

def extract_repo_url(link):
    match = re.match(r"(https://github\.com/[^/]+/[^/]+)", link)
    return match.group(1) + "/" if match else link

def count_tokens(text):
    """Counts tokens using OpenAI's tokenizer for GPT-4."""
    encoding = tiktoken.encoding_for_model("gpt-4")
    return len(encoding.encode(text))

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

def extract_code_contents(root_folder, file_limit=50):
    """Extracts code contents from a repo folder (basic file types only)."""
    code_extensions = (
        '.py', '.js', '.java', '.cpp', '.c', '.h', '.html',
        '.css', '.md', '.json', '.xml', '.yaml', '.yml',
        '.sh', '.ts'
    )

    contents = []
    file_count = 0

    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith(code_extensions):
                try:
                    file_path = os.path.join(dirpath, filename)
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                        contents.append(file.read())
                        file_count += 1
                    if file_count >= file_limit:
                        return "\n".join(contents)
                except Exception as e:
                    print(f"[WARNING] Could not read {filename}: {e}")

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

    results = []

    for _, row in df.iterrows():
        link = row[COLUMN_NAME]
        result = process_repository(link)
        results.append(result)

    token_df = pd.DataFrame(results)
    token_df.to_csv(OUTPUT_CSV, index=False)
    print(f"[SUCCESS] Token counts saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
