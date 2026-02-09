'''
This script generates architectural view diagrams based on repository summaries, concerns, and behaviors using the Claude 3.5 Sonnet API.
It implements a one-shot prompting technique to guide the model in generating valid Python code that produces architectural diagrams using libraries
like PlantUML, Graphviz, or Diagrams. The generated code is then
'''
import os
import subprocess
from openai import OpenAI
import json
import glob
import shutil
import tempfile
import anthropic
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Claude client
api_key = os.getenv("CLAUDE_API_KEY")
if not api_key:
    print("⚠️ Warning: CLAUDE_API_KEY not found in environment variables or .env file.")
client = anthropic.Anthropic(api_key=api_key)

def prompt_builder(view_details, error_message=None, code=None):
    """
    Prompt Builder Agent: Constructs comprehensive prompts integrating IEEE architectural 
    view standards (behavior, concerns, granularity), architectural design style specifications,
    extracted architectural information, and view generation instructions.
    Dynamically selects the architectural notation based on metadata.
    
    Args:
        view_details: Dictionary containing architectural metadata
        error_message: Optional error feedback for iterative correction
        code: Previous code attempt if error correction is needed
    
    Returns:
        Tuple of (system_prompt, user_prompt) for view generation
    """
    # Dynamically select python library based on Architectural Notation
    python_library = "diagrams"  
    if view_details.get("Architectural Notation") == "boxes_and_arrows":
        python_library = "graphviz"
    elif view_details.get("Architectural Notation") == "UML":
        python_library = "plantuml"
    
    with open("diagrams_import_reference.txt", "r") as f:
        import_content = ",".join(line.strip() for line in f)

    system_prompt=f"""You are an expert Software Architect specializing in software architecture views and also you are proficient in python. Your task in the hand is generating a python code which represents a view given summary and other meta information.
    You are given architectural knowledge extracted from a software repository. This input includes a summary of the architecture and additional metadata fields that describe different aspects of the architectural view.
    Your task is to **generate valid Python code** that produces a diagram of the architecture described in the summary and metadata.The diagram should represent the architecture visually, incorporating components, connectors, styles, and metadata into the final structure.
    The Python code must be self-contained, executable, and use a standard visualization library {python_library}. Type of diagram should be decided based on the metadata information. Do not return plain text explanations only Python code that, when run, generates the diagram.
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
6.  **Architectural Notation:** Use appropriate syntax given in the metadata and conventions to represent the architectural elements accurately **please use given python library {python_library} as only means of representation**.
7.  Output must be only raw Python code, without any Markdown code fences (no python or ), without explanations, and without surrounding text. The response should begin directly with Python code and end with Python code.
8.  If using 'diagrams' library, please use the imports given in this string {import_content}. Not any other. Please do not hallucinate any other imports.
IMPORTANT NOTE : when using diagrams library, please refer the new documentation to look for the imports as your knowledge is not updated **https://diagrams.mingrammer.com/docs/nodes/**.
PLEASE CHECK FOR THE IMPORTS NEW VERSION AND USE THEM. DO NOT USE THE OLD VERSION. PLEASE REFER TO THE NEW DOCUMENTATION.**https://diagrams.mingrammer.com/docs/nodes/**
"""
    if error_message:
        retry_instruction = f"""**CRITICAL CORRECTION:** A previous attempt failed. You MUST fix the error and generate a valid diagram.
- **Error from previous attempt:** {error_message}
- **Problematic Code to fix:**
{code}
"""
    else:
        retry_instruction = ""
    
    user_prompt = "Generate an architectural view diagram."
    
    # Combine system prompt with retry instruction if error exists
    final_system_prompt = system_prompt + retry_instruction if error_message else system_prompt
    
    return final_system_prompt, user_prompt


def view_generator(system_prompt, user_prompt):
    """
    View Generator Agent: Processes the structured prompt and generates code 
    representing the architecture view.
    
    Args:
        system_prompt: Comprehensive system prompt from Prompt Builder
        user_prompt: User instruction for view generation
    
    Returns:
        Generated Python code as string or error message
    """
    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            temperature=0.7,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_prompt
                        }
                    ]
                }
            ]
        )
        # Return only the text blocks
        return ''.join(part.text for part in response.content if part.type == "text")
    except Exception as e:
        return f"Error: {e}"
        return model_response["content"][0]["text"]
        
    except (ClientError, Exception) as e:
        return f"Error: {e}"



def image_generator(python_code, repo_name):
    os.makedirs("approach_claude_python", exist_ok=True)
    file_path = os.path.join("approach_claude_python", f"{repo_name}.py")
    lines = python_code.strip().splitlines()
    if (len(lines) >= 2 and
            lines[0].strip() == "```python" and
            lines[-1].strip() == "```"):
        lines_to_save = lines[1:-1]
        final_code = "\n".join(lines_to_save)
    else:
        final_code = python_code
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(final_code)
        
    return file_path


def code_compiler(repo_name, input_path, output_dir="./approach_claude_python_images"):
    """
    Image Renderer Agent: Validates the generated code, provides error feedback for 
    iterative correction (maximum three iterations), compiles validated code into 
    visual diagrams, and stores results for evaluation.
    
    Args:
        repo_name: Name of the repository being processed
        input_path: Path to the Python script to execute
        output_dir: Directory to store generated diagrams
    
    Returns:
        Tuple of (success: bool, message: str) - success status and output path or error message
    """
    os.makedirs(output_dir, exist_ok=True)

    with tempfile.TemporaryDirectory() as temp_dir:
        absolute_script_path = os.path.abspath(input_path)
        
        result = subprocess.run(
            ["python3", absolute_script_path], # Use the absolute path here
            capture_output=True, 
            text=True,
            cwd=temp_dir # The script will still run inside the temp directory
        )

        if result.returncode != 0:
            print(f"Error executing script: {input_path}")
            print(result.stderr)
            return False, result.stderr

        # Find the file generated by the script inside the temp directory
        generated_files = glob.glob(os.path.join(temp_dir, "*"))
        if not generated_files:
            error_msg = "Script ran successfully but generated no output file."
            print(error_msg)
            return False, error_msg

        # Move and rename the generated file
        generated_file = generated_files[0]
        ext = os.path.splitext(generated_file)[1]
        final_output_path = os.path.join(output_dir, repo_name + ext)

        shutil.move(generated_file, final_output_path)
        print(f"Successfully generated file: {final_output_path}")
        return True, final_output_path




def process_view(repo_name, view_details):

    # Generate and compile code with retry mechanism (max 3 iterations)
    max_retries = 3
    attempt = 0
    cnt=0
    error_message = None
    python_code = None
    
    # Open log file in append mode
    with open("error.log", "a", encoding="utf-8") as log_file:
        while attempt < max_retries:
            # Prompt Builder: Construct comprehensive prompts and select notation
            system_prompt, user_prompt = prompt_builder(view_details, error_message=error_message, code=python_code)
            
            # View Generator: Generate code from structured prompt
            python_code = view_generator(system_prompt, user_prompt)

            file_path = image_generator(python_code, repo_name)
            
            # Image Renderer: Validate, compile, and store diagram
            success, error_message = code_compiler(repo_name, file_path)

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
            log_file.write(f"Failed to generate valid diagram for {repo_name} after {max_retries} attempts\n")

    return cnt

def main():
    default_input_jsonl = "../../../../Repo_Summary_Extraction/generated_summaries.jsonl"
    input_jsonl = input(f"Enter the path for the input JSONL file [default: {default_input_jsonl}]: ").strip() or default_input_jsonl
    
    global_cnt = 0
    total=1
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
    output_dir = "approach_claude_python_images"
    for entry in entries:
        required_keys = ["Repository Name", "summary", "Concern", "Behavior"]
        if all(key in entry for key in required_keys):
            clean_repo_name = entry["Repository Name"].replace('/', '_').replace('\\', '_').rstrip('_')
            expected_output_path = os.path.join(output_dir, f"{clean_repo_name}.png")
            if os.path.exists(expected_output_path):
                print(f"Skipping {clean_repo_name} — already exists.")
                continue
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

    print(f"Results saved in results folder. Total failed attempts: {global_cnt}")

if __name__ == "__main__":
    main()
