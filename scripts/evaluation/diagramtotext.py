import os
import csv
import json
import re
import PIL.Image
import google.generativeai as genai
import time
def load_image(image_path):
    return PIL.Image.open(image_path)

def extract_components_and_connectors(image_path, model):
    image = load_image(image_path)

    prompt = '''
You are analyzing a software architecture diagram. Extract **all** possible information into a structured JSON format. Include:

- components and their names, descriptions (if any), and boundaries (e.g., microservice, database)
- connectors between components, along with descriptions, direction, and type (HTTP, RPC, etc.)
- any textual annotations present in the diagram and their relative positions
- logical groups or layers of components
- diagram metadata (like title, filename)

Use the following JSON structure exactly and do NOT include any explanation text:

```json
{
  "components": [
    {
      "name": "ComponentA",
      "description": "optional",
      "boundary": "optional",
      "position": {"x": 0, "y": 0}
    }
  ],
  "connectors": [
    {
      "source": "ComponentA",
      "target": "ComponentB",
      "label": "optional",
      "description": "optional",
      "type": "optional"
    }
  ],
  "annotations": [
    {
      "text": "optional",
      "position": {"x": 0, "y": 0}
    }
  ],
  "groups": [
    {
      "name": "optional",
      "components": ["ComponentA"],
      "boundary": "optional"
    }
  ],
  "metadata": {
    "diagram_title": "optional",
    "extracted_from": "filename.png",
    "date_extracted": "optional"
  }
}
```
'''


    response = model.generate_content([prompt, image])
    text = getattr(response, 'text', '') or ''
    # First try direct JSON parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Fallback: extract the first {...} substring
        match = re.search(r'\{[\s\S]*\}', text)
        if match:
            snippet = match.group(0)
            try:
                return json.loads(snippet)
            except json.JSONDecodeError:
                pass

    # log for debugging
    log_path = "gemini_raw_responses.log"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"--- {os.path.basename(image_path)} ---\n{repr(text)}\n\n")
    return None


def write_to_json(image_name, data, output_dir="json_outputs"):
    os.makedirs(output_dir, exist_ok=True)
    json_path = os.path.join(output_dir, f"{image_name.rsplit('.', 1)[0]}.json")
    
    with open(json_path, mode='w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)


def main():
    genai.configure(api_key="AIzaSyA19TLhE8m7qJuNy5VaKB7Ns7f_ymsWH4I")
    model = genai.GenerativeModel("gemini-2.0-flash-exp")

    input_folder = "../initial_images"
    for image_name in os.listdir(input_folder):
        image_path = os.path.join(input_folder, image_name)
        
        try:
            result = extract_components_and_connectors(image_path, model)
            if result:
                write_to_json(image_name, result)
                print(f"Processed and saved: {image_name}")
            else:
                print(f"No data extracted from: {image_name}")
        except Exception as e:
            print(f"Error processing {image_name}: {str(e)}")
        time.sleep(10)
if __name__ == "__main__":
    main()
