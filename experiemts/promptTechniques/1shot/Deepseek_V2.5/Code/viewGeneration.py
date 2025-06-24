import os
import subprocess
from openai import OpenAI
import json
# Initialize DeepSeek client
client = OpenAI(api_key="", base_url="https://api.deepseek.com/v1")

def load_one_shot_example(json_path="example_prompts.json"):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading one-shot example: {e}")
        return None

def get_plantuml_from_summary(summary, repo_name, concern, behavior, error_message=None, code=None):
    example = load_one_shot_example()  

    if not example:
        return "Error: Failed to load example for one-shot prompting."

    # Select instruction template based on behavior
    if behavior == "static":
        diagram_type = "component diagram"
        diagram_goal = "- Clearly shows the main components and their relationships"
    else:
        diagram_type = "sequence diagram"
        diagram_goal = "- Captures runtime interactions between components"

    task_instruction = f"""You are expert software architect. Your task is to design a view for the system based on the architectural knowledge provided. Use PlantUML diagrams. 
For {behavior} architecture, generate a **PlantUML {diagram_type}** that:
{diagram_goal}
- Matches the system **behavior**
- Addresses the architectural **concern**
- Uses valid PlantUML syntax
- Outputs only PlantUML code (no explanation)
this is the repository name, so please name the generate image the with the same {repo_name}.
Below is the example of a valid PlantUML code along with corresponding summary for reference:
"""

    if error_message:
        task_instruction += f"\nNote: A previous attempt failed with:\n{error_message}\nProblematic code:\n{code}\nPlease regenerate correctly."

    # Combine into one system message
    system_message = f"""{task_instruction}

### Example Input:
Summary: {example['summary']}
Concern: {example['concern']}
Behavior: {example['behavior']}

### Example Output:
{example["plantuml_code"]}
"""

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"""### Actual Input:
Summary: {summary}
Concern: {concern}
Behavior: {behavior}

Please generate the appropriate PlantUML diagram."""}
    ]

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"



def save_plantuml_code(puml_code, repo_name):
    os.makedirs("oneShot_deepseek_plantumlcode", exist_ok=True)
    file_path = os.path.join("oneShot_deepseek_plantumlcode", f"{repo_name}.puml")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(puml_code)
    return file_path

def compile_plantuml(input_path, output_dir="../oneShot_deepseek_output_images"):
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
    input_jsonl = "../../../Architectural_knowledge_extraction/generated_summaries.jsonl"
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

    for entry in entries[:5]:
        if all(key in entry for key in [column_name1, column_name2, column_name3, column_name4]):
            clean_repo_name = entry[column_name1].replace('/', '_').replace('\\', '_').rstrip('_')
            process_view(clean_repo_name, entry[column_name2], entry[column_name3], entry[column_name4])
            print(f"Processed entry: {clean_repo_name}")
        else:
            print(f"Skipping entry due to missing required fields: {entry}")

    print("✅ Results saved in results folder.")

if __name__ == "__main__":
    main()
