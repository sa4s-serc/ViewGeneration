import os
import subprocess
from openai import OpenAI
import json
from pathlib import Path

# Initialize DeepSeek client
client = OpenAI(api_key="", base_url="https://api.deepseek.com/v1")

def get_mermaid_from_summary(summary, repo_name, concern, behavior, error_message=None, code=None):
    # Decide on diagram type based on behavior
    if behavior == "dynamic":
        diagram_instruction = f'''
You are expert software architect. Your task is to design a view for the system based on the architectural knowledge provided. Use Mermaid diagrams. Based on the following repository summary and system behavior, generate a **Mermaid sequence diagram** to show dynamic interactions.

**Behavioral focus:** {concern}

Ensure the diagram:
- Accurately represents runtime message flow between components or services.
- Matches the described system behavior.
- Is valid Mermaid code with no explanation.
- Uses the repository name for context: {repo_name}
'''
    else:
        diagram_instruction = f'''
You are expert software architect. Your task is to design a view for the system based on the architectural knowledge provided. Use Mermaid diagrams. Based on the following repository summary, generate a **Mermaid C4 component diagram** to capture the static architecture. Focus on the architectural concern: **{concern}**.

Ensure the diagram:
- Clearly shows system components and their relationships.
- Highlights how the architecture addresses the specified concern.
- Is valid Mermaid code with no explanation.
- Uses the repository name for context: {repo_name}
'''

    # Include retry guidance if needed
    if error_message:
        diagram_instruction += f"\nNote: A previous attempt failed with the following error:\n{error_message}\nProblematic code:\n{code}\nPlease correct and regenerate."

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": diagram_instruction},
                {"role": "user", "content": summary}
            ],
            temperature=0.7,
            max_tokens=1024,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def cleanup_mermaid_code(mermaid_code):
    """Clean up Mermaid code by removing markdown code blocks if present."""
    mermaid_code = mermaid_code.strip()
    if mermaid_code.startswith("```mermaid") and mermaid_code.endswith("```"):
        return mermaid_code[10:-3].strip()
    elif mermaid_code.startswith("```") and mermaid_code.endswith("```"):
        return mermaid_code[3:-3].strip()
    return mermaid_code

def save_mermaid_code(mermaid_code, repo_name):
    """Save Mermaid code to a file with proper formatting."""
    os.makedirs("results/mermaid_code", exist_ok=True)
    os.makedirs("results/diagrams", exist_ok=True)
    
    clean_repo_name = repo_name.replace('/', '_').replace('\\', '_').rstrip('_')
    file_path = f"results/mermaid_code/{clean_repo_name}.mmd"
    
    cleaned_code = cleanup_mermaid_code(mermaid_code)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(cleaned_code)
    
    return file_path

def find_mmdc():
    """Try to locate the mmdc executable in common locations."""
    try:
        subprocess.run(["mmdc", "--version"], capture_output=True, check=True)
        return "mmdc"
    except:
        pass
    
    if os.name == 'nt':
        paths_to_try = [
            os.path.join(os.environ.get("APPDATA", ""), "npm", "mmdc.cmd"),
            os.path.join(os.environ.get("USERPROFILE", ""), "AppData", "Roaming", "npm", "mmdc.cmd"),
            os.path.join(os.environ.get("PROGRAMFILES", ""), "nodejs", "mmdc.cmd")
        ]
        for path in paths_to_try:
            if os.path.exists(path):
                return path
    else:
        paths_to_try = [
            "/usr/local/bin/mmdc",
            "/usr/bin/mmdc",
            os.path.expanduser("~/.npm-global/bin/mmdc"),
            os.path.expanduser("~/.nvm/versions/node/*/bin/mmdc")
        ]
        for path in paths_to_try:
            if os.path.exists(path):
                return path
    return None

def compile_mermaid(input_file):
    """Compile Mermaid file to SVG using mmdc."""
    try:
        output_file = input_file.replace("mermaid_code", "diagrams").replace(".mmd", ".svg")
        mmdc_path = find_mmdc()
        if not mmdc_path:
            return False, "mermaid-cli (mmdc) not found in PATH"
        
        cmd = [
            mmdc_path,
            "-i", input_file,
            "-o", output_file,
            "-t", "default",
            "-b", "transparent",
            "-s", "2"
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        if result.returncode != 0:
            return False, result.stderr
        
        return True, None
    
    except subprocess.CalledProcessError as e:
        return False, f"mmdc compilation failed: {e.stderr}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"

def process_view(repo_name, summary, concern, behavior):
    max_retries = 3
    attempt = 0
    error_message = None
    mermaid_code = None
    
    with open("error.log", "a", encoding="utf-8") as log_file:
        while attempt < max_retries:
            mermaid_code = get_mermaid_from_summary(
                summary, repo_name, concern, behavior,
                error_message=None if attempt == 0 else error_message,
                code=None if attempt == 0 else mermaid_code
            )
            
            if mermaid_code.startswith("Error:"):
                log_file.write(f"API Error for {repo_name}: {mermaid_code}\n")
                break
                
            file_path = save_mermaid_code(mermaid_code, repo_name)
            success, error_message = compile_mermaid(file_path)
            
            if success:
                log_file.write(f"Successfully processed repo {repo_name}\n")
                break
            else:
                log_file.write(f"Attempt {attempt + 1} failed for {repo_name}: {error_message}\n")
                attempt += 1
                
        if attempt == max_retries:
            log_file.write(f"Failed to generate valid mermaid for {repo_name} after {max_retries} attempts\n")

def main():
    input_jsonl = "../experiemts/Architectural_knowledge_extraction/generated_summaries.jsonl"
    column_name1 = "Repository Name"
    column_name2 = "summary"
    column_name3 = "Concern"
    column_name4 = "Behavior"

    try:
        with open(input_jsonl, 'r', encoding='utf-8') as f:
            entries = [json.loads(line) for line in f]
    except Exception as e:
        print(f"Error reading JSONL file: {e}")
        return

    for entry in entries[:5]:  # Process first 5 entries for testing
        if all(key in entry for key in [column_name1, column_name2, column_name3, column_name4]):
            clean_repo_name = entry[column_name1].replace('/', '_').replace('\\', '_').rstrip('_')
            process_view(clean_repo_name, entry[column_name2], entry[column_name3], entry[column_name4])
            print(f"Processed entry: {clean_repo_name}")
        else:
            print(f"Skipping entry due to missing required fields: {entry}")

    print("✅ Results saved in results folder.")

if __name__ == "__main__":
    main()