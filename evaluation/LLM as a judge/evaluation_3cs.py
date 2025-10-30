'''This script uses OpenAI's GPT-4o model to compare two sets of software architecture diagrams.
It extracts structured information from both diagrams and generates a JSON report with comparisons.
The script handles images with the same stem name in both folders, ensuring that only valid comparisons are made.
It also manages API interactions with OpenAI, including error handling and response parsing.'''

import os
import json
import re
import time
from openai import OpenAI
import base64

client = OpenAI(api_key="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")


def load_image_as_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

def extract_and_compare_images(image_path1, image_path2):
    print(f"Processing image pair:\n  GroundTruth: {image_path1}\n  Generated: {image_path2}")
    base64_img1 = load_image_as_base64(image_path1)
    base64_img2 = load_image_as_base64(image_path2)

    prompt = '''
**Objective:** Evaluate the quality of the generated architecture diagram by comparing it with the ground truth diagram.
**Instructions:** 
1. The first attached image is the ground truth image, and the second attached image is the generated image.
2. Evaluate the generated diagram according to the criteria below.
3. For each criterion, select one rating:
    - **Meets Expectations**: No significant issues.
    - **Partially Meets Expectations**: Minor issues or small improvements needed.
    - **Does Not Meet Expectations**: Major issues or incorrect/missing elements.
4. Provide a brief justification for each rating, focusing on specific observations from the diagrams.
**Evaluation Criteria:**
1. **Clarity**: The generated diagram should be understandable to both technical and non-technical stakeholders. 
        - Assess whether the symbols, icons, labels, information, components, connectors are clear and unambiguous.
        - Make sure each component has a clear and descriptive name that reflects its purpose or function.
        - Verify that components are arranged in a logical and readable layout.
2. **Consistency:** Check whether symbols, icons, styles, and notations, connectors, components are used uniformly throughout the diagram.
        - Assess whether the generated diagram is structurally and semantically aligned with the ground truth diagram.
3. **Completeness:** Evaluate whether the diagram includes all the necessary information from the ground truth.
        - Identify any missing, extra, or incorrect elements or connections.

Output Format:
Return a JSON object in the exact structure below, filling in the rating (Meets Expectations, Partially Meets Expectations, or Does Not Meet Expectations) and justification for each criterion.
```json
{
  "Clarity": {
    "rating": "",
    "justification": ""
  },
  "Completeness": {
    "rating": "",
    "justification": ""
  },
  "Consistency": {
    "rating": "",
    "justification": ""
  }
}
```
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
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.3
        )
        text = response.choices[0].message.content
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
def write_to_json(filename, data, output_dir="LLM_as_a_Judge_openai_outputs_3cs"):
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
    output_dir = "LLM_as_a_Judge_openai_outputs_3cs"
    folder1 = "./initial_images"
    folder2 = "./approach_gpt_python_images"
    tried=0
    files1 = get_files_by_stem(folder1)
    files2 = get_files_by_stem(folder2)
    common_stems = sorted(set(files1.keys()) & set(files2.keys()))
    print("started")
    for stem in common_stems:
        # if tried>5:
        #     break
        output_filename = f"{stem}_comparison.json"
        output_path = os.path.join(output_dir, output_filename)

        if os.path.exists(output_path):
            print(f"Skipping {stem} — already evaluated.")
            continue

        file1 = os.path.join(folder1, files1[stem])
        file2 = os.path.join(folder2, files2[stem])
        tried+=1
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



# Results saved in results folder. Total failed attempts: 58