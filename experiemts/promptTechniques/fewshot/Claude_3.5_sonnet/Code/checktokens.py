import json
import csv
import tiktoken
import os

def count_tokens_tiktoken(text, model_name="gpt-4"):
    try:
        encoding = tiktoken.encoding_for_model(model_name)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))

def load_few_shot_example(json_path="examples.json"):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading few-shot examples: {e}")
        return []

def build_prompt(summary, repo_name, concern, behavior, examples):
    diagram_type = "component" if behavior == "static" else "sequence"
    focus = "- Clearly shows main components and their relationships" if behavior == "static" else "- Clearly shows runtime interactions between components"

    system_instruction = f"""You are an expert software architect. Your job is to design architectural views using PlantUML based on system summaries.

Generate a **PlantUML {diagram_type} diagram** that:
{focus}
- Matches the system **behavior** and addresses the architectural **concern**
- Uses valid PlantUML syntax
- Outputs only PlantUML code (no explanation)
Name the diagram after this repository: **{repo_name}**

Below are some examples with summaries and the corresponding PlantUML diagrams for reference.
"""

    for i, ex in enumerate(examples):
        system_instruction += f"""

### Example {i + 1} Input:
Summary: {ex['summary']}
Concern: {ex['concern']}
Behavior: {ex['behavior']}

### Example {i + 1} Output:
{ex['plantuml_code']}
"""

    user_content = f"""### Actual Input:
Summary: {summary}
Concern: {concern}
Behavior: {behavior}

Please generate the appropriate PlantUML diagram."""

    full_prompt = system_instruction + user_content
    return full_prompt

def main():
    input_jsonl = "../../../../Architectural_knowledge_extraction/generated_summaries.jsonl"
    output_csv = "token_counts_not_completed.csv"
    required_keys = ["Repository Name", "summary", "Concern", "Behavior"]
    examples = load_few_shot_example()
    output_dir = "../fewShot_claude_output_images"

    rows = []

    try:
        with open(input_jsonl, 'r', encoding='utf-8') as f:
            entries = [json.loads(line) for line in f]
    except Exception as e:
        print(f"Error reading input file: {e}")
        return

    for entry in entries:
        if all(key in entry for key in required_keys):
            clean_repo_name = entry["Repository Name"].replace('/', '_').replace('\\', '_').rstrip('_')
            expected_output_path = os.path.join(output_dir, f"{clean_repo_name}.png")
            if os.path.exists(expected_output_path):
                print(f"✅ Diagram already exists for {clean_repo_name}, skipping...")
                continue
            else:
                print(f"🔍 Processing {entry['Repository Name']}...")
                repo = entry["Repository Name"].replace("/", "_").replace("\\", "_").strip()
                full_prompt = build_prompt(
                    entry["summary"],
                    repo,
                    entry["Concern"],
                    entry["Behavior"],
                    examples
                )
                token_count = count_tokens_tiktoken(full_prompt)
                print(f"{repo}: {token_count} tokens")
                rows.append({"Repository Name": repo, "Token Count": token_count})
        else:
            print(f"⚠️ Skipping invalid entry: {entry}")

    # Write to CSV
    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["Repository Name", "Token Count"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n✅ Token counts written to: {output_csv}")

if __name__ == "__main__":
    main()
