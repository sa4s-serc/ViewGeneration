import os
import subprocess
from openai import OpenAI
import json
import glob
import shutil
import tempfile
client = OpenAI(api_key="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")

def get_python_from_summary(view_details, error_message=None, code=None):
    # The System Prompt now contains all instructions and constraints.
    # It is more direct and uses a numbered list for clarity.
    system_prompt="""You are an expert Software Architect specializing in software architecture views and also you are proficient in python. Your task in the hand is generating a python code which represents a view given summary and other meta information.
    You are given architectural knowledge extracted from a software repository. This input includes a summary of the architecture and additional metadata fields that describe different aspects of the architectural view.
    Your task is to **generate valid Python code** that produces a diagram of the architecture described in the summary and metadata.The diagram should represent the architecture visually, incorporating components, connectors, styles, and metadata into the final structure.
    The Python code must be self-contained, executable, and use a standard visualization library such as graphviz, diagrams, networkx, or plantuml. Type of diagram should be decided based on the metadata information. Do not return plain text explanations only Python code that, when run, generates the diagram.
    Below is the detailed explanation of the each field of metadata.
    {view_details["summary"]} provides a textual description of the architecture and should be treated as the primary guide for the overall structure and relationships in the diagram.
    {view_details["Concern"]} describes the main purpose or goal of this architectural view, such as performance, scalability, or maintainability, and the diagram should highlight this focus accordingly.
    {view_details["Behavior"]} denotes the system behavior, these should be represented through connectors, arrows, or annotations where appropriate.
    {view_details["Granularity"]} indicates the level of abstraction, whether at the system, subsystem, module, or component level, and should guide whether the diagram depicts coarse-grained or fine-grained elements.
    {view_details["Components Nature"]} specifies the types of elements involved, such as services, APIs, classes, etc., and these must be represented as nodes in the diagram.
    {view_details["Connectors Nature"]} describes the ways in which these components communicate, such as through function calls, REST APIs, message queues, etc., and these interactions should be shown as edges styled appropriately.
    {view_details["QAs"]} outline non-functional requirements like scalability, fault tolerance, or security; the diagram should visually suggest how these qualities are addressed.
    {view_details["Architecture Scope"]} defines the breadth of the view, whether it represents the entire system, a subsystem, or a specific feature slice, and the diagram should remain consistent with this scope.
    {view_details["Architectural Notation"]} identifies whether the description follows UML, icons and arrows, or informal diagramming conventions, and the choice of notation should inform the diagram’s node and connector styles.
    {view_details["Architectural Styles"]} identifies whether the description follows layered, microservices, client-server, event-driven, or hexagonal styles, and the choice of style should inform the diagram’s structure.
    {view_details["Shapes"]} and {view_details["Colored?"]} fields specify how nodes should be visually represented and whether different types of components or technologies should be distinguished with colors or not.
    {view_details["Connectors Direction"]} indicates whether links are unidirectional, bidirectional, or mixed, and should be represented with suitable arrow styles.
    {view_details["Legend?"]} gives information about legend presence, {view_details["Nested Components?"]} notifies the presence of components within other components, {view_details["Explicit Ports/Interfaces?"]} notifies the presence of explicit ports or interfaces, {view_details["Explicit Connectors?"]} notifies the presence of explicit connectors.
    **Instructions & Constraints:**
1.  **Output Format:** Your response MUST contain ONLY the Python code. Do not include any explanations, apologies, or markdown fences.
2.  **Adherence to Data:** The diagram must accurately represent the components, connectors, behaviors, and architectural styles described in the user's metadata.
3.  **Architectural Reasoning:** Apply your knowledge of software architecture to create a logical and well-structured diagram that respects the specified concern and scope.
4.  **Completeness:** Ensure all key components and their primary relationships from the metadata are visible in the diagram.
5.  **Clarity:** You are also specializing in creating clear diagrams in a 'box and arrows' style using Python syntax.
6.  **Architectural Notation:** Use appropriate syntax given in the metadata and conventions to represent the architectural elements accurately **please use python as only means of representation**.

"""
    if error_message:
        retry_instruction = f"""**CRITICAL CORRECTION:** A previous attempt failed. You MUST fix the error and generate a valid diagram.
- **Error from previous attempt:** {error_message}
- **Problematic Code to fix:**
{code}
"""

    user_prompt="Generate an architectural view diagram."
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt + retry_instruction if error_message else system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=1024,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"


def save_code(python_code, repo_name):
    os.makedirs("zeroShot_gpt_python", exist_ok=True)
    # clean_repo_name = repo_name.replace('/', '_').replace('\\', '_').rstrip('_')
    file_path = os.path.join("zeroShot_gpt_python", f"{repo_name}.py")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(python_code)
    return file_path



def compile_python(repo_name, input_path, output_dir="./zeroShot_gpt_python"):
    os.makedirs(output_dir, exist_ok=True)

    with tempfile.TemporaryDirectory() as temp_dir:
        # Run PlantUML in temporary directory
        result = subprocess.run(
            ["python3", temp_dir, input_path],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            return False, result.stderr
        # Find the generated file (e.g., .png)
        generated_files = glob.glob(os.path.join(temp_dir, "*"))
        if not generated_files:
            return False, "No file generated by Python."

        # Assume one diagram per file — take the first
        generated_file = generated_files[0]
        ext = os.path.splitext(generated_file)[1]
        output_path = os.path.join(output_dir, repo_name + ext)

        shutil.move(generated_file, output_path)

        return True, None



def process_view(repo_name, view_details):

    # Generate and compile PlantUML code with retry mechanism
    max_retries = 3
    attempt = 0
    cnt=0
    error_message = None
    python_code = None
    # Open log file in append mode
    with open("error.log", "a", encoding="utf-8") as log_file:
        while attempt < max_retries:
            python_code = get_python_from_summary(view_details, error_message=error_message, code=python_code)

            file_path = save_code(python_code, repo_name)
            success, error_message = compile_python(repo_name, file_path)

            if success:
                log_file.write(f"Successfully processed repo {repo_name}\n")
                log_file.write(f"Python script generated at {file_path}\n")
                break
            else:
                log_file.write(f"Attempt {attempt + 1}: Error in generating Python script for {repo_name}\n")
                log_file.write(f"Error message: {error_message}\n")
                attempt += 1
                
        if attempt == max_retries:
            cnt+=1
            log_file.write(f"Failed to generate valid PlantUML for {repo_name} after {max_retries} attempts\n")

    return cnt

def main():
    input_jsonl = "../../experiments/Architectural_knowledge_extraction/generated_summaries.jsonl"
    global_cnt = 0
    total=0
    try:
        with open(input_jsonl, 'r', encoding='utf-8') as f:
            entries = [json.loads(line) for line in f]
    except Exception as e:
        print(f"Error reading JSONL file: {e}")
        return
    key_mapping = {
        "Repository Name",
        "summary",
        "Concern",
        "Behavior",
        "Granularity",
        "Components Nature",
        "Connectors Nature",
        "QAs",
        "Architecture Scope",
        "Architectural Notation",
        "Architectural Styles",
        "Shapes",
        "Colored?",
        "Connectors Direction",
        "Legend?",
        "Nested Components?",
        "Explicit Ports/Interfaces?",
        "Explicit Connectors?",
    }

    for entry in entries:
        required_keys = ["Repository Name", "summary", "Concern", "Behavior"]
        # if total>10:
        #     break
        if all(key in entry for key in required_keys):
            clean_repo_name = entry["Repository Name"].replace('/', '_').replace('\\', '_').rstrip('_')
            
            view_details = {}
            for json_key in key_mapping:
                if entry.get(json_key):
                    value = entry[json_key]
                    view_details[json_key] = value

            global_cnt += process_view(clean_repo_name, view_details)
            total += 1
            print(f"Processed entry: {clean_repo_name}")
        else:
            print(f"Skipping entry due to missing required fields: {entry}")

    print(f"✅ Results saved in results folder. Total failed attempts: {global_cnt}")

if __name__ == "__main__":
    main()
