import os
import subprocess
import openai
import pandas as pd
import shutil
import json
import re
import tiktoken  

TOKEN_LIMIT = 5000

with open("openai_key.txt", "r") as file:
    openai.api_key = file.read().strip()
def extract_repo_url(link):
    match = re.match(r"(https://github\.com/[^/]+/[^/]+)", link)
    return match.group(1) + "/" if match else link

def count_tokens(text):
    """Counts tokens using OpenAI's tokenizer."""
    encoding = tiktoken.encoding_for_model("gpt-4")
    return len(encoding.encode(text))

def chunk_text(text, max_tokens=TOKEN_LIMIT):
    """Splits text into smaller chunks based on token count."""
    words = text.split()
    chunks = []
    current_chunk = []
    current_tokens = 0

    for word in words:
        token_count = count_tokens(word)
        if current_tokens + token_count > max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_tokens = 0

        current_chunk.append(word)
        current_tokens += token_count

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def clone_repository(link):
    """Clones a GitHub repository to a local directory and returns the path."""
    try:
        repo_name = link.split('github.com/')[-1].rstrip('/')
        local_repo_path = f"./{repo_name.replace('/', '_')}"

        # Remove existing repository if it exists
        if os.path.exists(local_repo_path):
            shutil.rmtree(local_repo_path)

        # Clone the repository
        clone_cmd = ["git", "clone", link, local_repo_path]
        clone_result = subprocess.run(clone_cmd, capture_output=True, text=True)

        if clone_result.returncode != 0:
            print(f"Git Clone Error: {clone_result.stderr}")  # Debug output
            return f"Error: Failed to clone repository {link}"

        return local_repo_path
    except Exception as e:
        return f"Error: {e}"

def extract_contents(root_folder, file_limit=50):
    """Extracts contents of code/text files up to a limit for performance."""
    extracted_data = []
    file_count = 0

    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)

            if filename.endswith(('.py', '.js', '.java', '.cpp', '.c', '.h', 
                                  '.html', '.css', '.md', '.json', '.xml', 
                                  '.yaml', '.yml', '.sh', '.ts')):
                extracted_data.append(f"--- File: {file_path} ---\n")
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                        extracted_data.append(file.read())
                    file_count += 1
                except Exception as e:
                    extracted_data.append(f"Error reading file: {e}\n")

    return "\n".join(extracted_data)

def get_chatgpt_response(repo_link):
    """Generates a structured analysis of the GitHub repository using chunked content processing."""
    try:
        print(f"Cloning repository: {repo_link}...")
        repo_path = clone_repository(repo_link)
        
        if "Error" in repo_path:
            return repo_path  # Return error message if cloning failed

        print("Extracting repository structure...")
        try:
            if os.name == "nt":  # Windows
                structure_result = subprocess.run(["tree", "/F", repo_path], capture_output=True, text=True, shell=True)
            else:  # Linux/Mac
                structure_result = subprocess.run(["tree", "-L", "3", repo_path], capture_output=True, text=True)

            repo_structure = structure_result.stdout
        except Exception as e:
            repo_structure = f"Error generating repository structure: {e}"

        print("Extracting repository contents...")
        repo_contents = extract_contents(repo_path)
        chunks = chunk_text(repo_contents, max_tokens=TOKEN_LIMIT)

        partial_summaries = []
        for i, chunk in enumerate(chunks):
            print(f"Processing chunk {i+1}/{len(chunks)}...")

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
            """

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an AI designed to analyze GitHub repositories."},
                        {"role": "user", "content": chunk_prompt}
                    ],
                    temperature=0.7
                )
                partial_summaries.append(response["choices"][0]["message"]["content"])
            except Exception as e:
                partial_summaries.append(f"Error processing chunk {i+1}: {e}")

        final_summary = "\n\n".join(partial_summaries)

        return final_summary
    except Exception as e:
        return f"Error: {e}"

def incorporate_concern(summary, concern):
    """Incorporates the view of the repository into the summary."""
    view_prompt = f"""
    Please incorporate the following concern into the summary:
    Concern: {concern}
    {summary}

    Ensure that the summary is comprehensive and captures the essence of the repository.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI designed to enhance summaries with additional concerns."},
                {"role": "user", "content": view_prompt}
            ],
            temperature=0.7
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error incorporating concern: {e}"

def process_repository(link, concern):
    if pd.notna(link):
        repo_url = extract_repo_url(link)
        summary = get_chatgpt_response(repo_url)
        final_summary = incorporate_concern(summary, concern)
        result = {
            "repo_url": repo_url,
            "summary": final_summary,
            "concern": concern
        }
        return result


def main():
    with open("openai_key.txt", "r") as file:
        openai.api_key = file.read().strip()

    input_csv = "./examples_dataset.csv"
    output_jsonl = "output.jsonl"
    column_name = "Image URL"
    column_name2 = "Concern"
    df = pd.read_csv(input_csv, delimiter=";", encoding="utf-8", on_bad_lines="skip")
    if column_name not in df.columns:
        print(f"Error: Column '{column_name}' not found in CSV file.")
        return

    with open(output_jsonl, "w", encoding="utf-8") as file:
        for index, row in df.iterrows():
            result = process_repository(row[column_name],concern=row[column_name2])
            if result:
                file.write(json.dumps(result) + "\n")

    print(f"Results saved in {output_jsonl}")

if __name__ == "__main__":
    main()
