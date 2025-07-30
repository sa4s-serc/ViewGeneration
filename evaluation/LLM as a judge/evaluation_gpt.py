import os
import json
import re
import time
import openai
import base64

openai.api_key = ""

def load_image_as_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

def extract_and_compare_images(image_path1, image_path2):
    print(f"Processing image pair:\n  GroundTruth: {image_path1}\n  Generated: {image_path2}")
    base64_img1 = load_image_as_base64(image_path1)
    base64_img2 = load_image_as_base64(image_path2)

    prompt = '''
You are analyzing two software architecture diagrams. Extract **all** possible information from BOTH diagrams into structured JSON and COMPARE them.

**Step 1: Extract**
For each diagram, extract:
- Components (with names, descriptions, boundaries, and positions)
- Connectors (with source/target, label, type, etc.)
- Annotations
- Logical groups/layers
- Metadata (filename, title if found)

**Step 2: Compare**
- Identify similar/same components by name or purpose.
- Identify same/similar connectors.
- Highlight differences (components or connections present in one but not the other).
- Analyze the architectural structure, organization (e.g., layers or services), and any observable design patterns.

**Step 3: Explain**
- Provide a natural-language explanation summarizing the similarities and differences between the two diagrams.
- Include points about structure, shared elements, and key distinctions in architecture.

Return a JSON object in this exact structure:
```json
{
 "GroundTruth": {
 "components": [],
 "connectors": [],
 "annotations": [],
 "groups": [],
 "metadata": {}
 },
 "GeneratedImage": {
 "components": [],
 "connectors": [],
 "annotations": [],
 "groups": [],
 "metadata": {}
 },
 "comparison": {
 "common_components": [],
 "unique_to_GroundTruth": [],
 "unique_to_GeneratedImage": [],
 "common_connectors": [],
 "unique_connectors_GroundTruth": [],
 "unique_connectors_GeneratedImage": [],
 "explanation": "A detailed explanation highlighting similarities and differences between the two diagrams and also please rate the generated image on a scale of 1 to 10 based on its accuracy and completeness, similarity compared to the ground truth and explain the reasoning behind the rating.",
 "Rating": 0
 }
}
Only return valid JSON.
'''

    messages = [
        {"role": "system", "content": "You are a software architecture expert."},
        {"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_img1}"}},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_img2}"}},
        ]}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.3
        )
        text = response.choices[0].message.get("content", "")
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return None

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r'\{[\s\S]*\}', text)
        if match:
            snippet = match.group(0)
            try:
                return json.loads(snippet)
            except json.JSONDecodeError:
                pass

        # Log raw output
        with open("gpt4o_raw_responses.log", "a", encoding="utf-8") as f:
            f.write(f"--- {os.path.basename(image_path1)} & {os.path.basename(image_path2)} ---\n{text}\n\n")
        return None
def write_to_json(filename, data, output_dir="LLM_as_a_Judge_openai_outputs"):
    os.makedirs(output_dir, exist_ok=True)
    json_path = os.path.join(output_dir, f"{filename}.json")
    with open(json_path, mode='w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)

def get_files_by_stem(folder):
    file_map = {}
    for fname in os.listdir(folder):
        stem, _ = os.path.splitext(fname)
        file_map[stem] = fname
    return file_map

def main():
    output_dir = "LLM_as_a_Judge_openai_outputs"
    folder1 = "./initial_images"
    folder2 = "./zeroShot_gpt_output_images"

    files1 = get_files_by_stem(folder1)
    files2 = get_files_by_stem(folder2)
    common_stems = sorted(set(files1.keys()) & set(files2.keys()))
    # tried=0
    print("started")
    for stem in common_stems:
        # if tried>10:
        #     break
        output_filename = f"{stem}_comparison.json"
        output_path = os.path.join(output_dir, output_filename)

        if os.path.exists(output_path):
            print(f"Skipping {stem} — already evaluated.")
            continue

        file1 = os.path.join(folder1, files1[stem])
        file2 = os.path.join(folder2, files2[stem])
        # tried+=1
        try:
            result = extract_and_compare_images(file1, file2)
            if result:
                write_to_json(f"{stem}_comparison", result, output_dir)
                print(f"Compared and saved: {stem}_comparison.json")
            else:
                print(f"Comparison failed for: {stem}")
        except Exception as e:
            print(f"Error comparing {stem}: {str(e)}")
        # time.sleep(10)
if __name__ == "__main__":
    main()