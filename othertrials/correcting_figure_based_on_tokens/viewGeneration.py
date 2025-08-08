import os
import subprocess
from openai import OpenAI
import json
import glob
import shutil
import tempfile
import tiktoken

client = OpenAI(api_key="")

AVERAGE_CODE_TOKENS_BY_GRANULARITY = {
    "high": 292,
    "medium": 582,
    "low": 900
}

def count_tokens(text, model="gpt-4"):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def get_plantuml_from_summary(summary, repo_name, concern, behavior, error_message=None, code=None, granularity_note=None):
    # Decide on diagram type based on behavior
    if behavior == "dynamic":
        diagram_instruction = f'''
You are expert software architect. Your task is to design a view for the system based on the architectural knowledge provided. Use PlantUML diagrams. Based on the following repository summary and system behavior, generate a **PlantUML sequence diagram** to show dynamic interactions.

**Behavioral focus:** {concern}
'''
    else:
        diagram_instruction = f'''
You are expert software architect. Your task is to design a view for the system based on the architectural knowledge provided. Use PlantUML diagrams. Based on the following repository summary, generate a **PlantUML component diagram** to capture the static architecture. Focus on the architectural concern: **{concern}**.
'''

    # Add granularity guidance if available
    if granularity_note:
        diagram_instruction += f"\n{granularity_note.strip()}\n"

    # Add retry guidance if error message exists
    if error_message:
        diagram_instruction += f"\nNote: A previous attempt failed with the following error:\n{error_message}\nProblematic code:\n{code}\nPlease correct and regenerate."

    # Final instruction rules
    diagram_instruction += f'''
Ensure the diagram:
- Clearly shows system components and their relationships.{"\n- Accurately represents runtime message flow between components or services." if behavior == "dynamic" else ""}
- Matches the described system behavior if applicable.
- Is valid PlantUML code with no explanation.
This is the repository name, so please name the generated image with the same: **{repo_name}**.
'''

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
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

def ensure_code_matches_granularity(summary, repo_name, concern, behavior, granularity):
    expected_avg = AVERAGE_CODE_TOKENS_BY_GRANULARITY.get(granularity.lower())
    if expected_avg is None:
        print(f"[WARN] Unknown granularity '{granularity}'. Defaulting to 'medium' average.")
        expected_avg = AVERAGE_CODE_TOKENS_BY_GRANULARITY["medium"]

    # Initial generation
    puml_code = get_plantuml_from_summary(summary, repo_name, concern, behavior)
    token_count = count_tokens(puml_code)
    save_plantuml_code(puml_code, repo_name)

    if abs(token_count - expected_avg) <= 100:
        print(f"[OK] Token count {token_count} matches expected average ({expected_avg}) ±100 for '{granularity}' granularity.")
        return

    print(f"[RETRY] Token count {token_count} deviates from expected average ({expected_avg}) for '{granularity}' granularity.")

    # Granularity-specific guidance added to system prompt
    granularity_note = f"""
The PlantUML code should reflect **{granularity} granularity**.
Adjust the level of architectural detail so that the output aligns with approximately {expected_avg} tokens — either increasing or reducing complexity as needed.
"""

    regenerated_code = get_plantuml_from_summary(
        summary=summary,
        repo_name=repo_name,
        concern=concern,
        behavior=behavior,
        granularity_note=granularity_note
    )

    new_token_count = count_tokens(regenerated_code)
    save_plantuml_code(regenerated_code, repo_name)

    print(f"[INFO] Retried token count: {new_token_count} (expected ~{expected_avg})")


def save_plantuml_code(puml_code, repo_name):
    os.makedirs("zeroShot_gpt_plantumlcode", exist_ok=True)
    # clean_repo_name = repo_name.replace('/', '_').replace('\\', '_').rstrip('_')
    file_path = os.path.join("zeroShot_gpt_plantumlcode", f"{repo_name}.puml")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(puml_code)
    return file_path



def compile_plantuml(repo_name, input_path, output_dir="../zeroShot_gpt_output_images"):
    os.makedirs(output_dir, exist_ok=True)

    with tempfile.TemporaryDirectory() as temp_dir:
        # Run PlantUML in temporary directory
        result = subprocess.run(
            ["plantuml", "-o", temp_dir, input_path],
            capture_output=True, text=True
        )

        if result.returncode != 0:
            return False, result.stderr

        # Find the generated file (e.g., .png)
        generated_files = glob.glob(os.path.join(temp_dir, "*"))
        if not generated_files:
            return False, "No file generated by PlantUML."

        # Assume one diagram per file — take the first
        generated_file = generated_files[0]
        ext = os.path.splitext(generated_file)[1]
        output_path = os.path.join(output_dir, repo_name + ext)

        shutil.move(generated_file, output_path)

        return True, None



def process_view(repo_name, summary, concern, behavior, granularity):
    max_retries = 3
    attempt = 0
    cnt = 0

    # Open log file in append mode
    with open("error.log", "a", encoding="utf-8") as log_file:
        while attempt < max_retries:
            # Step 1: Generate PlantUML code matching granularity
            puml_code = ensure_code_matches_granularity(summary, repo_name, concern, behavior, granularity)
            
            # Step 2: Save the code
            file_path = save_plantuml_code(puml_code, repo_name)

            # Step 3: Try to compile it
            success, error_message = compile_plantuml(repo_name, file_path)

            if success:
                log_file.write(f"Successfully processed repo {repo_name}\n")
                log_file.write(f"PlantUML diagram generated at {file_path}\n")
                break
            else:
                log_file.write(f"Attempt {attempt + 1}: Error in compiling PlantUML for {repo_name}\n")
                log_file.write(f"Error message: {error_message}\n")
                attempt += 1

        if attempt == max_retries:
            cnt += 1
            log_file.write(f"Failed to generate valid PlantUML for {repo_name} after {max_retries} attempts\n")

    return cnt


def main():
    input_jsonl = "../../experiments/Architectural_knowledge_extraction/generated_summaries.jsonl"
    column_name1 = "Repository Name"
    column_name2 = "summary"
    column_name3 = "Concern"
    column_name4 = "Behavior"
    column_name5 = "Granularity"
    global_cnt=0

    try:
        with open(input_jsonl, 'r', encoding='utf-8') as f:
            entries = [json.loads(line) for line in f]
    except Exception as e:
        print(f"Error reading JSONL file: {e}")
        return

    for entry in entries:
        if all(key in entry for key in [column_name1, column_name2, column_name3, column_name4]):
            clean_repo_name = entry[column_name1].replace('/', '_').replace('\\', '_').rstrip('_')
            global_cnt += process_view(clean_repo_name, entry[column_name2], entry[column_name3], entry[column_name4],entry[column_name5])
            print(f"Processed entry: {clean_repo_name}")
        else:
            print(f"Skipping entry due to missing required fields: {entry}")

    print(f"✅ Results saved in results folder. Total failed attempts: {global_cnt}")

if __name__ == "__main__":
    main()
