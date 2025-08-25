import os
import subprocess
import openai
import pandas as pd
import csv
import re
import json
import shutil

# Set your OpenAI API key here
openai.api_key = "sk-your-api-key"

def extract_repo_url(link):
    match = re.match(r"(https://github\.com/[^/]+/[^/]+)", link)
    return match.group(1) + "/" if match else link

def get_chatgpt_response(link):
    try:
        repo_name = link.split('github.com/')[-1].rstrip('/')
        local_repo_path = f"./{repo_name.replace('/', '_')}"

        if os.path.exists(local_repo_path):
            shutil.rmtree(local_repo_path)

        clone_cmd = ["git", "clone", link, local_repo_path]
        clone_result = subprocess.run(clone_cmd, capture_output=True, text=True)

        if clone_result.returncode != 0:
            return f"Error: Failed to clone repository {link}"

        try:
            if os.name == "nt":
                structure_result = subprocess.run(["tree", "/F", local_repo_path], capture_output=True, text=True, shell=True)
            else:
                structure_result = subprocess.run(["tree", "-L", "3", local_repo_path], capture_output=True, text=True)

            repo_structure = structure_result.stdout
        except Exception as e:
            repo_structure = f"Error generating repository structure: {e}"

        prompt = f"""
Please analyze the GitHub repository at {link}. Include:

- **Repository Structure**: Overview of files and folders
- **File-by-File Analysis**: Purpose and functionality of key files
- **Repository Organization**: How files/directories relate
- **Architecture Summary**: Major components, how they interact
- **Overall Summary**: Main purpose, structure, and interaction of components

Here is the repository structure:
{repo_structure}
"""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {e}"

def get_plantuml_from_summary(summary, repo_name, error_message=None):
    system_prompt = '''You are an expert in PlantUML. Based on the repository summary below, generate a valid PlantUML component diagram. Include:
- Clear components and their relationships
- Accurate system structure
- Only the PlantUML code, no explanation
- Syntax must be valid and usable with PlantUML
'''

    if error_message:
        system_prompt += f"\nNote: The previous output had the following error: {error_message}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": summary}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {e}"

def save_plantuml_code(puml_code, repo_name):
    os.makedirs("chatgpt_plantumlcode", exist_ok=True)
    clean_repo_name = repo_name.replace('/', '_').replace('\\', '_').rstrip('_')
    file_path = os.path.join("chatgpt_plantumlcode", f"{clean_repo_name}.puml")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("@startuml\n")
        file.write(puml_code)
        file.write("\n@enduml")
    return file_path

def compile_plantuml(input_path, output_dir="../chatgpt_output_images"):
    os.makedirs(output_dir, exist_ok=True)
    result = subprocess.run(["plantuml", "-o", output_dir, input_path], 
                            capture_output=True, text=True)
    return result.returncode == 0, result.stderr

def process_repository(link):
    if pd.notna(link):
        repo_url = extract_repo_url(link)
        summary = get_chatgpt_response(repo_url)

        result = {
            "repo_url": repo_url,
            "summary": summary
        }

        repo_name = repo_url.split('github.com/')[-1].rstrip('/')
        max_retries = 3
        attempt = 0

        with open("error.log", "a", encoding="utf-8") as log_file:
            while attempt < max_retries:
                puml_code = get_plantuml_from_summary(summary, repo_name, 
                                                      error_message=None if attempt == 0 else error_message)
                file_path = save_plantuml_code(puml_code, repo_name)
                success, error_message = compile_plantuml(file_path)

                if success:
                    log_file.write(f"Successfully processed repo {repo_url}\n")
                    log_file.write(f"PlantUML diagram saved at {file_path}\n")
                    break
                else:
                    log_file.write(f"Attempt {attempt + 1}: Failed for {repo_url}\n")
                    log_file.write(f"Error: {error_message}\n")
                    attempt += 1

            if attempt == max_retries:
                log_file.write(f"Failed after {max_retries} attempts: {repo_url}\n")

        return result

def main():
    input_csv = "./dataset/filtered_output_uml.csv"
    output_jsonl = "chatgpt_output.jsonl"
    column_name = "Image URL"

    df = pd.read_csv(input_csv, delimiter=";", encoding="utf-8", on_bad_lines="skip").head(16)

    if column_name not in df.columns:
        print(f"Error: Column '{column_name}' not found in CSV.")
        return

    with open(output_jsonl, "w", encoding="utf-8") as file:
        for _, row in df.iterrows():
            result = process_repository(row[column_name])
            if result:
                file.write(f"{json.dumps(result)}\n")

    print(f"All results saved in {output_jsonl}")

if __name__ == "__main__":
    main()
