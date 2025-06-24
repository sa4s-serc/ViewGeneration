import os
import csv
import json
import re
import PIL.Image
import google.generativeai as genai
import time

def load_image(image_path):
    return PIL.Image.open(image_path)

def extract_and_compare_images(image_path1, image_path2, model):
    image1 = load_image(image_path1)
    image2 = load_image(image_path2)
    
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
     "diagram1": {
     "components": [],
     "connectors": [],
     "annotations": [],
     "groups": [],
     "metadata": {}
     },
     "diagram2": {
     "components": [],
     "connectors": [],
     "annotations": [],
     "groups": [],
     "metadata": {}
     },
     "comparison": {
     "common_components": [],
     "unique_to_diagram1": [],
     "unique_to_diagram2": [],
     "common_connectors": [],
     "unique_connectors_diagram1": [],
     "unique_connectors_diagram2": [],
     "explanation": "A detailed explanation highlighting similarities and differences between the two diagrams and also be as a judge and provide a score from 0 to 10 based on the quality of the diagrams and determine which diagram is better and why."
     }
    }
    Provide ONLY this JSON output without additional text or explanations.
    '''
    
    response = model.generate_content([prompt, image1, image2])
    text = getattr(response, 'text', '') or ''
    
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
        
        # Log raw response for debugging
        with open("gemini_raw_responses.log", "a", encoding="utf-8") as f:
            f.write(f"--- {os.path.basename(image_path1)} & {os.path.basename(image_path2)} ---\n{repr(text)}\n\n")
        
        return None

def write_to_json(filename, data, output_dir="json_outputs"):
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
    genai.configure(api_key="")
    model = genai.GenerativeModel("gemini-2.0-flash-exp")
    
    folder1 = "./initial_images"
    folder2 = "./fewShot_deepseek_output_images"
    

    files1 = get_files_by_stem(folder1)
    files2 = get_files_by_stem(folder2)
    common_stems = sorted(set(files1.keys()) & set(files2.keys()))

    
    for stem in common_stems:
        file1 = os.path.join(folder1, files1[stem])
        file2 = os.path.join(folder2, files2[stem])
        
        try:
            result = extract_and_compare_images(file1, file2, model)
            if result:
                base_name = f"{stem}_comparison"
                write_to_json(base_name, result)
                print(f"Compared and saved: {base_name}.json")
            else:
                print(f"Comparison failed for: {stem}")
        except Exception as e:
            print(f"Error comparing {stem}: {str(e)}")
        
        time.sleep(10)


if __name__ == "__main__":
    main()