"""
Summarization pipeline agent with chunked repo summarization:
- Clones a GitHub repo from a given link
- Extracts code and docs while excluding data/binaries/build artifacts
- Builds a shallow repo tree structure for context
- Splits content into chunks
- Summarizes each chunk
- Merges partial summaries into a final cohesive summary
"""

import os
import tempfile
import shutil
import subprocess
from typing import List
from moya.agents.openai_agent import OpenAIAgent, OpenAIAgentConfig

CODE_EXTENSIONS = {'.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rb', '.rs', '.cs', '.php', '.swift', '.kt', '.scala', '.m', '.h', '.sh', '.pl', '.lua', '.r', '.jl'}

# Exclusions and limits adapted from experiments/Architectural_knowledge_extraction/Summary_extraction.py
EXCLUDE_EXTENSIONS = {
    '.csv', '.tsv', '.xlsx', '.xls', '.json',
    '.sqlite', '.db', '.sql', '.parquet', '.avro', '.orc',
    '.lock', '.gradle', '.maven', '.sbt',
    '.exe', '.dll', '.so', '.dylib', '.a', '.lib', '.obj', '.o',
    '.bin', '.dat', '.zip', '.tar', '.gz', '.bz2', '.xz', '.7z',
    '.rar', '.jar', '.war', '.ear',
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.ico',
    '.webp', '.raw', '.cr2', '.nef', '.arw',
    '.mp3', '.wav', '.flac', '.aac', '.ogg', '.mp4', '.avi', '.mkv',
    '.mov', '.wmv', '.flv', '.webm', '.m4a', '.wma',
    '.pdf', '.ppt', '.pptx', '.xls', '.xlsx',
    '.ttf', '.otf', '.woff', '.woff2', '.eot',
    '.pickle', '.pkl', '.npy', '.npz', '.mat', '.rds', '.feather'
}

EXCLUDE_FILENAMES = {
    'package-lock.json', 'yarn.lock', 'composer.lock', 'Pipfile.lock',
    'poetry.lock', 'pnpm-lock.yaml', 'npm-shrinkwrap.json',
    'CMakeLists.txt', 'build.gradle', 'build.sbt',
    'Dockerfile', '.gitignore', '.dockerignore', '.eslintignore', '.prettierignore'
}

SKIP_DIRS = {
    '.git', 'node_modules', '__pycache__', '.pytest_cache',
    'venv', 'env', '.venv', 'dist', 'target',
}

MAX_FILE_BYTES = 2_000_000  # 2MB per file guardrail

def is_likely_data_file(content: str, filename: str) -> bool:
    if any(filename.lower().endswith(ext) for ext in ['.py', '.js', '.java', '.cpp', '.c', '.h', '.md', '.txt', '.rst']):
        return False
    lines = content.split('\n')
    if len(lines) < 10:
        return False
    comma_lines = sum(1 for line in lines if line.count(',') > 5)
    pipe_lines = sum(1 for line in lines if line.count('|') > 3)
    tab_lines = sum(1 for line in lines if line.count('\t') > 3)
    data_lines = comma_lines + pipe_lines + tab_lines
    return data_lines > len(lines) * 0.5

def clone_repository(github_url: str) -> str:
    temp_dir = tempfile.mkdtemp()
    subprocess.run(["git", "clone", github_url, temp_dir], check=True, capture_output=True)
    return temp_dir

def build_repo_structure(repo_path: str) -> str:
    try:
        if os.name == "nt":
            result = subprocess.run(["tree", "/F", repo_path], capture_output=True, text=True, shell=True)
        else:
            result = subprocess.run(["tree", "-L", "3", repo_path], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Error generating repository structure: {e}"

def extract_contents(repo_path: str) -> str:
    extracted_data: List[str] = []
    for dirpath, dirnames, filenames in os.walk(repo_path):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            _, ext = os.path.splitext(filename.lower())
            if ext in EXCLUDE_EXTENSIONS:
                continue
            if filename.lower() in EXCLUDE_FILENAMES:
                continue
            if filename.lower().endswith(('.json', '.lock', '.xml')) and any(
                build_word in filename.lower() for build_word in ['package', 'composer', 'build', 'gradle', 'maven']
            ):
                continue
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                if len(content) > MAX_FILE_BYTES:
                    continue
                if is_likely_data_file(content, filename):
                    continue
                extracted_data.append(f"--- File: {os.path.relpath(file_path, repo_path)} ---\n")
                extracted_data.append(content)
                extracted_data.append("\n\n")
            except Exception:
                continue
    return "".join(extracted_data)

def chunk_text(text: str, max_words: int = 8000) -> List[str]:
    words = text.split()
    chunks: List[str] = []
    current: List[str] = []
    for w in words:
        current.append(w)
        if len(current) >= max_words:
            chunks.append(" ".join(current))
            current = []
    if current:
        chunks.append(" ".join(current))
    return chunks

class SummarizationPipelineAgent(OpenAIAgent):
    def __init__(self, config):
        super().__init__(config)

    def summarize_github_repo(self, github_url: str) -> str:
        temp_dir = None
        try:
            temp_dir = clone_repository(github_url)
            repo_structure = build_repo_structure(temp_dir)
            repo_contents = extract_contents(temp_dir)
            if not repo_contents.strip():
                return "[SummarizationPipelineAgent] No eligible content found in the repository."

            chunks = chunk_text(repo_contents, max_words=8000)
            partial_summaries: List[str] = []
            system_prompt = "You are a helpful assistant that summarizes codebases accurately and concisely."

            # Route prompts through the OpenAIAgent's response method (no tools)
            for i, chunk in enumerate(chunks, start=1):
                chunk_prompt = (
                    f"This is part {i} of {len(chunks)} from a GitHub repository analysis.\n\n"
                    f"Repository Structure (depth 3):\n{repo_structure}\n\n"
                    f"Repository Contents (Chunk {i}):\n{chunk}\n\n"
                    "Please analyze this part and generate a summary that includes:\n"
                    "- Key functionalities and components\n"
                    "- Important files and their roles\n"
                    "- Architectural insights (if relevant)\n"
                    "- Any notable design patterns\n"
                    "Keep your response modular so it can be merged with other parts."
                )
                try:
                    message = self.get_response([
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": chunk_prompt},
                    ])
                    partial = (message.get("content", "") if isinstance(message, dict) else "").strip()
                    if not partial:
                        partial = "[Empty summary returned]"
                except Exception as e:
                    partial = f"[Error summarizing chunk {i}: {e}]"
                partial_summaries.append(partial)

            final_prompt = (
                "The following are partial summaries from an analysis of a GitHub repository:\n\n"
                + "\n\n".join(partial_summaries)
                + "\n\nPlease merge these summaries into a single, well-structured report. Ensure that:\n"
                "- There is no repetition\n"
                "- The information flows logically\n"
                "- The final report provides a cohesive overview of important components, functionality, and architecture.\n"
                "IMPORTANT: Your response must not exceed 4000 tokens. Prioritize the most critical information."
            )

            try:
                message = self.get_response([
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": final_prompt},
                ])
                final_summary = (message.get("content", "") if isinstance(message, dict) else "").strip()
                if not final_summary:
                    final_summary = "[Empty final summary returned]"
            except Exception as e:
                final_summary = f"[Error merging summaries: {e}]"

            return final_summary
        finally:
            if temp_dir and os.path.isdir(temp_dir):
                shutil.rmtree(temp_dir)

def main():
    config = OpenAIAgentConfig(
        agent_name="summarization_pipeline_agent",
        description="Agent that summarizes code from a GitHub repo.",
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name="gpt-4o",
        agent_type="SummarizationPipelineAgent",
        is_streaming=False,
        system_prompt="You are an agent that summarizes code from GitHub repositories."
    )
    # agent = SummarizationPipelineAgent(config)
    # summary = agent.summarize_github_repo(github_url)
    # print("\nSummary:\n", summary)

if __name__ == "__main__":
    main()
