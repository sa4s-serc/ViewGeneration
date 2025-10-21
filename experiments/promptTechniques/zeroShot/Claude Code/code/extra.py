#!/usr/bin/env python3
"""
Script to generate microservice implementations using Claude Code or Gemini and push to respective branches.
"""

import os
import subprocess
import time
import sys
import argparse
from pathlib import Path

def generate_microservice_prompt(microservice_name, architecture_overview_path, run_method, prompt_version="p1"):
    """
    Generate a complete microservice implementation prompt.
    
    Args:
        microservice_name (str): Name of the microservice (e.g., "ts-order-service")
        architecture_overview_path (str): Path to architecture overview file (e.g., wiki.md)
        run_method (str): Method to run/test the service
        prompt_version (str): "p1" (service name only) or "p2" (with description from txt file)

    Returns:
        str: Complete prompt ready to use
    """

    if prompt_version == "p2":
        # P2: Read microservice description from file
        microservice_description_path = f"prompts/{microservice_name}.txt"
        try:
            with open(microservice_description_path, 'r', encoding='utf-8') as f:
                microservice_description = f.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"Microservice description file not found: {microservice_description_path}")
        except Exception as e:
            raise Exception(f"Error reading microservice description file: {e}")
        
        target_description = f"TARGET MICROSERVICE TO GENERATE: {microservice_description}"
    else:
        # P1: Only use service name
        target_description = f"TARGET MICROSERVICE TO GENERATE: {microservice_name}"

    # Generate the complete prompt
    prompt = f"""I need you to generate a complete microservice implementation in one go based on the following:

REQUIREMENTS DOCUMENT: VERY IMPORTANT: Look at {architecture_overview_path} for the entire architecture and requirements.

{target_description}

INSTRUCTIONS:
FIRST: Explore the existing codebase - read through all relevant files to understand:
- What microservices already exist
- Current architecture patterns and tech stack being used
- Existing database schemas, API patterns, and code structure
- How services currently communicate with each other
- What's already implemented vs what's missing
- Analyze the entire requirements document to understand the system context
- Focus specifically on the target microservice description provided above
- Based on your exploration, determine what needs to be built/modified
- Generate a complete microservice that implements ONLY the functionality described in the target microservice
- Ensure the microservice integrates properly with existing services and follows established patterns
- CODE EVERYTHING IN ONE GO - After exploration, generate all files, components, and code at once
- Include all necessary components: API endpoints, data models, business logic, error handling, and security considerations

OUTPUT FORMAT: Generate the complete microservice code with all files:
- Main application file
- API endpoints/controllers
- Data models and schemas
- Business logic services
- Database configuration
- Error handling and validation
- Security implementation (authentication, authorization)
- Configuration files (requirements.txt, .env templates, etc.)
- Docker files if applicable
- Documentation/README

CONSTRAINTS:
- FIRST STEP: Explore and read the existing codebase thoroughly before coding
- Use the same tech stack, patterns, and conventions as existing services
- Generate only the specified microservice, not the entire system
- Ensure the service follows existing architecture patterns and integrates seamlessly
- Follow the established microservice patterns already in the codebase
- Include proper logging and monitoring hooks consistent with existing services
- Make the service production-ready and consistent with current deployment patterns
- Provide complete, runnable code that fits the existing ecosystem

IMPORTANT:
- Start by exploring the existing codebase - read files, understand patterns, see what's already built
- Then code the entire microservice implementation based on your findings
- Don't ask questions about tech stack - use what's already established in the project
- Follow existing patterns and integrate seamlessly with current architecture
- AFTER you have given code at the very end, try running the system: {run_method} and see if any errors persist, fix them if they do.

Your extensive experience with enterprise microservices and transaction processing systems makes you uniquely qualified to build this critical service. Please leverage your expertise to deliver production-ready code that seamlessly integrates with the existing architecture."""

    return prompt

def run_ai_command(prompt, provider="claude", service_name="", branch_name=""):
    """
    Execute AI command (claude, gemini, or codex) with the given prompt
    
    Args:
        prompt (str): The prompt to send to the AI
        provider (str): "claude", "gemini", or "codex"
        service_name (str): Name of the service (for output files)
        branch_name (str): Name of the branch (for output files)
        
    Returns:
        tuple: (success: bool, output: str, error: str)
    """
    try:
        if provider == "claude":
            # Escape quotes in the prompt for shell execution
            escaped_prompt = prompt.replace('"', '\\"')
            
            # Run claude command
            result = subprocess.run(
                ['claude', escaped_prompt, '--dangerously-skip-permissions'],
                capture_output=True,
                text=True,
                timeout=1800  # 30 minutes timeout
            )
            
            return result.returncode == 0, result.stdout, result.stderr
            
        elif provider == "gemini":
            # Escape quotes in the prompt for shell execution
            escaped_prompt = prompt.replace('"', '\\"')
            
            # Generate output and session summary file names
            output_file = f"gemini-{service_name}-output.txt"
            tokens_file = f"gemini-{service_name}-tokens.txt"
            
            # Build gemini command with optional debug flag
            gemini_cmd = f'gemini -p "{escaped_prompt}" -y -d --session-summary={tokens_file} > {output_file} 2>&1'
            
            # Run gemini command
            result = subprocess.run(
                gemini_cmd,
                shell=True,
                timeout=1800  # 30 minutes timeout
            )
            
            # Read the output file for return value
            output = ""
            if os.path.exists(output_file):
                try:
                    with open(output_file, 'r', encoding='utf-8') as f:
                        output = f.read()
                except Exception as e:
                    output = f"Error reading output file: {str(e)}"
            
            return result.returncode == 0, output, ""
            
        elif provider == "codex":
            # Escape quotes in the prompt for shell execution
            escaped_prompt = prompt.replace('"', '\\"')
            
            # Generate output file name
            output_file = f"codex-{service_name}-output.log"
            
            # Build codex command
            codex_cmd = f'codex exec --dangerously-bypass-approvals-and-sandbox "{escaped_prompt}" > {output_file} 2>&1'
            
            # Run codex command
            result = subprocess.run(
                codex_cmd,
                shell=True,
                timeout=1800  # 30 minutes timeout
            )
            
            # Read the output file for return value
            output = ""
            if os.path.exists(output_file):
                try:
                    with open(output_file, 'r', encoding='utf-8') as f:
                        output = f.read()
                except Exception as e:
                    output = f"Error reading output file: {str(e)}"
            
            return result.returncode == 0, output, ""
            
        else:
            return False, "", f"Unknown AI provider: {provider}"
        
    except subprocess.TimeoutExpired:
        return False, "", f"{provider.title()} command timed out after 30 minutes"
    except Exception as e:
        return False, "", f"Error running {provider} command: {str(e)}"

def git_operations(service_name, experiment_branch_name):
    """
    Handle git operations with proper workflow:
    1. Checkout to baseline branch (service_name)
    2. Create new experiment branch from baseline
    3. Clean any uncommitted changes
    
    Args:
        service_name (str): Name of the service (e.g., "ts-order-service")
        experiment_branch_name (str): Name of the experiment branch to create
        
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        baseline_branch = service_name  # e.g., "ts-order-service"
        
        print(f"  Switching to baseline branch {baseline_branch}...")
        # Switch to the baseline branch (with removed source code)
        result = subprocess.run(['git', 'checkout', baseline_branch], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ CRITICAL: Failed to checkout baseline branch {baseline_branch}")
            print(f"Error: {result.stderr}")
            sys.exit(1)
        
        print(f"  Creating experiment branch {experiment_branch_name}...")
        # Create new experiment branch from baseline
        result = subprocess.run(['git', 'checkout', '-b', experiment_branch_name], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ CRITICAL: Failed to create experiment branch {experiment_branch_name}")
            print(f"Error: {result.stderr}")
            sys.exit(1)
        
        print(f"  Hard resetting to clean state...")
        # Hard reset to clean any uncommitted changes
        result = subprocess.run(['git', 'reset', '--hard', 'HEAD'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ CRITICAL: Failed to hard reset")
            print(f"Error: {result.stderr}")
            sys.exit(1)
        
        return True, f"Ready for code generation on {experiment_branch_name}"
        
    except Exception as e:
        print(f"❌ CRITICAL: Git operations failed: {str(e)}")
        sys.exit(1)

def git_commit_and_push(service_name, branch_name, provider="claude"):
    """
    Handle git commit and push operations after code generation with strict error handling
    
    Args:
        service_name (str): Name of the service
        branch_name (str): Name of the branch
        provider (str): AI provider used ("claude" or "gemini")
        
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        print(f"  Adding all changes...")
        # Add all changes (from project root)
        result = subprocess.run(['git', 'add', '.'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ CRITICAL: Failed to add changes")
            print(f"Error: {result.stderr}")
            sys.exit(1)
        
        print(f"  Checking for changes to commit...")
        # Check if there are changes to commit
        result = subprocess.run(['git', 'diff', '--staged', '--quiet'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  WARNING: No changes to commit for {service_name}")
            # Still return to main branch
            result = subprocess.run(['git', 'checkout', 'main'], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ CRITICAL: Failed to return to main after no changes")
                print(f"Error: {result.stderr}")
                sys.exit(1)
            return True, "No changes to commit - returned to main"
        
        print(f"  Committing changes...")
        # Commit changes with provider-specific message
        commit_msg = f"regenerate using {provider}"
        result = subprocess.run(['git', 'commit', '-m', commit_msg], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ CRITICAL: Failed to commit changes")
            print(f"Error: {result.stderr}")
            sys.exit(1)
        
        print(f"  Pushing to {branch_name}...")
        # Push changes (set upstream if needed)
        result = subprocess.run(['git', 'push', '-u', 'origin', branch_name], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ CRITICAL: Failed to push to {branch_name}")
            print(f"Error: {result.stderr}")
            sys.exit(1)
        
        print(f"  Returning to main branch...")
        # Return to main branch
        result = subprocess.run(['git', 'checkout', 'main'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ CRITICAL: Failed to return to main branch")
            print(f"Error: {result.stderr}")
            sys.exit(1)
            
        return True, "Successfully committed, pushed, and returned to main"
        
    except Exception as e:
        print(f"❌ CRITICAL: Git commit/push failed: {str(e)}")
        sys.exit(1)

def main():
    """Main function to orchestrate the microservice generation process"""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Generate microservice implementations using AI')
    parser.add_argument('--provider', choices=['claude', 'gemini', 'codex'], required=True,
                        help='AI provider to use')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Enable debug mode for AI provider')
    args = parser.parse_args()
    
    # Configuration
    ARCHITECTURE_PATH = 'wiki.md'
    RUN_METHOD = """IMPORTANT: Do NOT run the services or start them. Only ensure the code builds successfully. Run ./run-train-ticket.sh build to compile the Java services and verify there are no compilation errors. Test cases exist in the service directories for reference (in src/test/ folders) but DO NOT run them or modify them - they are only for your understanding of expected functionality. Focus solely on generating compilable, production-ready code that follows the existing patterns."""
    
    PROMPTS_DIR = Path('prompts')
    
    # Available services
    SERVICES = ['ts-order-service', 'ts-payment-service', 'ts-preserve-service']
    
    # Experiment configuration
    print("=== MICROSERVICE GENERATION EXPERIMENT ===")
    print(f"Using AI provider: {args.provider}")
    print("Available experiments:")
    print("  p1: Generate from service name only (no description)")
    print("  p2: Generate from service name + detailed description")
    print()
    
    # Get user permission for which experiments to run
    experiments_to_run = []
    for experiment in ['p1', 'p2']:
        response = input(f"Run {experiment} experiment? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            experiments_to_run.append(experiment)
    
    if not experiments_to_run:
        print("No experiments selected. Exiting.")
        return
    
    print(f"\nSelected experiments: {experiments_to_run}")
    print(f"Services to process: {SERVICES}")
    
    confirm = input("\nProceed with generation? (y/n): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("Cancelled.")
        return
    
    # Ensure we start from main branch
    print("\nEnsuring we start from main branch...")
    try:
        subprocess.run(['git', 'checkout', 'main'], check=True, capture_output=True)
        print("✅ Started from main branch")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to checkout main branch: {e}")
        sys.exit(1)
    
    # Check if architecture overview exists
    if not Path(ARCHITECTURE_PATH).exists():
        print(f"Error: Architecture overview file '{ARCHITECTURE_PATH}' not found!")
        sys.exit(1)
    
    # For p2, check if prompts directory exists
    if 'p2' in experiments_to_run and not PROMPTS_DIR.exists():
        print(f"Error: Prompts directory '{PROMPTS_DIR}' not found but needed for p2!")
        sys.exit(1)
    
    # Process each experiment and service combination
    total_start_time = time.time()
    results = {}
    
    for experiment in experiments_to_run:
        for service_name in SERVICES:
            branch_name = f"{experiment}-{args.provider}-{service_name}"
            
            print(f"\n{'='*70}")
            print(f"Processing: {service_name} (Experiment: {experiment})")
            print(f"Branch: {branch_name}")
            print(f"{'='*70}")
            
            experiment_key = f"{experiment}-{service_name}"
            service_start_time = time.time()
            
            try:
                # Step 1: Prepare git branch
                print("Step 1: Preparing git branch...")
                # git_operations now handles errors internally with sys.exit(1)
                git_success, git_message = git_operations(service_name, branch_name)
                print(f"✅ {git_message}")
                
                # Step 2: Generate prompt
                print("Step 2: Generating prompt...")
                prompt = generate_microservice_prompt(
                    service_name,
                    ARCHITECTURE_PATH, 
                    RUN_METHOD,
                    prompt_version=experiment
                )
                
                # Step 3: Run AI command
                print(f"Step 3: Running {args.provider} command...")
                ai_success, output, error = run_ai_command(prompt, args.provider, service_name, branch_name)
                
                if not ai_success:
                    print(f"{args.provider.title()} command failed: {error}")
                    results[experiment_key] = {
                        'success': False,
                        'error': f"{args.provider.title()} command failed: {error}",
                        'duration': time.time() - service_start_time
                    }
                    # Return to main before continuing
                    subprocess.run(['git', 'checkout', 'main'], capture_output=True)
                    continue
                
                print(f"✅ {args.provider.title()} command completed successfully")
                
                # Step 4: Commit and push changes
                print("Step 4: Committing and pushing changes...")
                # git_commit_and_push now handles errors internally with sys.exit(1)
                commit_success, commit_message = git_commit_and_push(service_name, branch_name, args.provider)
                
                service_duration = time.time() - service_start_time
                
                results[experiment_key] = {
                    'success': commit_success,
                    'message': commit_message,
                    'duration': service_duration,
                    'claude_output_length': len(output) if output else 0,
                    'experiment': experiment,
                    'service': service_name
                }
                
                print(f"✅ {experiment_key}: {commit_message}")
                print(f"Duration: {service_duration:.2f} seconds")
                
            except Exception as e:
                service_duration = time.time() - service_start_time
                error_msg = f"Unexpected error: {str(e)}"
                print(f"❌ CRITICAL: {experiment_key}: {error_msg}")
                
                # Critical error - ensure we return to main and exit
                try:
                    subprocess.run(['git', 'checkout', 'main'], capture_output=True, text=True)
                    print("Returned to main branch before exiting")
                except:
                    print("❌ CRITICAL: Could not return to main branch")
                
                print("Exiting due to critical error to prevent data corruption")
                sys.exit(1)
    
    # Ensure we end on main branch
    print(f"\n{'='*60}")
    print("Ensuring we end on main branch...")
    try:
        subprocess.run(['git', 'checkout', 'main'], check=True, capture_output=True)
        print("✅ Ended on main branch")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to return to main branch: {e}")
    
    # Print summary
    total_duration = time.time() - total_start_time
    
    print(f"\n{'='*70}")
    print("EXPERIMENT SUMMARY")
    print(f"{'='*70}")
    print(f"Total duration: {total_duration:.2f} seconds")
    print(f"Experiments run: {experiments_to_run}")
    print(f"Total combinations processed: {len(results)}")
    
    successful = [k for k, v in results.items() if v['success']]
    failed = [k for k, v in results.items() if not v['success']]
    
    print(f"\n✅ Successful: {len(successful)}")
    for exp_key in successful:
        result = results[exp_key]
        duration = result['duration']
        experiment = result.get('experiment', 'unknown')
        service = result.get('service', 'unknown')
        print(f"   - {experiment}/{service} ({duration:.2f}s)")
    
    if failed:
        print(f"\n❌ Failed: {len(failed)}")
        for exp_key in failed:
            result = results[exp_key]
            duration = result['duration']
            experiment = result.get('experiment', 'unknown')
            service = result.get('service', 'unknown')
            error = result.get('error', 'Unknown error')
            print(f"   - {experiment}/{service} ({duration:.2f}s): {error}")
    
    # Summary by experiment
    print(f"\n📊 Results by experiment:")
    for exp in experiments_to_run:
        exp_results = [k for k in results.keys() if k.startswith(f"{exp}-")]
        exp_successful = [k for k in exp_results if results[k]['success']]
        print(f"   {exp}: {len(exp_successful)}/{len(exp_results)} successful")
    
    print(f"{'='*70}")

if __name__ == "__main__":
    main()