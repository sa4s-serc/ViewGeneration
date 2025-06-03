import os
import subprocess
import openai
import pandas as pd
import csv
import re
import json
import shutil

with open("openai_key.txt", "r") as file:
    openai.api_key = file.read().strip()

def get_plantuml_from_summary(summary, repo_name, concern, behavior, error_message=None, code=None):
    # Decide on diagram type based on behavior
    if behavior== "static":
        diagram_instruction = f'''
You are expert software architect.Your task at the hand is to design view for the system based on the architectural knowledge given about the system. To generate the view you should use plantuml diagrams. Based on the following repository summary, generate a **plantuml component diagram** that captures the static architecture of the system. To design the view, Focus on the architectural concern: **{concern}**.

Ensure the diagram:
- Clearly shows system components and their relationships.
- Highlights how the architecture addresses the specified concern.
- Is syntactically correct PlantUML code and contains no commentary.
'''
    elif behavior == "dynamic":
        diagram_instruction = f'''
You are expert software architect.Your task at the hand is to design view for the system based on the architectural knowledge given about the system. To generate the view you should use plantuml diagrams. Based on the following repository summary and system behavior, generate a **plantuml sequence diagram** to illustrate the dynamic interactions in the system.

**Behavioral focus:** {concern}

Ensure the diagram:
- Accurately represents runtime message flow between components or services.
- Aligns with the described system behavior.
- Is syntactically correct PlantUML code and contains no commentary.
'''

    # Include retry guidance if needed
    if error_message:
        diagram_instruction += f"\nNote: A previous attempt failed with the following error:\n{error_message}\nProblematic code:\n{code}\nPlease correct and regenerate."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": diagram_instruction},
                {"role": "user", "content": summary}
            ],
            temperature=0.7
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {e}"


def save_plantuml_code(puml_code, repo_name):
    os.makedirs("zerShot_gpt_plantumlcode", exist_ok=True)
    clean_repo_name = repo_name.replace('/', '_').replace('\\', '_').rstrip('_')
    file_path = os.path.join("zerShot_gpt_plantumlcode", f"{clean_repo_name}.puml")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("@startuml\n")
        file.write(puml_code)
        file.write("\n@enduml")
    return file_path

def compile_plantuml(input_path, output_dir="../zeroShot_gpt_output_images"):
    os.makedirs(output_dir, exist_ok=True)
    
    # Run PlantUML and capture output
    result = subprocess.run(["plantuml", "-o", ".", input_path], cwd=os.path.dirname(input_path), capture_output=True, text=True)

    
    return result.returncode == 0, result.stderr

def process_view(repo_url, summary, concern, behavior):

    repo_name = repo_url.split('github.com/')[-1].rstrip('/')
    
    # Generate and compile PlantUML code with retry mechanism
    max_retries = 3
    attempt = 0
    
    # Open log file in append mode
    with open("error.log", "a", encoding="utf-8") as log_file:
        while attempt < max_retries:
            puml_code = get_plantuml_from_summary(summary, repo_name, concern, behavior,
                                                error_message=None if attempt == 0 else error_message, code=None if attempt == 0 else puml_code)
            file_path = save_plantuml_code(puml_code, repo_name)
            success, error_message = compile_plantuml(file_path)
            
            if success:
                log_file.write(f"Successfully processed repo {repo_url}\n")
                log_file.write(f"PlantUML diagram generated at {file_path}\n")
                break
            else:
                log_file.write(f"Attempt {attempt + 1}: Error in generating PlantUML for {repo_url}\n")
                log_file.write(f"Error message: {error_message}\n")
                attempt += 1
                
        if attempt == max_retries:
            log_file.write(f"Failed to generate valid PlantUML for {repo_url} after {max_retries} attempts\n")
    
    return 

def main():
    input_csv = "../../../Architectural_knowledge_extraction/generated_summaries.csv"
    column_name1 = "repo_url"
    column_name2 = "summary"
    column_name3 = "concern"
    column_name4 = "behavior"
    df = pd.read_csv(input_csv, delimiter=";", encoding="utf-8", on_bad_lines="skip")
    if column_name1 not in df.columns or column_name2 not in df.columns or column_name3 not in df.columns or column_name4 not in df.columns:
        print(f"Error: Columns '{column_name1}' or '{column_name2}' not found in CSV file.")
        return
    for index, row in df.iterrows():
        process_view(row[column_name1], row[column_name2], row[column_name3], row[column_name4])

    print(f"Results saved in results folder.")

if __name__ == "__main__":
    main() 