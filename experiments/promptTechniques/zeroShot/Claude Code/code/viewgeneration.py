#!/usr/bin/env python3
"""
Script to generate PlantUML diagrams using claude agent based on architectural summaries.
"""

import os
import subprocess
import json
import time
import sys
import glob
import shutil
import tempfile
from pathlib import Path

def generate_plantuml_prompt(repo_name, summary, concern, behavior, error_message=None, previous_code=None):
    """
    Generate a prompt for claude to create PlantUML diagrams.
    This replaces the API call to generate PlantUML code.
    
    Args:
        repo_name (str): Name of the repository
        summary (str): Architectural summary
        concern (str): Architectural concern to focus on
        behavior (str): "dynamic" or "static" behavior type
        error_message (str): Error from previous attempt (for retry)
        previous_code (str): Previous PlantUML code that failed (for retry)
        
    Returns:
        str: Complete prompt for claude
    """
    
    if behavior == "dynamic":
        diagram_type = "sequence diagram"
        diagram_focus = f"""
**Diagram Type:** PlantUML Sequence Diagram (for dynamic interactions)
**Behavioral Focus:** {concern}

The diagram should:
- Accurately represent runtime message flow between components or services
- Show dynamic interactions and communication patterns
- Use proper sequence diagram syntax with participants, messages, and activations
- Match the described system behavior from the summary
"""
    else:
        diagram_type = "component diagram"
        diagram_focus = f"""
**Diagram Type:** PlantUML Component Diagram (for static architecture)
**Architectural Concern:** {concern}

The diagram should:
- Clearly show system components and their relationships
- Highlight how the architecture addresses the specified concern
- Use proper component diagram syntax with components, interfaces, and dependencies
- Represent the static structure of the system
"""

    # Build retry context if this is a retry attempt
    retry_context = ""
    if error_message and previous_code:
        retry_context = f"""
IMPORTANT - RETRY ATTEMPT:
A previous PlantUML generation failed with the following error:
```
{error_message}
```

The problematic code was:
```plantuml
{previous_code}
```

Please analyze the error, identify the issue, and generate corrected PlantUML code that compiles successfully.
"""

    prompt = f"""I need you to generate valid PlantUML code based on architectural knowledge.

TASK: Generate a {diagram_type} for the following system.

REPOSITORY: {repo_name}

{diagram_focus}

ARCHITECTURAL SUMMARY:
{summary}

{retry_context}

INSTRUCTIONS:
1. Read and analyze the architectural summary carefully
2. Understand the system components, relationships, and behaviors described
3. Create valid PlantUML code that:
   - Follows PlantUML syntax strictly
   - Is complete and can be compiled without errors
   - Accurately represents the architecture from the summary
   - Focuses on the specified concern: {concern}
   - Uses appropriate PlantUML elements for a {diagram_type}
4. Save the PlantUML code to: zeroShot_claude_plantumlcode/{repo_name}.puml
   - Create the directory if it doesn't exist
   - Save ONLY the PlantUML code (no markdown code blocks like ```plantuml)
   - The file must start with @startuml and end with @enduml
   - No explanations or comments outside the PlantUML code

CRITICAL: You must ONLY generate and save the .puml file. DO NOT compile it or run plantuml command. The compilation will be handled separately by the Python script.

Your expertise in software architecture and PlantUML makes you ideal for creating accurate PlantUML code."""

    return prompt

def run_claude_agent(prompt, repo_name, attempt=1):
    """
    Execute claude command to generate PlantUML code.
    This replaces the API call (get_plantuml_from_summary function).
    
    Args:
        prompt (str): The prompt for claude
        repo_name (str): Repository name for logging
        attempt (int): Attempt number for this generation
        
    Returns:
        tuple: (success: bool, output: str, error: str)
    """
    try:
        # Generate output file name
        output_file = f"./claude_logs/claude-{repo_name}-attempt{attempt}-output.log"
        error_file = f"./claude_logs/claude-{repo_name}-attempt{attempt}-error.log"
        
        # Save the prompt for debugging
        prompt_file = f"./claude_logs/claude-{repo_name}-attempt{attempt}-prompt.txt"
        try:
            with open(prompt_file, 'w', encoding='utf-8') as pf:
                pf.write(prompt)
        except Exception as e:
            print(f"    Warning: Could not save prompt file: {e}")
        
        # Use subprocess without shell=True to avoid escaping issues
        # Pass prompt directly as argument (no shell interpretation)
        try:
            with open(output_file, 'w', encoding='utf-8') as out_f, \
                 open(error_file, 'w', encoding='utf-8') as err_f:
                result = subprocess.run(
                    ['claude', prompt, '--dangerously-skip-permissions'],
                    stdout=out_f,
                    stderr=err_f,
                    timeout=600  # 10 minutes timeout per diagram
                )
        except FileNotFoundError:
            return False, "", "claude command not found. Is 'claude' installed and in PATH?"
        
        # Read the output file
        output = ""
        if os.path.exists(output_file):
            try:
                with open(output_file, 'r', encoding='utf-8') as f:
                    output = f.read()
            except Exception as e:
                output = f"Error reading output file: {str(e)}"
        
        # Read the error file
        error = ""
        if os.path.exists(error_file):
            try:
                with open(error_file, 'r', encoding='utf-8') as f:
                    error = f.read()
            except Exception as e:
                error = f"Error reading error file: {str(e)}"
        
        # If both are empty but command failed, provide context
        if result.returncode != 0 and not output and not error:
            error = f"claude command failed with return code {result.returncode} but produced no output"
        
        return result.returncode == 0, output, error
        
    except subprocess.TimeoutExpired:
        return False, "", "claude command timed out after 10 minutes"
    except Exception as e:
        return False, "", f"Error running claude command: {str(e)}"

def save_plantuml_code(repo_name):
    """
    Verify that claude agent saved the PlantUML code correctly.
    This replaces the save_plantuml_code function but only verifies (agent does the saving).
    
    Args:
        repo_name (str): Repository name
        
    Returns:
        tuple: (success: bool, file_path: str or None)
    """
    file_path = os.path.join("zeroShot_claude_plantumlcode", f"{repo_name}.puml")
    
    if not os.path.exists(file_path):
        return False, None
    
    # Verify the file is not empty and has valid content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        if not content: 
            return False, None
        
        # Check for markdown artifacts
        if content.startswith("```"):
            return False, None
            
        # Check for PlantUML markers
        if not content.startswith("@startuml") or not content.endswith("@enduml"):
            return False, None
            
        return True, file_path
    except Exception as e:
        return False, None

def compile_plantuml(repo_name, input_path, output_dir="zeroShot_claude_output_images"):
    """
    Compiles PlantUML code to generate diagram image.
    This is the exact logic from the original compile_plantuml function.
    
    Args:
        repo_name (str): Repository name
        input_path (str): Path to .puml file
        output_dir (str): Output directory for generated images
        
    Returns:
        tuple: (success: bool, error_message: str or None)
    """
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

def process_diagram(repo_name, summary, concern, behavior):
    """
    Process a single diagram generation with retry mechanism.
    claude agent replaces: API call (generates PlantUML code)
    Python handles: save verification + compilation
    
    Args:
        repo_name (str): Repository name
        summary (str): Architectural summary
        concern (str): Architectural concern
        behavior (str): Behavior type (dynamic/static)
        
    Returns:
        int: 1 if failed after all retries, 0 if successful
    """
    max_retries = 3
    attempt = 0
    error_message = None
    previous_code = None
    
    # Open log file in append mode
    log_file_path = "claude_plantuml_generation.log"
    
    with open(log_file_path, "a", encoding='utf-8') as log_file:
        log_file.write(f"\n{'='*70}\n")
        log_file.write(f"Processing: {repo_name}\n")
        log_file.write(f"Concern: {concern}\n")
        log_file.write(f"Behavior: {behavior}\n")
        log_file.write(f"{'='*70}\n")
        
        while attempt < max_retries:
            attempt += 1
            log_file.write(f"\nAttempt {attempt}/{max_retries}...\n")
            log_file.flush()
            
            # STEP 1: Generate prompt (includes retry context if applicable)
            prompt = generate_plantuml_prompt(
                repo_name, 
                summary, 
                concern, 
                behavior,
                error_message=error_message,
                previous_code=previous_code
            )
            
            # STEP 2: Run claude agent to generate PlantUML code (replaces API call)
            print(f"  Attempt {attempt}: Running claude agent to generate PlantUML code...")
            claude_success, output, error = run_claude_agent(prompt, repo_name, attempt)
            
            if not claude_success:
                log_file.write(f"claude agent execution failed: {error}\n")
                error_message = f"claude agent execution failed: {error}"
                continue
            
            # STEP 3: Verify the PlantUML code was saved correctly (replaces save_plantuml_code verification)
            print(f"    → Verifying saved PlantUML code...")
            save_success, file_path = save_plantuml_code(repo_name)
            
            if not save_success:
                log_file.write(f"PlantUML code not saved correctly or invalid format\n")
                error_message = "PlantUML code not saved correctly or invalid format"
                continue
            
            # Read the generated code for potential retry
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    previous_code = f.read()
            except:
                previous_code = None
            
            # STEP 4: Compile the PlantUML code (original compile_plantuml function)
            print(f"    → Compiling PlantUML diagram...")
            compile_success, compile_error = compile_plantuml(repo_name, file_path)
            
            if compile_success:
                log_file.write(f"✅ Successfully generated PlantUML diagram for {repo_name}\n")
                log_file.write(f"   - PlantUML file: {file_path}\n")
                log_file.write(f"   - Output image: zeroShot_claude_output_images/{repo_name}.*\n")
                print(f"  ✅ Success: {repo_name}")
                return 0
            else:
                log_file.write(f"Compilation failed: {compile_error}\n")
                error_message = compile_error
                print(f"  ⚠️  Attempt {attempt} failed: {compile_error}")
        
        # All attempts failed
        log_file.write(f"❌ Failed to generate valid PlantUML for {repo_name} after {max_retries} attempts\n")
        print(f"  ❌ Failed: {repo_name} (after {max_retries} attempts)")
        return 1
def main():
    """Main function to orchestrate PlantUML generation using Claude"""
    print("=== PLANTUML DIAGRAM GENERATION WITH CLAUDE ===\n")
    print("Workflow:")
    print(" 1. Claude agent generates PlantUML code (replaces API call)")
    print(" 2. Python verifies the saved .puml file")
    print(" 3. Python compiles with plantuml command\n")

    # Configuration
    INPUT_JSONL = "../../../../Architectural_knowledge_extraction/generated_summaries.jsonl"
    OUTPUT_CODE_DIR = "zeroShot_claude_plantumlcode"
    OUTPUT_IMAGE_DIR = "zeroShot_claude_output_images"

    # Check if input file exists
    if not os.path.exists(INPUT_JSONL):
        print(f"❌ Error: Input file '{INPUT_JSONL}' not found!")
        print("Please ensure the generated_summaries.jsonl file exists.")
        sys.exit(1)

    # Create output directories
    os.makedirs(OUTPUT_CODE_DIR, exist_ok=True)
    os.makedirs(OUTPUT_IMAGE_DIR, exist_ok=True)

    # Load entries from JSONL
    print(f"Loading entries from {INPUT_JSONL}...")
    try:
        with open(INPUT_JSONL, 'r', encoding='utf-8') as f:
            entries = [json.loads(line) for line in f]
        print(f"✅ Loaded {len(entries)} entries\n")
    except Exception as e:
        print(f"❌ Error reading JSONL file: {e}")
        sys.exit(1)

    # Get user confirmation
    print(f"About to process {len(entries)} repositories using Claude")
    confirm = input("Proceed? (y/n): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("Cancelled.")
        return

    # Process entries
    total_start_time = time.time()
    global_cnt = 0
    processed = 0
    skipped = 0
    existing = 0

    required_fields = ["Repository Name", "summary", "Concern", "Behavior"]

    for idx, entry in enumerate(entries, 1):
        print(f"\n[{idx}/{len(entries)}] Processing entry...")

        # Check if all required fields are present
        if not all(key in entry for key in required_fields):
            print(f" ⚠️ Skipping: Missing required fields")
            print(f" Available fields: {list(entry.keys())}")
            skipped += 1
            continue

        # Clean repository name
        raw_repo_name = entry["Repository Name"]
        clean_repo_name = raw_repo_name.replace('/', '_').replace('\\', '_').rstrip('_')

        # Expected output path
        expected_output_path = os.path.join(OUTPUT_IMAGE_DIR, f"{clean_repo_name}.png")

        # Skip if output already exists
        if os.path.exists(expected_output_path):
            print(f"⏩ Skipping {clean_repo_name} — output already exists.")
            existing += 1
            continue

        print(f" Repository: {raw_repo_name}")
        print(f" Concern: {entry['Concern']}")
        print(f" Behavior: {entry['Behavior']}")

        # Process the diagram
        failed_count = process_diagram(
            clean_repo_name,
            entry["summary"],
            entry["Concern"],
            entry["Behavior"]
        )
        global_cnt += failed_count
        processed += 1

    # Print summary
    total_duration = time.time() - total_start_time
    print(f"\n{'='*70}")
    print("GENERATION SUMMARY")
    print(f"{'='*70}")
    print(f"Total time: {total_duration:.2f} seconds")
    print(f"Entries processed: {processed}")
    print(f"Entries skipped (missing fields): {skipped}")
    print(f"Entries skipped (already exist): {existing}")
    print(f"Successful: {processed - global_cnt}")
    print(f"Failed: {global_cnt}")
    print(f"\n✅ Results saved in:")
    print(f" - PlantUML code: {OUTPUT_CODE_DIR}/")
    print(f" - Generated images: {OUTPUT_IMAGE_DIR}/")
    print(f" - Detailed log: claude_plantuml_generation.log")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()