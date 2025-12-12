import os
import subprocess
from openai import OpenAI
import json
import glob
import shutil
import tempfile
import anthropic
from pathlib import Path
import boto3
from botocore.exceptions import ClientError
# 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
# client = anthropic.Anthropic(api_key="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")
def get_python_from_summary(view_details, error_message=None, python_library="diagrams", code=None):
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
    user_prompt = "Generate an architectural view diagram."

    client = boto3.client(
        service_name='bedrock-runtime',
        region_name='us-west-2',
        aws_access_key_id="ASIA4N3EOZME7FRCLX2I",
        aws_secret_access_key="TJ+FplUv5pebxSGT4GXfKKBFuIN0760RQaTVmJqo",
        aws_session_token="IQoJb3JpZ2luX2VjEOT//////////wEaCXVzLWVhc3QtMSJHMEUCIQCciTd9MxOToMqkJLTwcLGaiInKeFqld+edOiTi6PWKaAIgd2urcmLxqyxioOOEbIDjNqN3vbMZN2g2EuA4ZfhuGyUqmwMIrf//////////ARAAGgw4NTQzNzIzMDU2NzMiDBQMIbroWxR6+p1HXSrvAvuZ0WOIRvEnxHdLTM4MeDuRHRklZIDWfrdJ79UMdBc4+/vHFcGD61X0n0ou8YHDI07GpZv4kW96G1vnhG/QnWtyWY1B7Uem6UsFuabZvsSzaNqtPjS6qX38HeqFNr/aiUQKLpLCc2NrCyq06sPUZ8ag3F4KR1kQq6FhHt1TzuKSSDxqYfFloq8XAOUZWb7IDPvo98XT1SfCuCZ/NHBXI99dgwbA/srrQNp/moQyk4JHvEiSVxmKNckIoYNGGme4CsBhcfvcG41U10aXlhcqzuynpzlTfRyFblZlRvzXgJQrvCOeJTThme0LMQ27puEdSjnzoK1zpR1QybPGcK6cOZxU1JP3vZjMs2uG1p2YQBwUjKLDTin+Qb5+obv0pc/l/yzxpWFGYbW1FCJAYNSL3jl9Am5hXV88ZSsjGJC7lwS50d4Q8uaRMoJ1uWUL+dO99l441/4zwTvUDEboVPHnkmMpDwfBU+oVwmIC924tPjMw6pHsyAY6pAFDZG7UTRMwSGfRNi+JL/Vv8Yd9KS+67JbESgFWYe9zIlZIDeRf7llcCHDki0VOF6e4sBai0tJw5OAA16IzC1KuOaN4hHW2tDi5zU4YkMVRU3cjb9N/czqSejrD+3nOrP1ioph03ShF04w+oSB9sqqY1KwsBhZQIKDh2qF6NC/Ox9bHeULdvLrf5d3GbWJypJTRcFHfikyRK63gaHVZXWeVsdHS5g=="        )
    
    model_id = "anthropic.claude-3-5-sonnet-20241022-v2:0"
    
    # Format the request payload using Bedrock's structure
    native_request = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "temperature": 0.7,
        "system": system_prompt + retry_instruction if error_message else system_prompt,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": user_prompt}]
            }
        ]
    }
    
    # Convert to JSON
    request = json.dumps(native_request)
    
    try:
        # Invoke the model
        response = client.invoke_model(modelId=model_id, body=request)
        
        # Parse the response
        model_response = json.loads(response["body"].read())
        
        # Extract and return the response text
        return model_response["content"][0]["text"]
        
    except (ClientError, Exception) as e:
        return f"Error: {e}"



def save_code(python_code, repo_name):
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


def compile_python(repo_name, input_path, output_dir="./approach_claude_python_images"):
    """
    Runs a Python script and captures its output file.
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

    # Generate and compile PlantUML code with retry mechanism
    max_retries = 3
    attempt = 0
    cnt=0
    error_message = None
    python_code = None
    python_library = "diagrams"  
    if view_details["Architectural Notation"] == "boxes_and_arrows":
        python_library = "graphviz"
    elif view_details["Architectural Notation"] == "UML":
        python_library = "plantuml"
    # Open log file in append mode
    with open("error.log", "a", encoding="utf-8") as log_file:
        while attempt < max_retries:
            python_code = get_python_from_summary(view_details, error_message=error_message, python_library=python_library, code=python_code)

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
    input_jsonl = "../../../../Architectural_knowledge_extraction/generated_summaries.jsonl"
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
