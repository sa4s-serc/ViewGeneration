import json

input_file = "generated_summaries.jsonl"
output_file = "UML.jsonl"

with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    for line in infile:
        if not line.strip():
            continue  # skip empty lines
        try:
            data = json.loads(line)
        except json.JSONDecodeError as e:
            print(f"Skipping invalid JSON line: {e}")
            continue

        if data.get("Architectural Notation", "").lower() == "uml":
            outfile.write(json.dumps(data) + "\n")

print(f"Filtered entries with Architectural Notation='UML' saved to {output_file}")
