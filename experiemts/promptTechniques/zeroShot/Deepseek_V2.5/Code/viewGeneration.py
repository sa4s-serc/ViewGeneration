import os
import subprocess
from openai import OpenAI
import json
import glob
import shutil
# Initialize DeepSeek client
client = OpenAI(api_key="sk-a18b61e35db14879ba5f975c2efddb32", base_url="https://api.deepseek.com/v1")

def get_plantuml_from_summary(summary, repo_name, concern, behavior, error_message=None, code=None):
    # Decide on diagram type based on behavior
    if behavior == "dynamic":
        diagram_instruction = f'''
You are expert software architect. Your task is to design a view for the system based on the architectural knowledge provided. Use PlantUML diagrams. Based on the following repository summary and system behavior, generate a **PlantUML sequence diagram** to show dynamic interactions.

**Behavioral focus:** {concern}

Ensure the diagram:
- Accurately represents runtime message flow between components or services.
- Matches the described system behavior.
- Is valid PlantUML code with no explanation.
this is the repository name, so please name the generate image the with the same {repo_name}.
'''
    else:
        diagram_instruction = f'''
You are expert software architect. Your task is to design a view for the system based on the architectural knowledge provided. Use PlantUML diagrams. Based on the following repository summary, generate a **PlantUML component diagram** to capture the static architecture. Focus on the architectural concern: **{concern}**.

Ensure the diagram:
- Clearly shows system components and their relationships.
- Highlights how the architecture addresses the specified concern.
- Is valid PlantUML code with no explanation.
this is the repository name, so please name the generate image the with the same {repo_name}.
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


def save_plantuml_code(puml_code, repo_name):
    os.makedirs("zeroShot_deepseek_plantumlcode", exist_ok=True)
    # clean_repo_name = repo_name.replace('/', '_').replace('\\', '_').rstrip('_')
    file_path = os.path.join("zeroShot_deepseek_plantumlcode", f"{repo_name}.puml")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(puml_code)
    return file_path

def compile_plantuml(input_path, output_dir="../zeroShot_deepseek_output_images"):
    os.makedirs(output_dir, exist_ok=True)
    
    # Run PlantUML and capture output
    result = subprocess.run(["plantuml", "-o", output_dir, input_path], 
                          capture_output=True, text=True)
    
    return result.returncode == 0, result.stderr


def process_view(repo_name, summary, concern, behavior):

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
                log_file.write(f"Successfully processed repo {repo_name}\n")
                log_file.write(f"PlantUML diagram generated at {file_path}\n")
                break
            else:
                log_file.write(f"Attempt {attempt + 1}: Error in generating PlantUML for {repo_name}\n")
                log_file.write(f"Error message: {error_message}\n")
                attempt += 1
                
        if attempt == max_retries:
            log_file.write(f"Failed to generate valid PlantUML for {repo_name} after {max_retries} attempts\n")

    return 


def main():
    input_jsonl = "../../../../Architectural_knowledge_extraction/generated_summaries.jsonl"
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

    for entry in entries:
        if all(key in entry for key in [column_name1, column_name2, column_name3, column_name4]):
            clean_repo_name = entry[column_name1].replace('/', '_').replace('\\', '_').rstrip('_')
            process_view(clean_repo_name, entry[column_name2], entry[column_name3], entry[column_name4])
            print(f"Processed entry: {clean_repo_name}")
        else:
            print(f"Skipping entry due to missing required fields: {entry}")

    print("✅ Results saved in results folder.")

if __name__ == "__main__":
    main()
