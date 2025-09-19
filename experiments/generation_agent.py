"""
Generation agent example:
- Generates Python diagram code from architectural summaries and metadata
- Compiles the generated Python into an output image/file
- Retries on failure with error-corrective prompting
"""

import os
import subprocess
import json
import glob
import shutil
import tempfile
from typing import Dict, Any, Tuple
from moya.agents.openai_agent import OpenAIAgent, OpenAIAgentConfig

class GenerationAgent(OpenAIAgent):
    def __init__(self, config):
        super().__init__(config)

    def generate_python_from_summary(self, view_details: Dict[str, Any], error_message: str = None, previous_code: str = None) -> str:
        system_prompt = f"""You are an expert Software Architect specializing in software architecture views and also you are proficient in python. Your task in the hand is generating a python code which represents a view given summary and other meta information.
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
7.  Output must be only raw Python code, without any Markdown code fences (no python or ), without explanations, and without surrounding text. The response should begin directly with Python code and end with Python code.
"""

        retry_instruction = ""
        if error_message:
            retry_instruction = (
                f"\nCRITICAL CORRECTION: A previous attempt failed. You MUST fix the error and generate a valid diagram.\n"
                f"Error from previous attempt: {error_message}\n"
                f"Problematic Code to fix:\n{previous_code or ''}\n"
            )

        # Keep the user prompt identical to your reference implementation
        user_prompt = "Generate an architectural view diagram."

        message = self.get_response([
            {"role": "system", "content": system_prompt + retry_instruction},
            {"role": "user", "content": user_prompt},
        ])
        code = (message.get("content", "") if isinstance(message, dict) else "").strip()
        return code

    def save_code(self, python_code: str, repo_name: str) -> str:
        os.makedirs("zeroShot_gpt_python", exist_ok=True)
        file_path = os.path.join("zeroShot_gpt_python", f"{repo_name}.py")
        lines = python_code.strip().splitlines()
        if (len(lines) >= 2 and lines[0].strip() == "```python" and lines[-1].strip() == "```"):
            lines_to_save = lines[1:-1]
            final_code = "\n".join(lines_to_save)
        else:
            final_code = python_code
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(final_code)
        return file_path

    def compile_python(self, repo_name: str, input_path: str, output_dir: str = "./zeroShot_gpt_python_images") -> Tuple[bool, str]:
        os.makedirs(output_dir, exist_ok=True)
        with tempfile.TemporaryDirectory() as temp_dir:
            absolute_script_path = os.path.abspath(input_path)
            result = subprocess.run(
                ["python3", absolute_script_path],
                capture_output=True,
                text=True,
                cwd=temp_dir
            )

            if result.returncode != 0:
                return False, result.stderr

            generated_files = glob.glob(os.path.join(temp_dir, "*"))
            if not generated_files:
                return False, "Script ran successfully but generated no output file."

            generated_file = generated_files[0]
            ext = os.path.splitext(generated_file)[1]
            final_output_path = os.path.join(output_dir, repo_name + ext)
            shutil.move(generated_file, final_output_path)
            return True, final_output_path

    def process_view(self, repo_name: str, view_details: Dict[str, Any]) -> int:
        max_retries = 3
        attempt = 0
        failures = 0
        error_message = None
        python_code = None
        os.makedirs(".", exist_ok=True)
        with open("error.log", "a", encoding="utf-8") as log_file:
            while attempt < max_retries:
                python_code = self.generate_python_from_summary(view_details, error_message=error_message, previous_code=python_code)
                file_path = self.save_code(python_code, repo_name)
                success, result = self.compile_python(repo_name, file_path)
                if success:
                    log_file.write(f"Successfully processed repo {repo_name}\n")
                    log_file.write(f"Python script generated at {file_path}\n")
                    break
                else:
                    log_file.write(f"Attempt {attempt + 1}: Error in generating Python script for {repo_name}\n")
                    log_file.write(f"Error message: {result}\n")
                    error_message = result
                    attempt += 1
        if attempt == max_retries:
            failures += 1
            with open("error.log", "a", encoding="utf-8") as log_file:
                log_file.write(f"Failed to generate valid Python diagram for {repo_name} after {max_retries} attempts\n")
        return failures

def main():
    config = OpenAIAgentConfig(
        agent_name="generation_agent",
        description="Agent that generates Python diagram code from architectural summaries and compiles outputs.",
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name="gpt-4o",
        agent_type="GenerationAgent",
        is_streaming=False,
        system_prompt="You are an agent that generates executable Python diagram code from architectural metadata."
    )
    agent = GenerationAgent(config)

    # Single-input mode: assume another agent provides summary + metadata
    # Prompt for repo/display name, summary text, and metadata JSON
    repo_name = input("Enter repository/view name (for output filename): ").strip()
    summary = input("Paste summary text: ").strip()
    print("Paste metadata JSON (keys like Concern, Behavior, Granularity, etc.). Press Enter for defaults:")
    metadata_raw = input().strip()
    try:
        metadata = json.loads(metadata_raw) if metadata_raw else {}
    except Exception as e:
        print(f"Invalid metadata JSON, using defaults. Error: {e}")
        metadata = {}

    view_details: Dict[str, Any] = {
        "Repository Name": repo_name,
        "summary": summary,
        "Concern": metadata.get("Concern", ""),
        "Behavior": metadata.get("Behavior", ""),
        "Granularity": metadata.get("Granularity", ""),
        "Components Nature": metadata.get("Components Nature", ""),
        "Connectors Nature": metadata.get("Connectors Nature", ""),
        "QAs": metadata.get("QAs", ""),
        "Architecture Scope": metadata.get("Architecture Scope", ""),
        "Architectural Notation": metadata.get("Architectural Notation", ""),
        "Architectural Styles": metadata.get("Architectural Styles", ""),
        "Shapes": metadata.get("Shapes", ""),
        "Colored?": metadata.get("Colored?", ""),
        "Connectors Direction": metadata.get("Connectors Direction", ""),
        "Legend?": metadata.get("Legend?", ""),
        "Nested Components?": metadata.get("Nested Components?", ""),
        "Explicit Ports/Interfaces?": metadata.get("Explicit Ports/Interfaces?", ""),
        "Explicit Connectors?": metadata.get("Explicit Connectors?", ""),
    }

    os.makedirs("zeroShot_gpt_python_images", exist_ok=True)
    failures = agent.process_view(repo_name.replace('/', '_').replace('\\', '_').rstrip('_'), view_details)
    print(f"Results saved in zeroShot_gpt_python_images. Failed: {failures}. Processed: {1}")

if __name__ == "__main__":
    main()
