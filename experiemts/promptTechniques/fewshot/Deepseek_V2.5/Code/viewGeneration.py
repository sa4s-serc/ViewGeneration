import os
import subprocess
from openai import OpenAI
import json
# Initialize DeepSeek client
client = OpenAI(api_key="", base_url="https://api.deepseek.com/v1")

def load_few_shot_example(behavior, json_path="examples.json"):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            examples = json.load(f)
            # Filter examples based on behavior
            return [ex for ex in examples if ex['behavior'] == behavior]
    except Exception as e:
        print(f"Error loading one-shot example: {e}")
        return None

def get_plantuml_from_summary(summary, repo_name, concern, behavior, error_message=None, code=None):
    examples = load_few_shot_example(behavior)

    if not examples:
        return "Error: Failed to load examples for few-shot prompting."

    # Select base instruction
    if behavior == "static":
        diagram_type = "component"
        focus = "- Clearly shows main components and their relationships"
    else:
        diagram_type = "sequence"
        focus = "- Clearly shows runtime interactions between components"

    # Base instruction
    task_instruction = f"""You are an expert software architect. Your job is to design architectural views using PlantUML based on system summaries.

Generate a **PlantUML {diagram_type} diagram** that:
{focus}
- Matches the system **behavior** and addresses the architectural **concern**
- Uses valid PlantUML syntax
- Outputs only PlantUML code (no explanation).
this is the repository name, so please name the generate image the with the same {repo_name}.
Below are some examples which have the architectural knowledge summary and corresponding plantuml code for reference.
"""

    # Append multiple few-shot examples
    for i, ex in enumerate(examples):
        task_instruction += f"""

### Example {i + 1} Input:
Summary: {ex['summary']}
Concern: {ex['concern']}
Behavior: {ex['behavior']}

### Example {i + 1} Output:
{ex['plantuml_code']}
"""

    if error_message:
        task_instruction += f"""\n\nNote: A previous attempt failed with:
Error: {error_message}
Problematic code:
{code}
Please regenerate correctly.
"""

    # Final messages with actual input
    messages = [
        {"role": "system", "content": task_instruction},
        {
            "role": "user",
            "content": f"""### Actual Input:
Summary: {summary}
Concern: {concern}
Behavior: {behavior}

Please generate the appropriate PlantUML diagram."""
        }
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
    os.makedirs("fewShot_deepseek_plantumlcode", exist_ok=True)
    file_path = os.path.join("fewShot_deepseek_plantumlcode", f"{repo_name}.puml")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(puml_code)
    return file_path

def compile_plantuml(input_path, output_dir="../fewShot_deepseek_output_images"):
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
